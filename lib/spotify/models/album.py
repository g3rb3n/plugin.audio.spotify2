import urllib.parse
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

from spotify.models.track import Track

from spotify import settings
from spotify.models.base import Model


ADDON_ID=settings.ADDON_ID
BASE_URL = settings.BASE_URL
ADDON_HANDLE = settings.ADDON_HANDLE


class Album(Model):

    _type = 'album'

    def parameters(self):
        return {
            'action': 'album',
            'album_id': self['id'],
        }

    def model_type(self):
        return 'album'

    def icon(self):
        if 'images' in self.data:
            return self['images'][0]['url']
        return 'DefaultMusicSongs.png'

    def fanart(self):
        if 'images' in self.data:
            return self['images'][0]['url']
        return 'DefaultMusicSongs.png'

    def artists(self):
        artists = [artist['name'] for artist in self['artists']]
        return ' / '.join(artists)

    def genre(self):
        if 'genres' not in self:
            return ''
        return ' / '.join(self['genres'])

    def year(self):
        return int(self['release_date'].split('-')[0])

    def popularity(self):
        if 'popularity' not in self:
            return 0
        self['popularity']

    def tracks(self):
        return [Track(data, self) for data in self.data['tracks']['items']]

    def context_items(self):
        return [(xbmc.getLocalizedString(208), self.action('play_album'))]

    def set_info(self, info):
        info.setArtist(self.artists())
        info.setAlbum(self['name'])
        if self.year():
            info.setYear(self.year())

    def info_labels(self):
        return {
            'album': self.get('name'),
            'artist': self.artists(),
            'year': self.year(),
            'genre': self.genre(),
            'rating': self.popularity(),
        }

    def action(self, action):
        parameters = {
            'action': action,
            'album_id': self['id'],
        }
        qs = urllib.parse.urlencode(parameters)
        return f'RunPlugin({BASE_URL}?{qs})'
