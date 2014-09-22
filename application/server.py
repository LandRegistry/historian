from flask import jsonify,  abort, request, make_response

from application import app
from .storage import S3Store
import json
import os

storage = S3Store()


@app.route('/', defaults={'key': ''})
@app.route('/<path:key>', methods=[ 'GET'])
def get(key):
    if not key:
        abort(400)
    version = request.args.get('version')
    if version == 'list':
        lst = storage.list_versions(key)
        return jsonify({'versions': [  _ver(key, ver) for ver in lst]})
    else:
        return get_for_version(key, version)

def _ver(key, ver):
    link = os.environ['HOST'] + key + "?version=" + ver.version_id
    return {
        'version_id': ver.version_id,
        'last_modified':ver.last_modified,
        "http://schema.org/url": { "@id": link }
    }

def get_for_version(key, version):
    value = storage.get(key, version)
    try:
        # see if the content is JSON
        value = json.loads(value)
    except:
        pass
    if not value:
        app.logger.warn('Object not found for key %s and version %s' % (key, version))
        abort(404)
    return jsonify({key : value})


@app.route('/', defaults={'key': ''})
@app.route('/<path:key>', methods=[ 'POST'])
def post(key):
    if not key:
        abort(400)
    try:
        storage.put(key, request.json)
        return 'OK'
    except:
        abort(400)
