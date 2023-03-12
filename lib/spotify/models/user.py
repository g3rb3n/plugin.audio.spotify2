import urllib.parse
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

from spotify import settings
from spotify.models.base import Model


ADDON_ID=settings.ADDON_ID
BASE_URL = settings.BASE_URL
ADDON_HANDLE = settings.ADDON_HANDLE

addon = xbmcaddon.Addon(id=ADDON_ID)

class User(Model):

    _type = 'user'

    def name(self):
        return self['display_name']

    def parameters(self):
        return {
            'action': 'user',
            'user_id': self['id']
        }

    def icon(self):
        if self['images']:
            return self['images'][0]['url']
        return 'DefaultMusicArtists.png'

    def fanart(self):
        if 'images' in self.data:
            return self['images'][0]['url']
        return 'DefaultMusicSongs.png'
