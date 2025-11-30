from typing import Dict, Any, List
from .base import BaseAgent, AgentResult

class InsightAgent(BaseAgent):
    name = "InsightAgent"

    def run(self, data_summary: Dict[str, Any]) -> AgentResult:
        cur = data_summary["current_summary"]
        base = data_summary["baseline_summary"]
        hypotheses: List[Dict[str, Any]] = []

        if not cur or not base:
            return AgentResult(data={"hypotheses": []}, debug={"reason": "no_data"})

        # Simple heuristic: compare ROAS of first segment
        cur_seg = cur[0]
        base_seg = base[0]

        if base_seg["roas"] > 0:
            roas_delta = (cur_seg["roas"] - base_seg["roas"]) / base_seg["roas"]
        else:
            roas_delta = 0

        hypotheses.append({
            "id": "H1",
            "description": "ROAS dropped for main campaign segment.",
            "segment_filter": {
                "campaign_name": cur_seg["campaign_name"],
                "country": cur_seg["country"],
            },
            "rationale": "Comparing current vs baseline ROAS for key segment.",
            "estimated_roas_delta": roas_delta,
        })

        return AgentResult(data={"hypotheses": hypotheses}, debug={"count": len(hypotheses)})
