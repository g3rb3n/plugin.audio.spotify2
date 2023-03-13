import sys

import xbmc
import xbmcaddon
import xbmcvfs

import os

ADDON_ID = 'plugin.audio.spotify2'
PLATFORM='linux'
SCOPE='user-read-playback-position user-library-read user-library-modify user-read-private user-read-email playlist-modify-public playlist-modify-private playlist-read-private user-top-read playlist-read-collaborative ugc-image-upload user-follow-read user-follow-modify user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-recently-played'


USERNAME=''
PASSWORD=''
DEVICE_NAME='Kodi'
CLIENT_ID=''
CLIENT_SECRET=''
OAUTH_URL='https://kodi.g3rb3n.online/'


LOG_LEVEL=xbmc.LOGINFO
LOG_LEVELS = {
    'librespot': xbmc.LOGINFO
}

BASE_URL = sys.argv[0]
ADDON_HANDLE = int(sys.argv[1]) if len(sys.argv) > 1 else 0

addon = xbmcaddon.Addon()
ADDON_PATH=addon.getAddonInfo('path')

USER_ADDON_DATA_PATH = xbmcvfs.translatePath(f'special://profile/addon_data/{ADDON_ID}')
SETTINGS_JSON_FILE = os.path.join(USER_ADDON_DATA_PATH, 'settings.json')
OAUTH_CACHE_FILE = os.path.join(USER_ADDON_DATA_PATH, '.cache')
