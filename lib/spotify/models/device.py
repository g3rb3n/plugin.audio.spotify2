from spotify.models.base import Model


class Device(Model):

    _type = 'Speaker'

    def parameters(self):
        return {
            'action': 'set_playback_device',
            'device_id': self['id'],
        }
