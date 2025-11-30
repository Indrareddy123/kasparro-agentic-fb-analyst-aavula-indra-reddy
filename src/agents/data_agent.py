from typing import Dict, Any
from .base import BaseAgent, AgentResult
from ..utils import data_utils

class DataAgent(BaseAgent):
    name = "DataAgent"

    def __init__(self, cfg: Dict[str, Any], date_col: str):
        super().__init__(cfg)
        self.date_col = date_col

    def run(self, df, plan: Dict[str, Any]) -> AgentResult:
        windows = data_utils.compute_time_windows(df, self.date_col, self.cfg["analysis"])
        current = df[(df[self.date_col] >= windows["current"]["start"]) &
                     (df[self.date_col] <= windows["current"]["end"])]
        baseline = df[(df[self.date_col] >= windows["baseline"]["start"]) &
                      (df[self.date_col] <= windows["baseline"]["end"])]

        group_bys = plan["data_requirements"]["group_bys"]
        cur_summary = data_utils.summarize_by_segment(current, group_bys)
        base_summary = data_utils.summarize_by_segment(baseline, group_bys)

        low_ctr = cur_summary[
            (cur_summary["ctr"] < self.cfg["metrics"]["ctr_low_threshold"]) &
            (cur_summary["impressions"] >= self.cfg["metrics"]["min_impressions_for_analysis"])
        ]

        data = {
            "time_windows": {
                "current": {"start": str(windows["current"]["start"]), "end": str(windows["current"]["end"])},
                "baseline": {"start": str(windows["baseline"]["start"]), "end": str(windows["baseline"]["end"])},
            },
            "current_summary": cur_summary.to_dict(orient="records"),
            "baseline_summary": base_summary.to_dict(orient="records"),
            "low_ctr_segments": low_ctr.to_dict(orient="records"),
        }
        return AgentResult(data=data, debug={"n_current": len(current), "n_baseline": len(baseline)})
