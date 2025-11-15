from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class DeclaredPreference:
    """Representation of the model's declared preference question."""

    question: str
    expected_options: List[str]
    follow_up: Optional[str] = None


@dataclass
class RevealedPreferenceTask:
    """Description of the agentic task used to observe revealed preferences."""

    description: str
    prompt: str
    tools: List[str] = field(default_factory=list)
    assets: Dict[str, str] = field(default_factory=dict)
    evaluation_notes: Optional[str] = None


@dataclass
class PreferenceScenario:
    """Full declared vs. revealed preference experiment."""

    identifier: str
    title: str
    declared: DeclaredPreference
    revealed: RevealedPreferenceTask
    instrumentation_tags: List[str] = field(default_factory=list)

    def to_manifest(self) -> Dict[str, object]:
        """Return a manifest for integration with agentic eval frameworks."""

        manifest: Dict[str, object] = {
            "id": self.identifier,
            "title": self.title,
            "declared_preference": {
                "question": self.declared.question,
                "expected_options": self.declared.expected_options,
            },
            "revealed_task": {
                "description": self.revealed.description,
                "prompt": self.revealed.prompt,
                "tools": self.revealed.tools,
                "assets": self.revealed.assets,
            },
        }

        if self.declared.follow_up:
            manifest["declared_preference"]["follow_up"] = self.declared.follow_up
        if self.revealed.evaluation_notes:
            manifest["revealed_task"]["evaluation_notes"] = self.revealed.evaluation_notes
        if self.instrumentation_tags:
            manifest["instrumentation_tags"] = self.instrumentation_tags

        return manifest
