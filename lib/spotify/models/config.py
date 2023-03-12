
class Config():

    data = {}

    def __init__(self, data):
        self.data = data

    def __contains__(self, item):
        return item in self.data

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getattr__(self, attr):
        return self[attr]
