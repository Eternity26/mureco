import streamlit as st

# noinspection PyTypeChecker
st.set_page_config(page_title='home - neunai',
                   page_icon=':cow:',
                   layout='wide',
                   menu_items={
                       'Get Help': None,
                       'Report a bug': None,
                       'About': 'K. Wong'
                   }
                   )

exec(open("pages/page_setting/setting.py").read())

import pandas as pd

from pages.backends.recommendation_backend import get_data_with_info, get_track_info_list, get_id_by_info, \
    get_info_by_id, get_recommendation_ids
from pages.backends.spotipy_backend import authorize, get_image_data_from_track_id, \
    get_external_url_from_track_id

if 'data_with_info' not in st.session_state:
    st.session_state['data_with_info'] = get_data_with_info()
    st.session_state['track_info_list'] = get_track_info_list()

data_with_info = st.session_state['data_with_info']
track_info_list = st.session_state['track_info_list']

# body
with st.container():
    if 'code' not in st.session_state:
        col1, col2 = st.columns([1, 2.2], gap='large')
    else:
        col2 = st.container()

# authorization
if 'col1' in globals():
    with col1:
        with st.container(border=True):
            st.markdown('### Spotify Authorization')

            st.divider()

            with st.container(border=True):
                st.caption('Login to Spotify to display album images and urls. Otherwise info of recommendations '
                           'will be displayed as:')
                with st.container(border=True):
                    '''artists - track_name | from album_name'''

            st.divider()

            auth_url = authorize()
            if auth_url and len(auth_url) > 0:
                st.link_button(label='Login', url=auth_url)
            else:
                st.error('Authorization failed. Please fill all fields correctly or check your network.')
                if st.button('rerun'):
                    st.rerun()
else:


# recommendation
with col2:
    with st.container(border=True):
        st.title('neunai')

        st.markdown('##### A Music Recommendation System')

        st.divider()

        recommendation_number = st.slider(label='Please choose the number of recommendations:',
                                          value=10, min_value=1, max_value=200, step=1)

        st.divider()

        input_track_info_list = st.multiselect(
            "Please choose a track from dataset of " + str(data_with_info.shape[0]) + " tracks:",
            track_info_list)

        if not input_track_info_list:
            st.error('Please choose at least one track.')
        else:
            input_track_info = input_track_info_list[0]
            input_id = get_id_by_info(input_track_info)

            with st.container(height=350):
                for recommendation_id in get_recommendation_ids(input_id, recommendation_number).values.tolist():
                    with st.container():
                        recommendation_info = get_info_by_id(recommendation_id[0])

                        if st.session_state.authorize_clicked:
                            if get_image_data_from_track_id(recommendation_id[0]):
                                recommendation_image = get_image_data_from_track_id(recommendation_id)
                                recommendation_info = pd.concat([recommendation_image, recommendation_info], axis=1)

                            if get_external_url_from_track_id(recommendation_id[0]):
                                recommendation_external_url = get_external_url_from_track_id(recommendation_id)
                                recommendation_info = pd.concat([recommendation_info, recommendation_external_url],
                                                                axis=1)

                        recommendation_info
