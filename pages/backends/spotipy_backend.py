import pandas as pd

import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

import requests
from PIL import Image
from io import BytesIO

if 'SPOTIPY_CLIENT_ID' not in st.session_state:
    SPOTIPY_CLIENT_ID = st.secrets['SPOTIPY_CLIENT_ID']
    SPOTIPY_CLIENT_SECRET = st.secrets['SPOTIPY_CLIENT_SECRET']
    SPOTIFY_REDIRECT_URI = 'https://neunai.streamlit.app/authentication-success/'
    SPOTIFY_SCOPE = 'user-library-read'

    auth_manager = None
    sp = spotipy.Spotify()


def authorize():
    global auth_manager, sp

    try:
        auth_manager = SpotifyOAuth(client_id=SPOTIPY_CLIENT_SECRET,
                                    client_secret=SPOTIPY_CLIENT_SECRET,
                                    scope=SPOTIFY_SCOPE,
                                    redirect_uri=SPOTIFY_REDIRECT_URI,
                                    open_browser=False)
        return auth_manager.get_authorize_url()

    except (spotipy.SpotifyException, spotipy.SpotifyOauthError):
        return None


def get_image_data_from_track_id(track_id):
    global sp
    try:
        track = sp.track(track_id)
        image_url = track['album']['images'][0]['url']
        response = requests.get(image_url)
        content = response.content
        pil = Image.open(BytesIO(content))
        image_df = pd.DataFrame({'album_image': [pil]})
        return image_df
    except spotipy.SpotifyException as e:
        return None


def get_external_url_from_track_id(track_id):
    global sp
    try:
        track = sp.track(track_id)
        external_url = track['external_urls']['spotify']
        external_url_df = pd.DataFrame({'external_url': [external_url]})
        return external_url_df
    except spotipy.SpotifyException as e:
        return None


def init_spotify():
    global sp
    sp = spotipy.Spotify(auth_manager=auth_manager)
