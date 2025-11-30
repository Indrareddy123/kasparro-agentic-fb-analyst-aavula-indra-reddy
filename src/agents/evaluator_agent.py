from typing import Dict, Any, List
import pandas as pd
from .base import BaseAgent, AgentResult

class EvaluatorAgent(BaseAgent):
    name = "EvaluatorAgent"

    def __init__(self, cfg: Dict[str, Any], date_col: str):
        super().__init__(cfg)
        self.date_col = date_col

    def run(self, df: pd.DataFrame, hypotheses: Dict[str, Any], data_summary: Dict[str, Any]) -> AgentResult:
        windows = data_summary["time_windows"]
        cur_start = pd.to_datetime(windows["current"]["start"])
        cur_end = pd.to_datetime(windows["current"]["end"])
        base_start = pd.to_datetime(windows["baseline"]["start"])
        base_end = pd.to_datetime(windows["baseline"]["end"])

        evaluated: List[Dict[str, Any]] = []

        for hyp in hypotheses.get("hypotheses", []):
            seg = hyp.get("segment_filter", {})

            mask = (df[self.date_col] >= base_start) & (df[self.date_col] <= cur_end)
            for k, v in seg.items():
                mask &= (df[k] == v)

            seg_df = df[mask]

            cur_df = seg_df[(seg_df[self.date_col] >= cur_start) & (seg_df[self.date_col] <= cur_end)]
            base_df = seg_df[(seg_df[self.date_col] >= base_start) & (seg_df[self.date_col] <= base_end)]

            def agg(d: pd.DataFrame):
                spend = d["spend"].sum()
                revenue = d["revenue"].sum()
                clicks = d["clicks"].sum()
                impressions = d["impressions"].sum()
                return {
                    "spend": spend,
                    "revenue": revenue,
                    "clicks": clicks,
                    "impressions": impressions,
                    "roas": (revenue / spend) if spend > 0 else 0,
                    "ctr": (clicks / impressions) if impressions > 0 else 0,
                }

            cur_m = agg(cur_df)
            base_m = agg(base_df)

            def pct(a, b):
                if b == 0:
                    return None
                return (a - b) / b

            roas_delta = pct(cur_m["roas"], base_m["roas"])

            confidence = 0.3
            status = "not_supported"
            thr = self.cfg["metrics"]["roas_drop_threshold"]

            if roas_delta is not None:
                if roas_delta <= -thr:
                    confidence = 0.8
                    status = "supported"
                elif abs(roas_delta) < thr / 2:
                    confidence = 0.5
                    status = "partially_supported"

            evaluated.append({
                "id": hyp["id"],
                "description": hyp["description"],
                "segment_filter": seg,
                "rationale": hyp["rationale"],
                "metrics_evidence": {
                    "current": cur_m,
                    "baseline": base_m,
                    "delta": {"roas": roas_delta},
                },
                "status": status,
                "confidence": confidence,
            })

        return AgentResult(data={"evaluated_hypotheses": evaluated}, debug={"count": len(evaluated)})
