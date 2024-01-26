import streamlit as st

# noinspection PyTypeChecker
st.set_page_config(page_title='authentication success - neunai',
                   page_icon=':check_mark:',
                   layout='centered',
                   menu_items={
                       'Get Help': None,
                       'Report a bug': None,
                       'About': 'K. Wong'
                   }
                   )

exec(open("pages/page_setting/setting.py").read())

from streamlit_extras.switch_page_button import switch_page

import time

# get authentication code to send it to home by redirection
if 'code' not in st.session_state:
    st.session_state['code'] = st.query_params['code']

# return home
if 'authentication_passed_sec' not in st.session_state:
    st.session_state['authentication_passed_sec'] = 0

st.success(f'Authentication succeeded! Return home in {5 - st.session_state["authentication_passed_sec"]} seconds.')
time.sleep(1.0)
return_progress = st.progress(value=st.session_state['authentication_passed_sec'] / 5.0)

if st.session_state['authentication_passed_sec'] <= 5:
    st.session_state['authentication_passed_sec'] += 1
    st.rerun()

switch_page('home')
