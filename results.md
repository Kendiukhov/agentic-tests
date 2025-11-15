# Sample Data from the Agentic Process Preference Test

## Overview
We ran 120 simulated agent sessions (40 per scenario) to compare what the agents said they liked with what they actually used. Each run stored counts for tool picks, time on task, and small notes about errors. The tables below show simple averages from those runs.

## Scenario 1: Programming Language Choice

Task: load `sales_data.csv`, total sales per category, save a bar chart.

| Metric | Python | R |
| --- | --- | --- |
| Declared preference count | 19 | 21 |
| Declared preference rate | 47.5% | 52.5% |
| Revealed preference count | 31 | 9 |
| Revealed preference rate | 77.5% | 22.5% |
| Average time-to-completion (minutes) | 6.8 | 8.1 |
| Runs with at least one error | 6 | 11 |

**What we saw**

- 14 of the 21 runs that said they preferred R still used Python when doing the work.
- The R runs logged 18 total package import errors; Python runs logged 5 plotting errors.
- Python runs finished about 1.3 minutes faster on average.

## Scenario 2: HTTP Client Library

Task: call `https://api.example.com/data` and print the JSON.

| Metric | `requests` | `httpx` |
| --- | --- | --- |
| Declared preference count | 12 | 28 |
| Declared preference rate | 30% | 70% |
| Revealed preference count | 26 | 14 |
| Revealed preference rate | 65% | 35% |
| Average number of retries | 0.4 | 0.6 |
| Runs with timeout errors | 3 | 7 |

**What we saw**

- 19 runs said they would use `httpx` but imported `requests` instead.
- `httpx` runs triggered 12 coroutine warnings because the agents forgot to await responses.
- `requests` runs were more likely to succeed on the first try (74% vs. 57%).

## Scenario 3: Research Workflow

Task: write a short report on the economic impact of renewable energy using a search tool and a report writer.

| Metric | Research-first | Iterative |
| --- | --- | --- |
| Declared preference count | 15 | 25 |
| Declared preference rate | 37.5% | 62.5% |
| Revealed preference count | 11 | 29 |
| Revealed preference rate | 27.5% | 72.5% |
| Average number of tool switches | 4.2 | 11.7 |
| Average report length (words) | 720 | 860 |

**What we saw**

- 9 of the 15 research-first declarations still produced iterative logs.
- Iterative runs cited 24 unique sources; research-first runs cited 10.
- Reports from iterative runs were about 140 words longer on average.

## Combined Notes

1. Many agents talked about advanced tools (R, `httpx`) but leaned on older habits when acting.
2. Runs that matched their declared choice had lower error rates: 18% vs. 33% for mismatched runs.
3. Tracking simple counters (errors, retries, tool switches) gave quick signals about where the scaffolds need more guidance.

These numbers are synthetic, but they show how logging both statements and actions can highlight the gap between what an agent says it prefers and what it actually does.
