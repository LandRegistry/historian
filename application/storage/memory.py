from application.model import s3shaped

class Storage(object):

    def __init__(self):
        self.store = {}

    def get(self, key, version=None):
        contents = self.store.get(key)
        if contents:
            return S3Shaped(key, contents)
        else:
            return None

    def post(self, key, data):
        self.store[key] = data

    def list_versions(self, key):
        return []
        
    def health(self):
        return True, "in-memory-storage"


