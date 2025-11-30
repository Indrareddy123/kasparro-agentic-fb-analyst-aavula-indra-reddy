from typing import Dict, Any
from .base import BaseAgent, AgentResult

class PlannerAgent(BaseAgent):
    name = "PlannerAgent"

    def run(self, user_query: str, dataset_description: Dict[str, Any]) -> AgentResult:
        plan = {
            "intent": "diagnose_roas_change",
            "data_requirements": {
                "group_bys": ["campaign_name", "adset_name", "audience_type", "country", "creative_type"],
                "metrics": ["roas", "ctr", "impressions", "spend", "purchases", "revenue"],
            },
            "analysis_plan": [
                {"step": 1, "agent": "DataAgent", "action": "summarize"},
                {"step": 2, "agent": "InsightAgent", "action": "generate_simple_hypotheses"},
                {"step": 3, "agent": "EvaluatorAgent", "action": "compute_confidence"},
                {"step": 4, "agent": "CreativeAgent", "action": "suggest_creatives_for_low_ctr"},
            ],
        }
        return AgentResult(data=plan, debug={"user_query": user_query, "dataset": dataset_description})
