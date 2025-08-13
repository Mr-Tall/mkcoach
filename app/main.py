"""
Run locally:
  1) pip install -r requirements.txt
  2) Install Ollama: https://ollama.com/
  3) Pull a model once (in terminal): `ollama run llama3.1`  (or `qwen2.5:3b-instruct`)
  4) streamlit run app/main.py
"""

import streamlit as st
from app.ui import sidebar, chat_input, render_sources
from app.llm_local import OllamaLLM
from app.coach import Coach
from app.memory import log_event, load_state

st.set_page_config(page_title="ComboCoach MK", page_icon="🕹️")

character, persona_mode, belt, show_sources = sidebar()

# Persist a coach per character selection
if "coach" not in st.session_state:
    st.session_state.coach = Coach(llm=OllamaLLM(), character=character)

if st.session_state.coach.character != character:
    st.session_state.coach = Coach(llm=OllamaLLM(), character=character)

st.title("ComboCoach MK")
state = load_state()
st.caption(f"Tactical Tutor with GameSense — data‑grounded coaching | Your Belt: {state.get('belt','White')} | XP: {state.get('xp',0)}")

if "history" not in st.session_state:
    st.session_state.history = []

# Render chat history
for role, content in st.session_state.history:
    with st.chat_message(role):
        st.markdown(content)

msg = chat_input()
if msg:
    st.session_state.history.append(("user", msg))
    with st.chat_message("user"):
        st.markdown(msg)

    reply, retrieved = st.session_state.coach.respond(msg)

    # basic success heuristic for progress (tweak per need)
    success = True
    info = log_event(intent="auto", prompt=msg, success=success)

    st.session_state.history.append(("assistant", reply))
    with st.chat_message("assistant"):
        st.markdown(reply)
        if show_sources:
            render_sources(retrieved)
