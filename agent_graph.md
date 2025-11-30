\# Agent Graph – Kasparro Agentic FB Analyst



```mermaid

flowchart TD

&nbsp;   U\[User Query] --> P\[Planner Agent]

&nbsp;   P --> D\[Data Agent]

&nbsp;   D --> I\[Insight Agent]

&nbsp;   I --> E\[Evaluator Agent]

&nbsp;   D --> C\[Creative Agent]

&nbsp;   E --> R\[Report Builder]

&nbsp;   C --> R

&nbsp;   R --> OUT\[(insights.json, creatives.json, report.md)]



