import json
import os
from application import db

class Contents(object):
    """The contents of the thing being stored."""

    def __init__(self, obj):
        contents = obj.get_contents_as_string()
        # see if the content is JSON
        try:
            contents = json.loads(contents)
        except:
            pass

        self.value = {
            'contents': contents,
            'meta': Meta(obj).as_dict()
        }

    def as_json(self):
        return json.dumps(self.value)


class Meta(object):
    """Meta-data about the thing being stored."""

    def __init__(self, key):
        self.meta = {
            'version_id': key.version_id,
            'last_modified': key.last_modified
        }
        self.meta.update(VersionedLink(key.name, key.version_id).as_dict())

        if key.metadata:
            previous_version_id = key.get_metadata('previous_version_id')
            if previous_version_id:
                previous = {'version_id': previous_version_id}
                previous.update(VersionedLink(key.name, previous_version_id).as_dict())
                self.meta.update({'previous': previous})

    def as_dict(self):
        return self.meta

class VersionedLink(object):

    def __init__(self, name, version_id):
        self.link = os.environ['HOST'] + name + "?version=" + version_id

    def as_dict(self):
        return {"http://schema.org/url": {"@id": self.link}}


class Historical(db.Model):

    __tablename__ = 'historical'

    key = db.Column(db.String(), nullable=False, primary_key=True)
    value = db.Column(db.String(), nullable=False)
    # metadata -> version, previous version, and a timestamp
    # that timestamp is the historian timestamp, not the system-of-record one
    version = db.Column(db.String(), nullable=False)



