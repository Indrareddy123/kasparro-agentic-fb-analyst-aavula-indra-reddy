from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class AgentResult:
    data: Dict[str, Any]
    debug: Dict[str, Any]

class BaseAgent:
    name: str = "BaseAgent"

    def __init__(self, cfg: Dict[str, Any]):
        self.cfg = cfg

    def run(self, *args, **kwargs) -> AgentResult:
        raise NotImplementedError
