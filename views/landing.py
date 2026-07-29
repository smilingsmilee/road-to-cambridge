import streamlit as st

def landing_page():
    st.title("Road to Cambridge")
    st.markdown("Select module")

    for mod in [
        "HS1502 Conceptual Introduction to Machine Learning",
        "CS3244 Machine Learning",
        "MA3270 Mathematics for Artificial Intelligence",
        "MA4207 Mathematical Logic",
        "MA4262 Measure and Integration",
        "MA4266 Introduction to Algebraic Topology"
    ]:
        if st.button(mod):
            st.session_state.page = mod
            st.rerun()