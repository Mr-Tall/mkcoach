import json, os, time
from typing import Dict, Any

PROGRESS_PATH = os.path.join("progress", "user_progress.json")

DEFAULT_STATE = {
    "belt": "White",
    "xp": 0,
    "streak": 0,
    "history": []  # list of {ts, intent, prompt, success}
}


def _ensure_file():
    os.makedirs(os.path.dirname(PROGRESS_PATH), exist_ok=True)
    if not os.path.exists(PROGRESS_PATH):
        with open(PROGRESS_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_STATE, f, indent=2)


def load_state() -> Dict[str, Any]:
    _ensure_file()
    with open(PROGRESS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state: Dict[str, Any]):
    _ensure_file()
    with open(PROGRESS_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def log_event(intent: str, prompt: str, success: bool = True):
    state = load_state()
    state["history"].append({
        "ts": int(time.time()),
        "intent": intent,
        "prompt": prompt,
        "success": success
    })
    # naive xp system
    state["xp"] += 5 if success else 1
    # promote belts at simple thresholds
    thresholds = [0, 20, 50, 90, 140, 200, 280]
    belts = ["White","Yellow","Green","Blue","Purple","Brown","Black"]
    for i, t in reversed(list(enumerate(thresholds))):
        if state["xp"] >= t:
            state["belt"] = belts[i]
            break
    save_state(state)
    return state
