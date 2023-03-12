import requests

import spotipy as spotipy
from spotipy.oauth2 import SpotifyOAuth
import xbmcgui
import xbmc

from spotify import settings


class CodeAuth(SpotifyOAuth):

    @staticmethod
    def _get_user_input(prompt):
        client_id = settings.CLIENT_ID
        client_secret = settings.CLIENT_SECRET
        scope = settings.SCOPE
        response = requests.post(f'{settings.OAUTH_URL}code',json={
            'client_id': client_id,
            'client_secret': client_secret,
            'scope': scope,
        })
        code = response.json()['code']
        prompt = f'Go to {settings.OAUTH_URL}code/{code}'
        code = xbmcgui.Dialog().input(heading=prompt, type=xbmcgui.INPUT_ALPHANUM, autoclose=0)
        xbmc.log(f'Got text input {code}', xbmc.LOGINFO)
        response = requests.get(f'{settings.OAUTH_URL}token/{code}')
        token = response.json()['token']
        xbmc.log(f'Got token {token}', xbmc.LOGINFO)
        return f'{settings.OAUTH_URL}?code={token}'
