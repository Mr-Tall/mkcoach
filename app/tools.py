import json, os
from typing import List, Dict, Optional

DATA_DIR = "data/frame_data"


def _char_path(character: str) -> str:
    return os.path.join(DATA_DIR, f"{character.lower().replace(' ', '_')}.json")


def load_character_moves(character: str) -> List[Dict]:
    path = _char_path(character)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("moves", [])


def lookup_frame_data(character: str, move_name: str) -> Optional[Dict]:
    for m in load_character_moves(character):
        if m.get("name", "").lower() == move_name.lower():
            return m
    return None


def recommend_punish(my_char: str, opp_on_block: int) -> List[Dict]:
    """Return moves from my_char with startup <= abs(opp_on_block)."""
    window = abs(int(opp_on_block))
    moves = [m for m in load_character_moves(my_char) if isinstance(m.get("startup"), int)]
    candidates = [m for m in moves if m["startup"] <= window]
    candidates.sort(key=lambda m: (m.get("startup", 99), m.get("type", "z")))
    return candidates[:5]


def design_drill(my_char: str, weakness: str = "anti-teleport") -> Dict:
    if "teleport" in weakness:
        return {
            "title": "Teleport Punish Reps",
            "goal": "Identify and recite 2 punishes for -14 on block",
            "checklist": [
                "Name two starters ≤ 14f",
                "Describe your confirm route",
                "Explain spacing caveat"
            ],
            "pass_condition": "User lists 2 valid starters and a route"
        }
    return {
        "title": "Custom Drill",
        "goal": "State one safe poke",
        "checklist": ["Name poke ≤ -3"],
        "pass_condition": "One valid poke"
    }
