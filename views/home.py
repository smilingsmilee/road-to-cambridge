import os
import streamlit as st

def make_module_page(code, title):
    def page():
        st.title(f"{code} {title}")
        
        if "notes_open" not in st.session_state:
            st.session_state.notes_open = False
        if "assistant_open" not in st.session_state:
            st.session_state.assistant_open = False

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

        if st.button("Close assistant"):
            st.session_state.assistant_open = False
            st.rerun()

def to_landing():
    if st.button("Home"):
        st.session_state.notes_open = False
        st.session_state.assistant_open = False
        st.session_state.page = "landing"
        st.rerun()