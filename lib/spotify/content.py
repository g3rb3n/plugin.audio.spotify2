import os
import sys
import json
from urllib.parse import parse_qs
import urllib.parse

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import spotipy

from spotify import settings
from spotify.client import Client

from spotify.models import (
    Artist,
    Album,
    Device,
    ListItem,
    Playlist, UserPlaylist,
    Track,
    User,
)

ADDON_ID=settings.ADDON_ID
BASE_URL = settings.BASE_URL
ADDON_HANDLE = settings.ADDON_HANDLE
addon = xbmcaddon.Addon()

def l(code):
    if code >= 11000 and code < 12000:
        return addon.getLocalizedString(code)
    return xbmc.getLocalizedString(code)

class Content():

    addon = xbmcaddon.Addon()
    loglevel = xbmc.LOGINFO

    menu_labels = {
        'library': l(11008),#'Library',
        'explore': 'Explore',
        'search': 'Search',
        'playback_devices': 'Playback devices',
        'users': 'Users',
        'explore_playlists': 'Playlists',
        'explore_new_releases': 'New releases',
        'top_artists': 'Top artists',
        'top_tracks': 'Top tracks',
        'user_playlists': l(136),
        'saved_albums': l(132),
        'saved_tracks': l(134),
        'followed_artists': 'Artists',
    }

    menu_icons = {
        'library': 'DefaultMusicCompilations.png',
        'explore': 'DefaultMusicGenres.png',
        'search': 'DefaultMusicSearch.png',
        'playback_devices': 'DefaultMusicPlugins.png',
        'users': 'DefaultMusicPlugins.png',
        'explore_playlists': 'DefaultMusicPlugins.png',
        'explore_new_releases': 'DefaultMusicPlugins.png',
        'top_artists': 'DefaultMusicPlugins.png',
        'top_tracks': 'DefaultMusicPlugins.png',
        'user_playlists': 'DefaultMusicPlugins.png',
        'saved_albums': 'DefaultMusicPlugins.png',
        'saved_tracks': 'DefaultMusicPlugins.png',
        'followed_artists': 'DefaultMusicPlugins.png',
    }

    limit = 20
    offset = 0
    market = 'NL'

    def __init__(self, config):
        try:
            self.client = Client(config)
            self.user_id = self.client.me()['id']
            self.parse_parameters()
            if self.action:
                func = getattr(self, self.action)
                func()
            else:
                self.main()
        except Exception as ex:
            time = 5000
            icon = os.path.join(settings.ADDON_PATH, 'resources','media', 'icon.png')
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(ADDON_ID,str(ex), time, icon))
            raise ex
        xbmcplugin.addSortMethod(ADDON_HANDLE, xbmcplugin.SORT_METHOD_UNSORTED)


    def get_arg(self, args, key):
        return args.get(key, [None])[0]

    def parse_parameters(self):
        args = parse_qs(sys.argv[2][1:])
        self.action = self.get_arg(args, 'action')
        self.device_id = self.get_arg(args, 'device_id')
        self.track_id = self.get_arg(args, 'track_id')
        self.album_id = self.get_arg(args, 'album_id')
        self.playlist_id = self.get_arg(args, 'playlist_id')
        self.artist_id = self.get_arg(args, 'artist_id')
        self.owner_id = self.get_arg(args, 'owner_id')
        self.query = self.get_arg(args, 'query')

    def log(self, msg):
        xbmc.log(f'{ADDON_ID} {msg}', level=self.loglevel)

    def log_found(self, t, l):
        xbmc.log(f'{ADDON_ID} Found {len(l)} {t}', level=self.loglevel)

    def log_json(self, msg):
        xbmc.log(f'{ADDON_ID} {json.dumps(msg, indent=2)}', level=self.loglevel)

    def add_list_item(self, list_item):
        xbmcplugin.addDirectoryItem(
            handle=ADDON_HANDLE,
            url=list_item.path(),
            listitem=list_item.to_xmbc_list_item(),
            isFolder=list_item.is_folder
        )

    def list_item(self, key, args={}):
        list_item = ListItem(self.menu_labels[key], key, self.menu_icons[key], True, args=args)
        xbmcplugin.addDirectoryItem(
            handle=ADDON_HANDLE,
            url=list_item.path(),
            listitem=list_item.to_xmbc_list_item(),
            isFolder=list_item.is_folder
        )

    def main(self):
        xbmcplugin.setContent(ADDON_HANDLE, 'files')
        self.list_item('library')
        self.list_item('explore')
        self.list_item('search')
        self.list_item('playback_devices')
        self.list_item('users')
        xbmcplugin.endOfDirectory(handle=ADDON_HANDLE)

    def library(self):
        xbmcplugin.setContent(ADDON_HANDLE, 'files')
        self.list_item('saved_tracks')
        self.list_item('saved_albums')
        self.list_item('followed_artists')
        self.list_item('user_playlists', args={'owner_id':self.user_id})
        xbmcplugin.endOfDirectory(handle=ADDON_HANDLE)

    def explore(self):
        xbmcplugin.setContent(ADDON_HANDLE, 'files')
        self.list_item('top_tracks')
        self.list_item('top_artists')
        self.list_item('explore_new_releases')
        self.list_item('explore_playlists')
        xbmcplugin.endOfDirectory(handle=ADDON_HANDLE)

    def users(self):
        result = self.client.spotify.me()
        user = User(result)
        self.set_directory_items([user], 'files', user['display_name'])

    def explore_playlists(self):
        result = self.client.spotify.featured_playlists()
        playlists = [Playlist(item) for item in result['playlists']['items']]
        self.set_directory_items(playlists, 'files', result['message'])

    def explore_new_releases(self):
        result = self.client.spotify.new_releases()
        albums = [Album(item) for item in result['albums']['items']]
        self.set_directory_items(albums, 'files', 'New releases')

    def playback_devices(self):
        devices = self.client.spotify.devices()['devices']
        devices = [Device(item) for item in devices]
        self.set_directory_items(devices, 'files', 'Playback devices')

    def top_artists(self):
        artists = self.client.spotify.current_user_top_artists(50)['items']
        artists = [Artist(item) for item in artists]
        self.log_found('artists', artists)
        self.set_directory_items(artists, 'artists', 'Top artists')

    def top_tracks(self):
        tracks = [Track(item) for item in self.client.spotify.current_user_top_tracks(50)['items']]
        self.log_found('tracks', tracks)
        self.set_directory_items(tracks, 'songs', 'Top tracks')

    def user_playlists(self):
        playlists = [UserPlaylist(item) for item in self.client.get_user_playlists(self.user_id)]
        self.set_directory_items(playlists, 'files', xbmc.getLocalizedString(136))

    def user_playlist(self):
        playlist = self.client.user_playlist(self.user_id, self.playlist_id, self.market)
        tracks = self.client.user_playlist_tracks(self.user_id, self.playlist_id, playlist['tracks']['total'], self.market)
        tracks = [Track(item['track']) for item in tracks]
        self.set_directory_items(tracks, 'songs', playlist['name'])

    def saved_tracks(self):
        tracks = self.client.current_user_saved_tracks()
        tracks = [Track(item['track']) for item in tracks]
        self.set_directory_items(tracks, 'songs', xbmc.getLocalizedString(134))

    def saved_albums(self):
        albums = [Album(item['album']) for item in self.client.current_user_saved_albums()]
        self.set_directory_items(albums, 'albums', xbmc.getLocalizedString(134))

    def artist_albums(self):
        albums = [Album(item) for item in self.client.artist_albums(self.artist_id)]
        self.log_found('albums', albums)
        self.set_directory_items(albums, 'albums', xbmc.getLocalizedString(134))

    def followed_artists(self):
        artists = [Artist(item) for item in self.client.current_user_followed_artists()]
        self.set_directory_items(artists, 'artists', xbmc.getLocalizedString(134))

    def album(self):
        album = self.client.spotify.album(self.album_id, self.market)
        tracks = [Track(item, Album(album)) for item in album['tracks']['items']]
        self.set_directory_items(tracks, 'songs', album['name'])
        self.log('album done')

    def create_search_result_label(self, result, code, key):
        total = result[key]["total"]
        return f'{xbmc.getLocalizedString(code)} ({total})'

    def search(self):
        xbmcplugin.setContent(ADDON_HANDLE, 'files')
        xbmcplugin.setPluginCategory(ADDON_HANDLE, xbmc.getLocalizedString(283))
        kb = xbmc.Keyboard('', xbmc.getLocalizedString(16017))
        kb.doModal()
        if kb.isConfirmed():
            value = kb.getText()
            items = []
            result = self.client.spotify.search(
                q=value,
                type='artist,album,track,playlist',
                limit=1,
                market=self.market
            )
            tracks_label = self.create_search_result_label(result, 134, 'tracks')
            albums_label = self.create_search_result_label(result, 132, 'albums')
            artists_label = self.create_search_result_label(result, 133, 'artists')
            playlists_label = self.create_search_result_label(result, 136, 'playlists')
            args = {'query':value}
            self.add_list_item(ListItem(tracks_label, 'search_tracks', args=args))
            self.add_list_item(ListItem(albums_label, 'search_albums', args=args))
            self.add_list_item(ListItem(artists_label, 'search_artists', args=args))
            self.add_list_item(ListItem(playlists_label, 'search_playlists', args=args))
        xbmcplugin.endOfDirectory(handle=ADDON_HANDLE)

    def search_artists(self):
        result = self.client.spotify.search(
            q=self.query,
            type='artist',
            limit=self.limit,
            offset=self.offset,
            market=self.market)
        artists = [Artist(item) for item in result['artists']['items']]
        self.set_directory_items(artists, 'artists', 'Artists')
        #self.add_next_button(result['artists']['total'])

    def search_albums(self):
        result = self.client.spotify.search(
            q=self.query,
            type='album',
            limit=self.limit,
            offset=self.offset,
            market=self.market)
        albums = [Album(item) for item in result['albums']['items']]
        self.set_directory_items(albums, 'albums', 'albums')
        #self.add_next_button(result['artists']['total'])

    def search_tracks(self):
        result = self.client.spotify.search(
            q=self.query,
            type='track',
            limit=self.limit,
            offset=self.offset,
            market=self.market)
        tracks = [Track(item) for item in result['tracks']['items']]
        self.set_directory_items(tracks, 'tracks', 'tracks')
        #self.add_next_button(result['artists']['total'])

    def search_playlists(self):
        result = self.client.spotify.search(
            q=self.query,
            type='playlist',
            limit=self.limit,
            offset=self.offset,
            market=self.market)
        playlists = [Playlist(item) for item in result['playlists']['items']]
        self.set_directory_items(playlists, 'playlists', 'playlists')
        #self.add_next_button(result['artists']['total'])

    def playlist(self):
        self.log(f'Get playlist {self.playlist_id}')
        playlist = self.client.spotify.playlist(self.playlist_id, market=self.market)
        playlist = Playlist(playlist)
        self.set_directory_items(playlist.tracks(), 'songs', 'Songs')

    def play(self, uri, use_uris=False):
        try:
            if use_uris:
                self.client.spotify.start_playback(uris=[uri])
            else:
                self.client.spotify.start_playback(context_uri=uri)
        except spotipy.exceptions.SpotifyException:
            devices = self.client.spotify.devices()['devices']
            device = next(item for item in devices if item['name'] == settings.DEVICE_NAME)
            self.device_id = device['id']
            self.set_playback_device()

    def play_track(self):
        self.play(f'spotify:track:{self.track_id}', True)

    def play_playlist(self):
        self.play(f'spotify:playlist:{self.playlist_id}')

    def play_album(self):
        self.play(f'spotify:album:{self.album_id}')

    def play_artist(self):
        self.play(f'spotify:artist:{self.artist_id}')

    def add_to_queue(self):
        self.client.spotify.add_to_queue(f'spotify:track:{self.track_id}')

    def set_playback_device(self):
        self.client.spotify.transfer_playback(self.device_id)

    def set_content_and_folder_name(self, content, folder_name):
        xbmcplugin.setContent(ADDON_HANDLE, content)
        xbmcplugin.setProperty(ADDON_HANDLE, 'FolderName', folder_name)

    def set_directory_items(self, items, content, directory_name):
        self.log('set directory items')
        self.log(f'name {directory_name}')
        self.log(f'#items {len(items)}')
        self.log(f'content {content}')

        self.set_content_and_folder_name(content, directory_name)
        for item in items:
            xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=item.url(), listitem=item.to_xmbc_list_item(), isFolder=item.is_folder)
        xbmcplugin.addSortMethod(ADDON_HANDLE, xbmcplugin.SORT_METHOD_UNSORTED)
        xbmcplugin.endOfDirectory(handle=ADDON_HANDLE)

    def get_user_label(self):
        user_display_name = self.client.me()['display_name']
        if user_display_name:
            return user_display_name
        user_display_name = self.client.me()['id']
        return user_display_name
