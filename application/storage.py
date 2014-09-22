import boto
import json
from boto.s3.key import Key
import os


class S3Store(object):

    def __init__(self):
        connection = boto.connect_s3()
        bucket = connection.lookup(os.environ['S3_BUCKET'])
        if not bucket:
            # if the user does not have 'create' permissions, ensure to create
            # a bucket with versioning enabled.
            bucket = connection.create_bucket(self.s3_bucket)
            bucket.configure_versioning(True)
        self.bucket = bucket


    def put(self, key, data):
        obj = Key(self.bucket)
        obj.key = key
        obj.set_contents_from_string(json.dumps(data))

    def get(self, key, version=None):
        obj = Key(self.bucket)
        obj.key = key
        try:
            return obj.get_contents_as_string()
        except:
            return None


    def list_versions(self, key):
        return self.bucket.list_versions(prefix=key)

