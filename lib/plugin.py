import xbmc
import os, sys

#sys.path.insert(1, os.path.join(os.path.dirname(__file__), 'resources', 'lib'))
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '..', '..', 'script.module.urllib3', 'lib'))
xbmc.log(','.join(sys.path), level=xbmc.LOGINFO)

import urllib3
xbmc.log(f'urllib3 version {urllib3.__version__}', level=xbmc.LOGINFO)

from spotify.content import Content
from spotify.utils import get_configuration, set_settings, log_json


class Plugin():


    def main(self):
        config = get_configuration()
        set_settings(config)
        self.content = Content(config)

    def stop(self):
        self.control = None

if __name__ == '__main__':
    Plugin().main()
