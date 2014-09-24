import json
from .model import Contents, Meta
from application import app
from .storage import S3Store
from .storage import pgStore


class Service(object):
    """
    Translates boto/S3 objects from 'storage' module
    into simple representations.
    """

    def __init__(self):
        # if app.config['STORAGE'] == 'S3':
        #     self.storage = S3Store()
        # else:
        self.storage = pgStore

    def post(self, key, data):
        self.storage.post(key, data)

    def get(self, key, version=None):
        if version == 'list':
            lst = self.storage.list_versions(key)
            return json.dumps(
                {'versions': [Meta(ver).as_dict() for ver in lst]}
            )
        else:
            return self.get_for_version(key, version)

    def get_for_version(self, key, version):
        try:
            obj = self.storage.get(key, version)
            return Contents(obj).as_json()
        except:
            return None



