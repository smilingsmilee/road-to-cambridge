import streamlit as st
from views.landing import *
from views.home import *

def main():
    st.set_page_config(page_title="JMCalendar", page_icon=":house:")
    
    if "page" not in st.session_state:
        st.session_state.page = "landing"
        
    pages = {
        "landing": landing_page,
        "HS1502 Conceptual Introduction to Machine Learning": hs1502_page,
        "CS3244 Machine Learning": cs3244_page,
        "MA3270 Mathematics for Artificial Intelligence": ma3270_page,
        "MA4207 Mathematical Logic": ma4207_page,
        "MA4262 Measure and Integration": ma4262_page,
        "MA4266 Introduction to Algebraic Topology": ma4266_page
    }
    page = pages.get(st.session_state.page)
    if page:
        page()
    else:
        st.error(f"Unknown page: {st.session_state.page}")

if __name__ == "__main__":
    main()