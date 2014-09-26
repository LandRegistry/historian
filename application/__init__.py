import os
import logging
from flask import Flask
from flask.ext.basicauth import BasicAuth
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(os.environ.get('SETTINGS'))

db = SQLAlchemy(app)


# auth
if os.environ.get('BASIC_AUTH_USERNAME'):
    app.config['BASIC_AUTH_FORCE'] = True
    basic_auth = BasicAuth(app)

if not app.debug:
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)
