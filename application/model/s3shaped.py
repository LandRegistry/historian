class S3Shaped(object):
    """
    Returned by the 'storage' to the 'service'.
    Service 's3' is already S3-shaped.
    Service 'db' and 'mem' wraps their results with this class.

    'service' in turn wraps S3Shaped in 'model.render.Contents'
    for rendering.
    """

    def __init__(self, key, data, version, _metadata=None):
        self.key = key
        self.data = data
        self.version = version
        self._metadata = _metadata

    def get_contents_as_string(self):
        return self.data

    @property
    def last_modified(self):
        if 'last_modified' in self.key:
            return self.key['last_modified']
        else:
            return None

    @property
    def version_id(self):
        return self.version

    @property
    def name(self):
        return self.key

    @property
    def metadata(self):
        return self._metadata or {}

    def get_metadata(self, key):
        return self.metadata[key]
