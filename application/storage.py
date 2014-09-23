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

    def post(self, key, data):
        # the new object to persist
        obj = Key(self.bucket)

        # get the previous version, if any
        previous = self.get(key, None)

        if previous:
            obj.set_metadata('previous_version_id', previous.version_id)

        # persist the new object
        obj.key = key
        obj.set_contents_from_string(json.dumps(data))

        # Do not:
        # - attempt to set 'previous'' metadata to have a pointer
        #   to 'next', because versioned objects' metadata cannot
        #   be modified.
        # - make a copy of 'previous' via 'set_remote_metadata' and
        #   expect to be able to just delete old 'previous' and
        #   setting 'current''s previous_version_id to the new
        #   previous' version_id, because at this point 'current'
        #   will be un-modifiable. Chicken/egg, in a nutshell.


    def get(self, key, version=None):
        return self.bucket.get_key(key, version_id=version)

    def list_versions(self, key):
        return self.bucket.list_versions(prefix=key)
