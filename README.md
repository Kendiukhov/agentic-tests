# Agentic Process Preference Tests

This repository contains an implementation of the "Agentic Process Preference Test" experimental harness. The harness
codifies declared versus revealed preference experiments across three scenarios: programming language selection,
HTTP client library usage, and workflow strategy for research-heavy writing tasks.

The implementation is built on top of an optional integration with the `openai-evals` agentic evaluation toolkit. The
core package offers:

- Structured scenario definitions that capture prompts, required tools, and evaluation hooks.
- Utilities to instrument agent runs in agentic scaffolds and record revealed preferences.
- A lightweight CLI for listing scenarios, exporting evaluation manifests, and running experiments once the
  `openai-evals` package is installed.

See `agentic_tests/scenarios.py` for high-level experiment definitions and `agentic_tests/runner.py` for the orchestration
logic that bridges scenarios with the agentic evaluation runtime.

## Usage

The CLI is intentionally dependency-light so it can be exercised in offline environments:

```bash
python -m agentic_tests.runner list
python -m agentic_tests.runner show programming-language
python -m agentic_tests.runner export programming-language manifest.json
```

Executing a scenario requires the optional `openai-evals` dependency:

```bash
pip install agentic-tests[agentic]
python -m agentic_tests.runner run programming-language gpt-4o
```

The `run` command defers the revealed preference instrumentation to the configured agentic scaffold; the exported manifest
contains all metadata necessary to configure the tooling surface for each scenario.
