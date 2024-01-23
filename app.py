import pandas as pd
import streamlit as st

from recommendation_backend import get_data_with_info, get_track_info_list, get_id_by_info, \
    get_info_by_id, get_recommendation_ids
from spotipy_backend import authorize, get_image_data_from_track_id

data_with_info = get_data_with_info()
track_info_list = get_track_info_list()

authorized = False

# side bar, get album image from id using spotipy
with st.sidebar:
    st.title('Spotify Authorization')

    st.divider()

    st.write('If no detail is given, image will not be included in the recommendation result. However, '
             'the information can still be displayed the format: ')
    st.caption('''artists - track_name | from album_name''')

    SPOTIFY_USERNAME = st.text_input('User Name')
    SPOTIFY_CLIENT_ID = st.text_input('Client ID')
    SPOTIFY_CLIENT_SECRET = st.text_input('Client Secret')

    auth_manager = None

    if st.button('Authorize'):
        if authorize(SPOTIFY_USERNAME, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET):
            authorized = True
            st.success('Authorization Succeeded!')

        else:
            st.error('Authorization failed. Please fill all fields correctly or check your network.')

# body
st.title('Music Recommendation System')

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
                if authorized:
                    if get_image_data_from_track_id(recommendation_id):
                        recommendation_image = get_image_data_from_track_id(recommendation_id)
                        recommendation_info = pd.concat([recommendation_image, recommendation_info], axis=1)
                st.write(recommendation_info)
