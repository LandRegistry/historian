from application.model import Historical
from application import db
from application import app
import json


class DatabaseStorage(object):

    # TODO
    # talk to database
    def get(self, key, version=None):
        pass

    def post(self, key, data):
        app.logger.debug('database storing ' + json.dumps(data))
        try:
            version_row = Historical()
            version_row.key = key
            version_row.value = json.dumps(data)
            version_row.version = '1'

            db.session.add(version_row)

            db.session.commit()
        except Exception as e:
            app.logger.error(e.message)






    def list_versions(self, key):
        pass
