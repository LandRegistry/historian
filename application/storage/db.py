from application.model.db import Historical
from sqlalchemy import desc
from application.model.s3shaped import S3Shaped
from application import db
from application import app
import json


class Storage(object):

    def get(self, key, version=None):
        if version:
            result = db.session.query(Historical).filter(
                Historical.version == version,
                Historical.key == key).first()
        else:
            # try and get latest version
            result = db.session.query(Historical).filter(
                Historical.key == key).order_by(desc(
                        Historical.version)).first()

        if result:
            metadata = {}

            # get previous version of this result
            previous = self.__get_previous_version_of(result)
            if previous:
                metadata['previous_version_id'] = previous.version

            return S3Shaped(
                   result.key,
                   result.value,
                   result.version,
                   metadata)
        else:
            return None

    def post(self, key, data):
        app.logger.debug('database storing ' + json.dumps(data))
        try:
            version_row = Historical()
            version_row.key = key
            version_row.value = json.dumps(data)
            version_row.version = self.__get_version_number(key)
            db.session.add(version_row)
            db.session.commit()
        except Exception as e:
            app.logger.error(e.message)

    def list_versions(self, key):
        results_list = []
        all_key_versions = db.session.query(
                Historical).filter(
                        Historical.key == key)
        for historical_instance in all_key_versions:
            results_list.append(
                S3Shaped(
                    historical_instance.key,
                    historical_instance.value,
                    historical_instance.version))
        return results_list

    def count(self):
        return Historical.query.count()

    def __get_version_number(self, key):
        query = db.session.query(Historical).filter(Historical.key == key)
        next_version_number = query.count() + 1
        return next_version_number

    def __get_previous_version_of(self, obj):
        """
        Gets the predecessor of retrieved 'obj'
        """
        previous_version = int(obj.version) - 1
        result = db.session.query(Historical).filter(
                Historical.version == str(previous_version),
                Historical.key == obj.key).first()
        return result

    def health(self):
        try:
            self.count()
            return True, "DB"
        except:
            return False, "DB"
