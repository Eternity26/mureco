import streamlit as st

if 'hide_sidebar' not in st.session_state:
    st.session_state.hide_sidebar = True


def apply():
    hide_sidebar()


def hide_sidebar():
    st.markdown('''<style>[data-testid="stSidebar"]{display: none;}</style>''', unsafe_allow_html=True)
