import re

INTENTS = {
    "punish": r"(punish|on block|unsafe|-\d+)",
    "combo": r"(combo|route|bnb|meterless|corner)",
    "frame": r"(startup|on block|frames|gap)",
    "drill": r"(quiz|drill|test|sparring|practice)"
}


def route_intent(text: str) -> str:
    text_l = text.lower()
    for name, pat in INTENTS.items():
        if re.search(pat, text_l):
            return name
    return "chat"
