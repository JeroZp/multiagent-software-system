import os
import json

BASE_DIR = "runs"

def create_run_folder(run_id: str):
    path = os.path.join(BASE_DIR, run_id)
    os.makedirs(path, exist_ok=True)
    return path


def save_text(run_id: str, filename: str, content: str):
    path = os.path.join(BASE_DIR, run_id, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def save_json(run_id: str, filename: str, data: dict):
    path = os.path.join(BASE_DIR, run_id, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)