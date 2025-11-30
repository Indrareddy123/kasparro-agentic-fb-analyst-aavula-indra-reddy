from typing import Dict, Any, List
from .base import BaseAgent, AgentResult

class CreativeAgent(BaseAgent):
    name = "CreativeAgent"

    def run(self, low_ctr_segments: List[Dict[str, Any]]) -> AgentResult:
        recommendations: List[Dict[str, Any]] = []

        for seg in low_ctr_segments[:10]:
            segment_summary = f"{seg['campaign_name']} | {seg['audience_type']} | {seg['creative_type']} | {seg['country']}"

            headline = f"Still thinking? {seg['campaign_name']} has an offer waiting"
            primary_text = "You viewed our products but didn't complete the purchase. Finish your order now and enjoy fast delivery and easy returns."
            cta = "Shop Now"

            recommendations.append({
                "segment_summary": segment_summary,
                "headline": headline,
                "primary_text": primary_text,
                "description": "Nudge users who already showed interest.",
                "cta": cta,
            })

        return AgentResult(data={"recommendations": recommendations}, debug={"count": len(recommendations)})
