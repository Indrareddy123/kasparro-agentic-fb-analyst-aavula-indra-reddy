import json
import yaml
from typing import Dict, Any
from ..utils.data_utils import load_data
from ..utils.logging_utils import log_event
from ..agents.planner_agent import PlannerAgent
from ..agents.data_agent import DataAgent
from ..agents.insight_agent import InsightAgent
from ..agents.evaluator_agent import EvaluatorAgent
from ..agents.creative_agent import CreativeAgent

def load_config(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def describe_dataset(df, date_col: str) -> Dict[str, Any]:
    return {
        "n_rows": len(df),
        "columns": list(df.columns),
        "date_min": str(df[date_col].min()),
        "date_max": str(df[date_col].max()),
    }

def run_pipeline(user_query: str, config_path: str = "config/config.yaml") -> Dict[str, Any]:
    cfg = load_config(config_path)
    df = load_data(cfg["data"]["path"], cfg["data"]["date_column"], cfg["data"]["date_format"])
    dataset_desc = describe_dataset(df, cfg["data"]["date_column"])

    planner = PlannerAgent(cfg)
    data_agent = DataAgent(cfg, cfg["data"]["date_column"])
    insight_agent = InsightAgent(cfg)
    evaluator = EvaluatorAgent(cfg, cfg["data"]["date_column"])
    creative = CreativeAgent(cfg)

    plan_res = planner.run(user_query, dataset_desc)
    plan = plan_res.data
    log_event(cfg["output"]["logs_dir"], "plan", plan)

    data_res = data_agent.run(df, plan)
    data_summary = data_res.data
    log_event(cfg["output"]["logs_dir"], "data_summary", {"current_len": len(data_summary["current_summary"])})

    insight_res = insight_agent.run(data_summary)
    hypotheses = insight_res.data
    log_event(cfg["output"]["logs_dir"], "hypotheses", hypotheses)

    eval_res = evaluator.run(df, hypotheses, data_summary)
    evaluated = eval_res.data
    log_event(cfg["output"]["logs_dir"], "evaluated_hypotheses", evaluated)

    creative_res = creative.run(data_summary["low_ctr_segments"])
    creatives = creative_res.data
    log_event(cfg["output"]["logs_dir"], "creatives", creatives)

    with open(cfg["output"]["insights_path"], "w", encoding="utf-8") as f:
        json.dump(evaluated, f, indent=2)

    with open(cfg["output"]["creatives_path"], "w", encoding="utf-8") as f:
        json.dump(creatives, f, indent=2)

    with open(cfg["output"]["report_path"], "w", encoding="utf-8") as f:
        f.write("# Facebook ROAS Diagnostic Report\n\n")
        f.write(f"**Query:** {user_query}\n\n")
        f.write("## Validated Hypotheses\n\n")
        for h in evaluated.get("evaluated_hypotheses", []):
            f.write(f"- **[{h['status'].upper()} | {h['confidence']:.2f}]** {h['description']}\n")
            f.write(f"  - ROAS Δ: {h['metrics_evidence']['delta']['roas']}\n")
        f.write("\n## Creative Recommendations\n\n")
        for c in creatives.get("recommendations", [])[:10]:
            f.write(f"- Segment: {c['segment_summary']}\n")
            f.write(f"  - Headline: {c['headline']}\n")
            f.write(f"  - Text: {c['primary_text']}\n")
            f.write(f"  - CTA: {c['cta']}\n\n")

    return {
        "insights_path": cfg["output"]["insights_path"],
        "creatives_path": cfg["output"]["creatives_path"],
        "report_path": cfg["output"]["report_path"],
    }
