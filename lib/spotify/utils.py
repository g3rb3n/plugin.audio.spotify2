import json

import xbmc
import xbmcaddon

from spotify import settings
from spotify.models.config import Config
from spotify.settings import ADDON_ID, LOG_LEVEL, SETTINGS_JSON_FILE


def error(msg):
    xbmc.log(f'{ADDON_ID} {msg}', level=xbmc.LOGERROR)

def log(msg):
    xbmc.log(f'{ADDON_ID} {msg}', level=LOG_LEVEL)

def log_found(t, l):
    xbmc.log(f'{ADDON_ID} Found {len(l)} {t}', level=LOG_LEVEL)

def log_json(msg):
    xbmc.log(f'{ADDON_ID} {json.dumps(msg, indent=2)}', level=LOG_LEVEL)


def update(d1, d2):
    for k in d2:
        if d2[k]:
            d1[k] = d2[k]

def set_settings(config):
    if config['username']:
        settings.USERNAME=config['username']
    if config['password']:
        settings.PASSWORD=config['password']
    if config['device_name']:
        settings.DEVICE_NAME=config['device_name']
    if config['client_id']:
        settings.CLIENT_ID=config['client_id']
    if config['client_secret']:
        settings.CLIENT_SECRET=config['client_secret']
    if config['oauth_url']:
        settings.OAUTH_URL=config['oauth_url']

def get_configuration_from_settings():
    return Config({
        'username': settings.USERNAME,
        'password': settings.PASSWORD,
        'device_name': settings.DEVICE_NAME,
        'client_id': settings.CLIENT_ID,
        'client_secret': settings.CLIENT_SECRET,
        'oauth_url': settings.OAUTH_URL,
    })

def get_configuration_from_settings_json():
    try:
        with open(settings.SETTINGS_JSON_FILE) as f:
            return json.load(f)
    except Exception as ex:
        error(f'Could not load settings from {settings.SETTINGS_JSON_FILE} {str(ex)}')
    return {}

def get_configuration_from_kodi():
    addon = xbmcaddon.Addon()
    return {
        'username': addon.getSetting('username'),
        'password': addon.getSetting('password'),
        'device_name':  addon.getSetting('device_name'),
        'client_id':  addon.getSetting('client_id'),
        'client_secret':  addon.getSetting('client_secret'),
        'oauth_url':  addon.getSetting('oauth_url'),
    }

def get_configuration():
    config = get_configuration_from_settings()
    update(config, get_configuration_from_kodi())
    update(config, get_configuration_from_settings_json())
    log_json(config.data)
    return config
