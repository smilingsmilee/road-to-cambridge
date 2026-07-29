import streamlit as st

def make_module_page(code, title):
    def page():
        st.title(f"{code} {title}")
        to_landing()

    return page

def to_landing():
    if st.button("Home"):
        st.session_state.page = "landing"