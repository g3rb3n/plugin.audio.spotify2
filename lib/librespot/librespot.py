import os
from subprocess import Popen, PIPE
import threading
import re

import xbmc

from spotify import settings


#[2023-03-12T22:03:51Z INFO  librespot_playback::player] Loading <In Het Gras> with Spotify URI <spotify:track:7EBSK2tltS2K1PdpaVL1Yh>
pattern = re.compile('.*Loading.*<(.*)> with Spotify URI <(.*)>')
icon = os.path.join(settings.ADDON_PATH, 'resources','media', 'icon.png')


class LibreSpot():

    def __init__(self, config):
        self.config = config
        self.loglevel = settings.LOG_LEVELS['librespot']
        self.stdout = None
        self.stderr = None
        self.running = False

    def log(self, msg):
        xbmc.log('%s %s %s' % (settings.ADDON_ID, 'LibreSpot', msg), level=self.loglevel)

    def start(self):
        self.log('start')
        self.run()

    def execute(self, cmd):
        process = Popen(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        for line in iter(process.stderr.readline, ''):
            yield line

    def run(self):
        self.log('run')
        username = self.config.username
        password = self.config.password
        device_name = self.config.device_name
        path = os.path.join(settings.ADDON_PATH, 'lib', 'librespot', settings.PLATFORM, 'librespot')
        cmd = [path,
            '--name', device_name,
            '-u', username,
            '-p', password
        ]
        self.log(cmd)

        self.running = True
        for line in self.execute(cmd):
            self.log(f'read {line}')
            if 'with Spotify URI' in line:
                match = pattern.match(line)
                title = match.group(1)
                uri = match.group(2)
                xbmc.executebuiltin(f'Notification(Spotify, {title}, {5000}, {icon})')
        self.log('end run')
        self.running = False
