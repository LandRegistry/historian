from application.model import Historical
from memory import S3Shaped
from application import db
from application import app
from sqlalchemy import func
import json


class DatabaseStorage(object):

    def get(self, key, version=None):
        query = db.session.query(Historical).filter(Historical.version == version, Historical.key == key).first()
        if query:
            app.logger.debug(query.value)
            return S3Shaped(query.key, query.value)
        else:
            app.logger.debug('version not found')
            empty_result = Historical()
            empty_result.key = None
            empty_result.value = None
            empty_result.version = None
            return S3Shaped(empty_result.key, empty_result.value)


    def post(self, key, data):
        app.logger.debug('database storing ' + json.dumps(data))
        try:
            version_row = Historical()
            version_row.key = key
            version_row.value = json.dumps(data)
            version_row.version = '2'

            db.session.add(version_row)

            db.session.commit()
        except Exception as e:
            app.logger.error(e.message)


    def list_versions(self, key):
        self.get_version_number(key)
        pass

    def get_version_number(self, key):
        query = db.session.query(Historical).filter(Historical.key == key)
        app.logger.debug(query.count()) #todo use this to determine next version.

