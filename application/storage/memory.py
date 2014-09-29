<<<<<<< HEAD

=======
from application import app
>>>>>>> df35ee7a655f954a9e5248bcd842118207b2570a
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
        

class S3Shaped(object):

    def __init__(self, key, data):
        self.key = key
        self.data = data

    def get_contents_as_string(self):
        return self.data

    @property
    def last_modified(self):
        return "Tue, 23 Sep 2014 10:30:42 GMT"

    @property
    def version_id(self):
        return "this-is-the-only-version"

    @property
    def name(self):
        return self.key

    @property
    def metadata(self):
        return {}
