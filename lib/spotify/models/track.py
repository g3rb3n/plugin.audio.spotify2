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


class Track(Model):

    _type = 'track'
    is_folder = False

    def __init__(self, data, album = None):
        super().__init__(data)
        self.album = album

    def get_album(self):
        from spotify.models.album import Album
        if self.album:
            return self.album
        return Album(self['album'])

    def model_type(self):
        return 'track'


    def action(self, action):
        parameters = {
            'action': action,
            'track_id': self['id'],
        }
        qs = urllib.parse.urlencode(parameters)
        return f'RunPlugin({BASE_URL}?{qs})'

    def parameters(self):
        return {
            'action': 'play_track',
            'track_id': self['id'],
        }

    def icon(self):
        if 'images' in self.data:
            return self['images'][0]['url']
        if 'album' in self.data and 'images' in self['album']:
            return self['album']['images'][0]['url']
        if self.album:
            return self.album.icon()
        return 'DefaultMusicSongs.png'

    def fanart(self):
        if 'images' in self.data:
            return self['images'][0]['url']
        if 'album' in self.data and 'images' in self['album']:
            return self['album']['images'][0]['url']
        if self.album:
            return self.album.icon()
        return 'DefaultMusicSongs.png'

    def artists(self):
        artists = [artist['name'] for artist in self['artists']]
        return ' / '.join(artists)

    def genre(self):
        if self.album:
            return self.album.genre()
        if 'album' in self.data and 'genre' in self['album']:
            return ' / '.join(self['album']['genres'])
        return None

    def year(self):
        if 'album' in self.data and 'release_date' in self['album']:
            int(self['album']['release_date'].split('-')[0])
        if self.album:
            return self.album.year()
        return None

    def context_items(self):
        return [
            (xbmc.getLocalizedString(208), self.url()),
            ('View album', self.get_album().url()),
            ('Add to queue', self.action('add_to_queue'))
        ]

    def set_list_item(self, li):
        li.setProperty('spotifytrackid', self['id'])

    def set_info(self, info):
        if self.year():
            info.setYear(self.year())
        info.setAlbum(self.get_album()['name'])
        info.setArtist(self.artists())
        info.setTitle(self['name'])
        info.setDuration(int(self['duration_ms'] / 1000))
        info.setTrack(self['track_number'])
