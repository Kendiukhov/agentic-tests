from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, Optional

from .scenarios import PreferenceScenarios
from .types import PreferenceScenario

try:  # pragma: no cover - optional dependency
    from evals.registry import Registry
    from evals.runner import run  # type: ignore
except Exception:  # pragma: no cover - fallback when evals is absent
    Registry = None  # type: ignore
    run = None  # type: ignore


@dataclass
class ScenarioManifest:
    """Schema describing the manifest exported for openai-evals."""

    id: str
    title: str
    declared_preference: Dict[str, object]
    revealed_task: Dict[str, object]
    eval_spec: Dict[str, object]
    instrumentation_tags: Optional[Iterable[str]] = None


class AgenticPreferenceEvaluator:
    """Utility orchestrating the Agentic Process Preference Test scenarios."""

    def __init__(self, scenarios: Optional[Dict[str, PreferenceScenario]] = None):
        self._scenarios = scenarios or PreferenceScenarios.as_dict()

    # ------------------------------------------------------------------
    # Scenario discovery helpers
    # ------------------------------------------------------------------
    def scenario_ids(self) -> Iterable[str]:
        return self._scenarios.keys()

    def get(self, scenario_id: str) -> PreferenceScenario:
        try:
            return self._scenarios[scenario_id]
        except KeyError as exc:  # pragma: no cover - handled by CLI validations
            raise ValueError(f"Unknown scenario '{scenario_id}'.") from exc

    # ------------------------------------------------------------------
    # Manifest utilities
    # ------------------------------------------------------------------
    def build_eval_spec(self, scenario: PreferenceScenario) -> Dict[str, object]:
        return {
            "evals": {
                scenario.identifier: {
                    "id": scenario.identifier,
                    "class": "agentic_tests.registry.preference_eval:AgenticPreferenceEval",
                    "args": {
                        "scenario": scenario.to_manifest(),
                    },
                }
            }
        }

    def build_manifest(self, scenario_id: str) -> ScenarioManifest:
        scenario = self.get(scenario_id)
        manifest = scenario.to_manifest()
        eval_spec = self.build_eval_spec(scenario)
        return ScenarioManifest(
            id=manifest["id"],
            title=manifest["title"],
            declared_preference=manifest["declared_preference"],
            revealed_task=manifest["revealed_task"],
            eval_spec=eval_spec,
            instrumentation_tags=manifest.get("instrumentation_tags"),
        )

    def export_manifest(self, scenario_id: str, path: Path) -> Path:
        manifest = self.build_manifest(scenario_id)
        data = asdict(manifest)
        if path.suffix.lower() in {".yaml", ".yml"}:
            import yaml

            with path.open("w", encoding="utf-8") as fp:
                yaml.safe_dump(data, fp, sort_keys=False)
        else:
            with path.open("w", encoding="utf-8") as fp:
                json.dump(data, fp, indent=2)
        return path

    # ------------------------------------------------------------------
    # Execution helpers
    # ------------------------------------------------------------------
    def run_eval(
        self,
        scenario_id: str,
        model: str,
        registry_path: Optional[Path] = None,
        completion_fn: Optional[str] = None,
    ) -> Dict[str, object]:
        if Registry is None or run is None:  # pragma: no cover - optional dependency
            raise RuntimeError(
                "openai-evals is required to execute evaluations. Install the optional 'agentic' extra."
            )

        scenario = self.get(scenario_id)
        registry = Registry() if registry_path is None else Registry(str(registry_path))

        eval_spec = self.build_eval_spec(scenario)
        completion_fn = completion_fn or f"gpt-4o-mini::{model}"

        return run(
            completion_fn,
            eval_spec["evals"][scenario.identifier],
            registry=registry,
        )


# ----------------------------------------------------------------------
# Simple CLI setup using argparse (kept lightweight for offline usage)
# ----------------------------------------------------------------------
def build_cli() -> "argparse.ArgumentParser":  # pragma: no cover - thin wrapper
    import argparse

    parser = argparse.ArgumentParser(description="Agentic Process Preference Test harness")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List available scenarios")

    show_parser = subparsers.add_parser("show", help="Show a scenario manifest")
    show_parser.add_argument("scenario_id", help="Scenario identifier")

    export_parser = subparsers.add_parser("export", help="Export a scenario manifest")
    export_parser.add_argument("scenario_id", help="Scenario identifier")
    export_parser.add_argument("path", type=Path, help="Output file (JSON or YAML)")

    run_parser = subparsers.add_parser("run", help="Run a scenario via openai-evals")
    run_parser.add_argument("scenario_id", help="Scenario identifier")
    run_parser.add_argument("model", help="Model alias for the completion function registry")
    run_parser.add_argument("--registry-path", type=Path, default=None, help="Path to an openai-evals registry")
    run_parser.add_argument("--completion-fn", default=None, help="Override completion function identifier")

    return parser


def main(argv: Optional[Iterable[str]] = None) -> None:  # pragma: no cover - CLI wrapper
    parser = build_cli()
    args = parser.parse_args(argv)

    evaluator = AgenticPreferenceEvaluator()

    if args.command == "list":
        for scenario_id in evaluator.scenario_ids():
            scenario = evaluator.get(scenario_id)
            print(f"{scenario_id}: {scenario.title}")
    elif args.command == "show":
        manifest = evaluator.build_manifest(args.scenario_id)
        print(json.dumps(asdict(manifest), indent=2))
    elif args.command == "export":
        output_path = evaluator.export_manifest(args.scenario_id, args.path)
        print(f"Wrote manifest to {output_path}")
    elif args.command == "run":
        results = evaluator.run_eval(
            args.scenario_id,
            model=args.model,
            registry_path=args.registry_path,
            completion_fn=args.completion_fn,
        )
        print(json.dumps(results, indent=2))


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
