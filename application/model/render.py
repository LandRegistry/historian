import json
import os
from application import app

# Classes to destructure 'S3Shaped' for rendering purposes.


class Contents(object):
    """The contents of the thing being stored."""

    def __init__(self, obj):
        contents = obj.get_contents_as_string()
        # see if the content is JSON
        try:
            contents = json.loads(contents)
            app.logger.debug(contents)
        except:
            pass

        try:
            meta_instance = Meta(obj)
            self.value = {
                'contents': contents,
                'meta': meta_instance.as_dict()
            }
        except Exception as e:
            app.logger.debug(e.message)

    def as_json(self):
        return json.dumps(self.value)


class Meta(object):
    """Meta-data about the thing being stored."""
    def __init__(self, obj):
        self.meta = {
            'version_id': obj.version_id,
            'last_modified': obj.last_modified
        }
        self.meta.update(VersionedLink(obj.name, obj.version_id).as_dict())

        if obj.metadata:
            previous_version_id = obj.get_metadata('previous_version_id')
            if previous_version_id:
                previous = {'version_id': previous_version_id}
                previous.update(
                        VersionedLink(obj.name, previous_version_id).as_dict())
                self.meta.update({'previous': previous})

    def as_dict(self):
        return self.meta


class VersionedLink(object):

    def __init__(self, name, version_id):
        self.link = os.environ['HOST'] + name + "?version=" + version_id

    def as_dict(self):
        return {"http://schema.org/url": {"@id": self.link}}
