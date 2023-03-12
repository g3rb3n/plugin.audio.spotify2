import spotipy as spotipy
from spotipy.oauth2 import SpotifyPKCE
from spotipy.cache_handler import CacheFileHandler, CacheHandler

from spotify import settings
from spotify.auth import CodeAuth


ADDON_ID = settings.ADDON_ID
BASE_URL = settings.BASE_URL
ADDON_HANDLE = settings.ADDON_HANDLE


class Client():

    def __init__(self, config):
        auth_manager=CodeAuth(
            client_id=config.client_id,
            client_secret=config.client_secret,
            redirect_uri=f'{settings.OAUTH_URL}callback',
            username=config['username'],
            scope=settings.SCOPE,
            open_browser=False,
            cache_handler=CacheFileHandler(cache_path=settings.OAUTH_CACHE_FILE)
        )
        self.spotify = spotipy.Spotify(
            auth_manager=auth_manager
        )

    def top_artists(self, num):
        artists = []
        while len(artists) < num:
            artists.extend(self.spotify.current_user_top_artists(limit=20, offset=len(artists))['items'])
        return artists

    def get_user_playlists(self, userid):
        playlists = []
        total = 1
        while len(playlists) < total:
            result = self.spotify.user_playlists(userid, limit=50, offset=len(playlists))
            total = result['total']
            playlists.extend(result['items'])
        return playlists

    def user_playlist(self, ownerid, playlistid, market):
        playlist = self.spotify.user_playlist(ownerid, playlistid, market=market, fields='tracks(total),name,owner(id),id')
        return playlist

    def user_playlist_tracks(self, ownerid, playlistid, count, market):
        tracks = []
        while len(tracks) < count:
            items = self.spotify.user_playlist_tracks(ownerid, playlistid, market=market, fields='', limit=50, offset=len(tracks))['items']
            if len(items) == 0:
                break
            tracks.extend(items)
        return tracks

    def current_user_saved_tracks(self):
        saved_tracks = []
        total = 1
        while len(saved_tracks) < total:
            result = self.spotify.current_user_saved_tracks(limit=50, offset=len(saved_tracks))
            total = result['total']
            saved_tracks.extend(result['items'])
        return saved_tracks

    def current_user_saved_albums(self):
        items = []
        total = 1
        while len(items) < total:
            result = self.spotify.current_user_saved_albums(limit=50, offset=len(items))
            total = result['total']
            items.extend(result['items'])
        return items

    def artist_albums(self, artist_id):
        items = []
        total = 1
        while len(items) < total:
            result = self.spotify.artist_albums(artist_id, limit=50, offset=len(items))
            total = result['total']
            items.extend(result['items'])
        return items

    def current_user_followed_artists(self):
        items = []
        after = None
        while True:
            result = self.spotify.current_user_followed_artists(limit=50, after=after)
            after = result['artists']['cursors']['after']
            items.extend(result['artists']['items'])
            if not after:
                break
        return items

    def album_tracks(self, album_id, total, market):
        tracks = []
        while len(tracks) < total:
            result = self.spotify.album_tracks(album_id, limit=50, offset=len(tracks), market=market)
            tracks.extend(result['items'])
        return tracks

    def me(self):
        return self.spotify.me()
