import streamlit as st

# noinspection PyTypeChecker
st.set_page_config(page_title='Home - Neunai',
                   page_icon=':cow:',
                   layout='wide',
                   menu_items={
                       'Get Help': None,
                       'Report a bug': None,
                       'About': 'K. Wong "Neurofun"'
                   }
                   )

from pages.page_setting import setting

exec(open("pages/page_setting/setting.py").read())

import pandas as pd

from pages.backends.recommendation_backend import get_data_with_info, get_track_info_list, get_id_by_info, \
    get_info_by_id, get_recommendation_ids
from pages.backends.spotipy_backend import authorize, get_image_data_from_track_id, \
    get_external_url_from_track_id

data_with_info = get_data_with_info()
track_info_list = get_track_info_list()

if 'authorize_clicked' not in st.session_state:
    st.session_state.authorize_clicked = False

# body
with st.container():
    col1, col2 = st.columns([1, 2.2], gap='large')

# authorization
with col1:
    with st.container(border=True):
        st.markdown('### Spotify Authorization')

        st.divider()

        with st.container(border=True):
            st.caption(
                'If no detail is given, image will not be included in the recommendation result. However, the information can still be displayed as the format: ')
            with st.container(border=True):
                '''artists - track_name | from album_name'''

        st.divider()

        SPOTIFY_USERNAME = st.text_input('User Name')
        SPOTIFY_CLIENT_ID = st.text_input('Client ID')
        SPOTIFY_CLIENT_SECRET = st.text_input('Client Secret')

        auth_manager = None

        if st.button('Authorize'):
            if authorize(SPOTIFY_USERNAME, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET):
                st.session_state.authorize_clicked = True
                st.info('If you are not directed to a new page, Authorization succeeded. '
                        'Otherwise please fill details in the new page.')

            else:
                st.error('Authorization failed. Please fill all fields correctly or check your network.')

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
