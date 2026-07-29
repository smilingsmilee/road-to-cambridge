import streamlit as st
from modules import modules

def landing_page():
    st.title("Road to Cambridge")
    st.markdown("Select module")

    for code, title in modules.items():
        if st.button(f"{code} {title}"):
            st.session_state.page = code
            st.rerun()