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

class Artist(Model):

    _type = 'artist'

    def parameters(self):
        return {
            'action': 'artist_albums',
            'artist_id': self['id']
        }

    def action(self, cmd, action, parameters):
        parameters['action'] = action
        qs = urllib.parse.urlencode(parameters)
        return f'{cmd}({BASE_URL}?{qs})'

    def context_items(self):
        parameters = {'artistid':self['id']}
        #follow_action = 'unfollow_artist' if self.is_followed else 'follow_artist'
        return [
            (xbmc.getLocalizedString(208), self.action('RunPlugin', 'connect_playback', parameters)),
            (xbmc.getLocalizedString(132), self.action('Container.Update', 'browse_artistalbums', parameters)),
            (addon.getLocalizedString(11011), self.action('Container.Update', 'artist_toptracks', parameters)),
            (addon.getLocalizedString(11012), self.action('Container.Update', 'related_artists', parameters)),
            #(self.addon.getLocalizedString(11026), self.action('RunPlugin', follow_action, parameters))
        ]

    def icon(self):
        if self['images']:
            return self['images'][0]['url']
        return 'DefaultMusicArtists.png'

    def fanart(self):
        if 'images' in self.data:
            return self['images'][0]['url']
        return 'DefaultMusicSongs.png'

    def get_genre(self):
        return ' / '.join(self['genres'])

    def get_rating(self):
        return str(get_track_rating(self['popularity']))

    def followers(self):
        return '%s followers' % self['followers']['total']

    def info_labels(self):
        return {
            'genre': self.get_genre(),
            'artist': self['name'],
            'rating': self['popularity']
        }

    def context_items(self):
        return [(xbmc.getLocalizedString(208), self.action('play_artist'))]

    def action(self, action):
        parameters = {
            'action': action,
            'album_id': self['id'],
        }
        qs = urllib.parse.urlencode(parameters)
        return f'RunPlugin({BASE_URL}?{qs})'
