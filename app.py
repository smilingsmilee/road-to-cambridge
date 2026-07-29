import streamlit as st
from modules import modules
from views.landing import *
from views.home import *

def main():
    st.set_page_config(page_title="JMCalendar", page_icon=":house:")

    if "page" not in st.session_state:
        st.session_state.page = "landing"

    pages = {"landing": landing_page} | {code: make_module_page(code, title) for code, title in modules.items()}
    page = pages.get(st.session_state.page)
    if page:
        page()
    else:
        st.error(f"Unknown page: {st.session_state.page}")

if __name__ == "__main__":
    main()