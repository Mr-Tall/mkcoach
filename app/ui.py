import streamlit as st
from typing import List, Dict


def sidebar():
    st.sidebar.header("ComboCoach MK")
    character = st.sidebar.selectbox("Character", ["Johnny Cage","Scorpion","Sub-Zero"], index=0)
    persona_mode = st.sidebar.checkbox("Use Persona Voice", value=True)
    st.sidebar.divider()
    belt = st.sidebar.selectbox("Your Belt", ["White","Yellow","Green","Blue","Purple","Brown","Black"], index=0)
    show_sources = st.sidebar.checkbox("Show Sources", value=True)
    return character, persona_mode, belt, show_sources


def chat_input():
    return st.chat_input("Ask for a combo, punish, or drill... e.g., 'What punishes -12 in corner?'")


def render_sources(items: List[Dict]):
    with st.expander("Sources / Retrieved context"):
        for r in items:
            st.markdown(f"- {r.get('text')}")
