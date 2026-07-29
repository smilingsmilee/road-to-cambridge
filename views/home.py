import streamlit as st

def hs1502_page():
    st.title("HS1502 Conceptual Introduction to Machine Learning")
    to_landing()

def cs3244_page():
    st.title("CS3244 Machine Learning")
    to_landing()

def ma3270_page():
    st.title("MA3270 Mathematics for Artificial Intelligence")
    to_landing()

def ma4207_page():
    st.title("MA4207 Mathematical Logic")
    to_landing()

def ma4262_page():
    st.title("MA4262 Measure and Integration")
    to_landing()

def ma4266_page():
    st.title("MA4266 Introduction to Algebraic Topology")
    to_landing()

def to_landing():
    if st.button("Home"):
        st.session_state.page = "landing"