# Spotify plugin for Kodi
A completely rewritten Spotify client based on:
- Python3
- Kodi 20 Nexus
- Librespot for playback
- spotipy
- uses an opensource external service for handling OAuth with a simple short code, see https://github.com/g3rb3n/oauth_server

## Setup
### Install
git clone https://github.com/g3rb3n/plugin.audio.spotify2.git
copy the directory to .kodi/addons/


## Build libresport
https://github.com/librespot-org/librespot/blob/dev/COMPILING.md
https://github-wiki-see.page/m/librespot-org/librespot/wiki/Cross-compiling



### Setup app in Spotify
- Goto https://developer.spotify.com/dashboard/applications
- Click CREATE AN APP
- Fill in app name
- Copy client id and secret

- Click Edit settings
- Enter {your server}/i/callback in Redirect URIs
- Click Add
- Click Save

### Setup OAuth code server
Clone https://github.com/g3rb3n/oauth_server and set it up on your own server.
Fill in your own service url at settings.py / settings.json or in the addon settings in the kodi interface.

## Support
Create an issue in Github.
