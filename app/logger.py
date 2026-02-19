import json
import os
from datetime import datetime


def log_event(run_id: str, agent: str, stage: str, message: str):

    log_path = f"runs/{run_id}/log.json"

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "agent": agent,
        "stage": stage,
        "message": message
    }

    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open(log_path, "w") as f:
        json.dump(data, f, indent=2)
