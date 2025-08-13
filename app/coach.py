import os, re
from typing import Tuple, List, Dict
from app.embeddings import RAGIndex
from app.routing import route_intent
from app.tools import lookup_frame_data, recommend_punish, design_drill

SYSTEM_BASE = """You are ComboCoach MK, a factual, clipped fighting-game coach.
Rules:
- Always ground advice in retrieved frame data (quote numbers).
- If recommending a punish, ensure startup ≤ opponent on-block disadvantage.
- If uncertain, ask a clarifying question or assign a quick drill.
- Keep answers compact and actionable.
"""


def load_persona(character: str) -> str:
    path = f"personas/{character.lower().replace(' ', '_')}.md"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return "Voice: neutral. Tactics: concise."


class Coach:
    def __init__(self, llm, character: str = "Johnny Cage"):
        self.rag = RAGIndex()
        self.llm = llm         # any chat() -> str interface (OllamaLLM)
        self.character = character
        self.persona = load_persona(character)

    def _prompt(self, user: str, retrieved: List[Dict]) -> str:
        ctx = "\n".join([f"- {r['text']}" for r in retrieved])
        return (
            SYSTEM_BASE
            + "\nPersona:\n" + self.persona
            + f"\n\nContext:\n{ctx}\n\nUser: {user}\nCoach:"
        )

    def respond(self, user_text: str) -> Tuple[str, List[Dict]]:
        intent = route_intent(user_text)
        retrieved = self.rag.search(user_text, k=6)

        # Tool hooks for determinism
        if intent == "punish":
            m = re.search(r"-(\d+)", user_text)
            if m:
                window = int(m.group(1))
                moves = recommend_punish(self.character, -window)
                if moves:
                    top = [f"{mv['name']} ({mv['startup']}f, on block {mv.get('on_block','?')})" for mv in moves]
                    deterministic = f"Recommended punishes ≤ {window}f: " + ", ".join(top)
                    retrieved.insert(0, {"text": deterministic, "meta": {"type":"tool"}, "score": 1.0})

        if intent == "drill":
            drill = design_drill(self.character)
            retrieved.insert(0, {"text": f"DRILL: {drill['title']} | Goal: {drill['goal']} | Checklist: {drill['checklist']}", "meta": {"type":"tool"}, "score": 1.0})

        prompt = self._prompt(user_text, retrieved)
        reply = self.llm.chat(prompt)
        return reply, retrieved
