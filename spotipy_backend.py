import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth

import requests
from PIL import Image
from io import BytesIO

SPOTIFY_REDIRECT_URI = 'https://music-recommendation-system.streamlit.app/#/'
SPOTIFY_SCOPE = 'user-library-read'

auth_manager = None
sp = spotipy.Spotify()


def authorize(spotify_username, spotify_client_id, spotify_client_secret):
    global auth_manager, sp

    try:
        auth_manager = SpotifyOAuth(client_id=spotify_client_id,
                                    client_secret=spotify_client_secret,
                                    scope=SPOTIFY_SCOPE,
                                    username=spotify_username,
                                    redirect_uri=SPOTIFY_REDIRECT_URI)
        sp = spotipy.Spotify(auth_manager=auth_manager)

        if not auth_manager or not sp:
            return False
        return True

    except (spotipy.SpotifyException, spotipy.SpotifyOauthError):
        return False


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


def test_authorization():
    sp.search('')
