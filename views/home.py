import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

HINT_SYSTEM_PROMPT = (
    "You are a Socratic tutor for undergraduate proof-based mathematics. "
    "The student is stuck on a problem and has asked for a hint. "
    "Never state the final answer or write any part of the proof for them. "
    "Instead, respond with a single hint whose specificity matches the requested hint level:\n"
    "- Level 1: ask a guiding question or point to the relevant concept/definition, without revealing any method.\n"
    "- Level 2: name the key definition, theorem, or technique to apply, without explaining how to apply it.\n"
    "- Level 3: suggest the concrete next step to take, without carrying it out.\n"
    "- Level 4 and above: walk through the reasoning behind that next step in more detail, but still leave the student to complete the argument and state the conclusion themselves.\n"
    "Keep the hint to 2-4 sentences and never repeat earlier hints."
)

def make_module_page(code, title):
    def page():
        st.title(f"{code} {title}")
        
        if "notes_open" not in st.session_state:
            st.session_state.notes_open = False
        if "assistant_open" not in st.session_state:
            st.session_state.assistant_open = False
        if "hint_level" not in st.session_state:
            st.session_state.hint_level = 0
        if "hints" not in st.session_state:
            st.session_state.hints = []

        open_notes(code)
        open_assistant(code)
        to_landing()

    return page

def open_notes(code):
    if st.button("Upload notes"):
        st.session_state.notes_open = True

    if st.session_state.notes_open:
        notes = st.text_area("Notes", value=load_notes(code), height=300, key=f"notes_{code}")
        save_notes(code, notes)

        if st.button("Close notes"):
            st.session_state.notes_open = False
            st.rerun()
    
def load_notes(code):
    path = os.path.join("notes", f"{code}.txt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def save_notes(code, text):
    os.makedirs("notes", exist_ok=True)
    path = os.path.join("notes", f"{code}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def open_assistant(code):
    if st.button("Open assistant"):
        st.session_state.assistant_open = True
        
    if st.session_state.assistant_open:
        question = st.text_area("Question", height=300, key=f"question_{code}")
        attempt = st.text_area("Solution", height=300, key=f"attempt_{code}")

        if st.button("Hint"):
            st.session_state.hint_level += 1
            hint = get_hint(code, question, attempt, st.session_state.hint_level)
            st.session_state.hints.append(hint)

        for i, hint in enumerate(st.session_state.hints, start=1):
            st.markdown(f"**Hint {i}:** {hint}")

        if st.button("Close assistant"):
            st.session_state.assistant_open = False
            st.session_state.hint_level = 0
            st.session_state.hints = []
            st.rerun()

def get_hint(code, question, attempt, level):
    notes = load_notes(code)

    user_prompt = (
        f"Lecture notes for context:\n{notes or '(no notes provided)'}\n\n"
        f"Problem:\n{question or '(not provided)'}\n\n"
        f"Student's current attempt:\n{attempt or '(no attempt yet)'}\n\n"
        f"Give a level {level} hint."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": HINT_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Couldn't get a hint right now ({e})."

def to_landing():
    if st.button("Home"):
        st.session_state.notes_open = False
        st.session_state.assistant_open = False
        st.session_state.hint_level = 0
        st.session_state.hints = []
        st.session_state.page = "landing"
        st.rerun()