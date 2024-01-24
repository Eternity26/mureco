import streamlit as st
from streamlit_extras.switch_page_button import switch_page


st.markdown('''<style>[data-testid="stSidebar"]{display: none;}</style>''', unsafe_allow_html=True)

switch_page('home')
