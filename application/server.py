from flask import abort, jsonify, request

from application import app

from .service import Service
from .health import Health

service = Service()
Health(app, checks=[service.health])


@app.route('/', defaults={'key': ''})
@app.route('/<path:key>', methods=['GET'])
def get(key):
    if not key:
        abort(400)
    version = request.args.get('version')
    result = service.get(key, version)
    if not result:
        app.logger.warn('Object 404, key=%s, version=%s' % (key, version))
        abort(404)
    else:
        return result


@app.route('/', defaults={'key': ''})
@app.route('/<path:key>', methods=['POST'])
def post(key):
    if not key:
        abort(400)
    try:
        service.post(key, request.json)
        return jsonify(request.json)
    except:
        abort(400)
