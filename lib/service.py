import xbmc
import os, sys


from librespot import LibreSpot

import xbmc
import xbmcaddon
from spotify import settings
from spotify import utils


if __name__ == '__main__':
    LibreSpot(utils.get_configuration()).start()


def start():
    LibreSpot(utils.get_configuration()).start()
