from application.model import Historical
from memory import S3Shaped
from application import db
from application import app
import json


class Storage(object):

    def get(self, key, version=None):
        query = db.session.query(Historical).filter(
                Historical.version == version,
                Historical.key == key).first()
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
            self.get_version_number(key)
            version_row.version = self.get_version_number(key)
            db.session.add(version_row)
            db.session.commit()
        except Exception as e:
            app.logger.error(e.message)

    def list_versions(self, key):
        results_list = []
        all_key_versions = db.session.query(Historical).filter(Historical.key == key)
        for historical_instance in all_key_versions:
            results_list.append(S3Shaped(historical_instance.key, historical_instance.value))
        return results_list

    def count(self):
        return Historical.query.count()


    def get_version_number(self, key):
        query = db.session.query(Historical).filter(Historical.key == key)
        next_version_number = query.count() + 1
        return next_version_number


    def health(self):
        try:
            self.count()
            return True, "DB"
        except:
            return False, "DB"

