import urllib.parse
import xbmcgui

from spotify import settings
from spotify.models.base import Model

ADDON_ID=settings.ADDON_ID
BASE_URL = settings.BASE_URL
ADDON_HANDLE = settings.ADDON_HANDLE


class ListItem():
    icon = ''
    label = ''
    action = ''
    is_folder = False

    def __init__(self, label, action, icon='DefaultMusicPlaylists.png', is_folder=True, args={}):
        self.label = label
        self.label = label
        self.action = action
        self.is_folder = is_folder
        self.args = args

    def path(self):
        self.args['action'] = self.action
        qs = urllib.parse.urlencode(self.args)
        return f'plugin://{ADDON_ID}/?{qs}'

    def to_xmbc_list_item(self):
        list_item = xbmcgui.ListItem(
            self.label,
            path=self.path()
        )
        list_item.setProperty('IsPlayable', 'false')
        list_item.setArt({'fanart': 'special://home/addons/plugin.audio.spotify2/resources/media/fanart.jpg'})
        list_item.addContextMenuItems([], True)
        return list_item
