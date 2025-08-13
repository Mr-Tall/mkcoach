from app.llm_local import OllamaLLM
from app.coach import Coach

if __name__ == "__main__":
    coach = Coach(llm=OllamaLLM(), character="Johnny Cage")
    reply, ctx = coach.respond("What punishes -14 on block?")
    print("CTX:", ctx[:2])
    print("REPLY:\n", reply)
