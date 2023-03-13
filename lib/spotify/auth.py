import requests

import spotipy as spotipy
from spotipy.oauth2 import SpotifyOAuth
import xbmcgui
import xbmc

from spotify import settings
from spotify.utils import log


class CodeAuth(SpotifyOAuth):

    @staticmethod
    def _get_user_input(prompt):
        client_id = settings.CLIENT_ID
        client_secret = settings.CLIENT_SECRET
        scope = settings.SCOPE
        response = requests.post(f'{settings.OAUTH_URL}initialize',json={
            'client_id': client_id,
            'client_secret': client_secret,
            'scope': scope,
        })
        data = response.json()
        log(data)
        shortcode = data['code']

        prompt = f'Go to {settings.OAUTH_URL}{shortcode}'
        shortcode = xbmcgui.Dialog().input(heading=prompt, type=xbmcgui.INPUT_ALPHANUM, autoclose=0)
        log(f'Got text input {shortcode}')

        response = requests.get(f'{settings.OAUTH_URL}code/{shortcode}')
        code = response.json()['code']
        log(f'Got token {code}')

        return f'{settings.OAUTH_URL}?code={code}'
