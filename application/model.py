import json
import os

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
        link = os.environ['HOST'] + key.name + "?version=" + key.version_id
        self.meta = {
            'version_id': key.version_id,
            'last_modified': key.last_modified,
            "http://schema.org/url": {"@id": link}
        }

    def as_dict(self):
        return self.meta
