import urllib.parse
import xbmcgui

from spotify import settings

ADDON_ID=settings.ADDON_ID
BASE_URL = settings.BASE_URL

class Model():
    data = {}

    is_folder = True

    def __init__(self, data):
        self.data = data
        self.check_type()

    def model_type(self):
        if self._type:
            return self._type
        return None

    def data_type(self):
        return self['type']

    def type(self):
        return None

    def check_type(self):
        self_type = self.model_type()
        data_type = self.data_type()
        if self_type:
            if data_type != self_type:
                raise Exception(f'Wrong type {data_type} is not {self_type}')

    def __contains__(self, item):
        return item in self.data

    def get(self, key):
        return self[key]

    def __getitem__(self, key):
        return self.data[key]

    def __getattr__(self, attr):
        return self[attr]

    #def __setattr__(self, attr, value):
    #    self[attr] = value

    def parameters(self):
        raise Exception('Not implemented')

    def action(self, cmd, action, parameters):
        parameters['action'] = action
        qs = urllib.parse.urlencode(parameters)
        return f'{cmd}({BASE_URL}?{qs})'

    def url(self):
        parameters = self.parameters()
        qs = urllib.parse.urlencode(parameters)
        return f'{BASE_URL}?{qs}'

    def fanart(self):
        return 'special://home/addons/plugin.audio.spotify2/resources/media/fanart.jpg'

    def icon(self):
        return 'special://home/addons/plugin.audio.spotify2/resources/media/icon.jpg'

    def art(self):
        return {
            'fanart': self.fanart(),
            'thumb': self.icon()
        }

    def set_info(self, info):
        pass

    def info_labels(self):
        return {}

    def context_items(self):
        return []

    def set_list_item(self, li):
        pass

    def name(self):
        return self['name']

    def to_xmbc_list_item(self):
        li = xbmcgui.ListItem(self.name(), path=self.url(), offscreen=True)
        li.setProperty('IsPlayable', 'false')
        li.setProperty('do_not_analyze', 'true')
        li.setArt(self.art())
        li.setInfo(
            type='Music',
            infoLabels=self.info_labels()
        )
        li.addContextMenuItems(self.context_items(), True)
        self.set_list_item(li)
        info = li.getMusicInfoTag()
        self.set_info(info)
        return li

    def log(self, msg):
        xbmc.log('%s --> %s' % (ADDON_ID, msg), level=xbmc.LOGINFO)
