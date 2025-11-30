import json
import os
from datetime import datetime
from typing import Dict, Any

def log_event(logs_dir: str, event_type: str, payload: Dict[str, Any]) -> None:
    os.makedirs(logs_dir, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S%f")
    path = os.path.join(logs_dir, f"{ts}_{event_type}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"timestamp_utc": ts, "event_type": event_type, **payload}, f, indent=2, default=str)
