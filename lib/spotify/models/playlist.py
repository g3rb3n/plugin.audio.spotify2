import urllib.parse
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

from spotify import settings
from spotify.models import Model, Track


ADDON_ID=settings.ADDON_ID
BASE_URL = settings.BASE_URL
ADDON_HANDLE = settings.ADDON_HANDLE


class Playlist(Model):

    _type = 'playlist'
    is_folder = True

    def tracks(self):
        return [Track(item['track']) for item in self.data['tracks']['items']]

    def parameters(self):
        return {
            'action': 'playlist',
            'playlist_id': self['id'],
            'owner_id': self['owner']['id']
        }

    def action(self):
        parameters = {
            'action': 'play_playlist',
            'playlist_id': self['id'],
            'owner_id': self['owner']['id']
        }
        qs = urllib.parse.urlencode(parameters)
        return f'RunPlugin({BASE_URL}?{qs})'

    def icon(self):
        if 'images' in self.data and len(self.data['images']) > 0:
            return self['images'][0]['url']
        return 'DefaultMusicAlbums.png'

    def fanart(self):
        if 'images' in self.data:
            return self['images'][0]['url']
        return 'DefaultMusicSongs.png'

    def context_items(self):
        return [(xbmc.getLocalizedString(208), self.action())]


class UserPlaylist(Playlist):
    def parameters(self):
        return {
            'action': 'user_playlist',
            'playlist_id': self['id'],
            'owner_id': self['owner']['id']
        }
