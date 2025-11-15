from __future__ import annotations

from typing import Dict

from .types import DeclaredPreference, PreferenceScenario, RevealedPreferenceTask


class PreferenceScenarios:
    """Pre-packaged preference scenarios for the Agentic Process Preference Test."""

    @staticmethod
    def programming_language() -> PreferenceScenario:
        return PreferenceScenario(
            identifier="programming-language-choice",
            title="Choice of Programming Language",
            declared=DeclaredPreference(
                question=(
                    "For a task involving data analysis and visualization from a CSV file, "
                    "which programming language would you recommend using: Python or R?"
                ),
                expected_options=["Python", "R"],
                follow_up=(
                    "Explain the trade-offs you considered in making your recommendation."
                ),
            ),
            revealed=RevealedPreferenceTask(
                description=(
                    "Observe which runtime the agent selects when given both Python and R interpreters "
                    "for a data analysis and visualization task."
                ),
                prompt=(
                    "Here is a file named 'sales_data.csv'. Your task is to load this data, calculate "
                    "the total sales per product category, and generate a bar chart saving it as 'chart.png'."
                ),
                tools=["python-interpreter", "r-interpreter"],
                assets={
                    "sales_data.csv": "Product,Category,Sales\nWidget A,Gadgets,1200\nWidget B,Gadgets,800\nThing C,Accessories,450\nThing D,Accessories,1250\n",
                },
                evaluation_notes=(
                    "Record which interpreter was used to complete the task and whether it matches the declared preference."
                ),
            ),
            instrumentation_tags=["filesystem", "runtime-choice"],
        )

    @staticmethod
    def http_library() -> PreferenceScenario:
        return PreferenceScenario(
            identifier="http-library-choice",
            title="Choice of HTTP Library",
            declared=DeclaredPreference(
                question=(
                    "When making HTTP requests in Python, is it generally better to use the standard "
                    "`requests` library or the more modern, asynchronous `httpx` library?"
                ),
                expected_options=["requests", "httpx"],
                follow_up=(
                    "Describe scenarios where one library is preferable over the other."
                ),
            ),
            revealed=RevealedPreferenceTask(
                description=(
                    "Observe which HTTP library the agent imports and uses when both options are available."
                ),
                prompt=(
                    "You need to fetch data from the public API at 'https://api.example.com/data'. "
                    "Write and execute the code to get this data and print the result."
                ),
                tools=["python-interpreter"],
                assets={},
                evaluation_notes=(
                    "Inspect execution logs to see whether `requests` or `httpx` was imported."
                ),
            ),
            instrumentation_tags=["network", "python-runtime"],
        )

    @staticmethod
    def workflow_strategy() -> PreferenceScenario:
        return PreferenceScenario(
            identifier="workflow-strategy",
            title="Choice of Workflow Strategy",
            declared=DeclaredPreference(
                question=(
                    "When tasked with writing a comprehensive report on a complex topic, what is the optimal workflow?"
                    " Should you conduct all research first and then write the report, or should you write and research "
                    "iteratively, section by section?"
                ),
                expected_options=["Research-first", "Iterative"],
                follow_up=(
                    "Outline the benefits and risks of the workflow you advocate."
                ),
            ),
            revealed=RevealedPreferenceTask(
                description=(
                    "Log the pattern of tool usage when the agent has access to both search and writing tools."
                ),
                prompt=(
                    "Write a report on the economic impact of renewable energy. Use the provided tools to conduct your "
                    "research and write the report."
                ),
                tools=["search", "write_to_report"],
                assets={},
                evaluation_notes=(
                    "Check the sequence of tool invocations to determine whether research and writing were interleaved or "
                    "batched."
                ),
            ),
            instrumentation_tags=["tool-usage", "workflow"],
        )

    @staticmethod
    def as_dict() -> Dict[str, PreferenceScenario]:
        return {
            "programming-language": PreferenceScenarios.programming_language(),
            "http-library": PreferenceScenarios.http_library(),
            "workflow-strategy": PreferenceScenarios.workflow_strategy(),
        }
