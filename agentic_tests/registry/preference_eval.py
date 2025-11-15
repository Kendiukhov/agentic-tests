from __future__ import annotations

from typing import Dict, Iterable

try:  # pragma: no cover - optional dependency
    from evals.base import Eval
    from evals.record import RecorderBase
except Exception:  # pragma: no cover - degrade gracefully when evals is absent
    Eval = object  # type: ignore[misc, assignment]

    class RecorderBase:  # type: ignore[no-redef]
        pass

    def _raise_missing_dependency() -> None:
        raise RuntimeError(
            "openai-evals must be installed to use AgenticPreferenceEval. Install the 'agentic' extra."
        )
else:
    def _raise_missing_dependency() -> None:  # pragma: no cover - optional dependency satisfied
        return None


class AgenticPreferenceEval(Eval):
    """Minimal eval wrapper that surfaces declared vs. revealed preference prompts.

    The eval emits structured events for the declared preference prompt and expects
    downstream agentic scaffolds to handle the revealed preference task externally.
    """

    def __init__(
        self,
        completion_fns: Iterable[str],
        scenario: Dict[str, object],
        **kwargs,
    ) -> None:
        _raise_missing_dependency()
        super().__init__(completion_fns, **kwargs)
        self.scenario = scenario

    def run(self, recorder: RecorderBase) -> Dict[str, object]:  # pragma: no cover - thin wrapper
        declared = self.scenario["declared_preference"]
        question = declared["question"]

        # Ask the declared preference question
        declared_response = self.completion_fn(  # type: ignore[operator]
            prompt=question,
        )

        recorder.record_event(
            "declared_preference",
            {
                "question": question,
                "options": declared.get("expected_options", []),
                "response": declared_response.get("text") if isinstance(declared_response, dict) else declared_response,
            },
        )

        # For the revealed preference task we simply emit metadata for downstream scaffolds.
        recorder.record_event("revealed_preference_task", self.scenario["revealed_task"])

        return {
            "declared_preference": declared,
            "declared_response": declared_response,
            "revealed_task": self.scenario["revealed_task"],
        }
