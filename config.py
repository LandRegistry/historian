import os

class Config(object):
    DEBUG = False
    STORAGE = os.environ['STORAGE']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

    # these are on heroku only so get safely
    BASIC_AUTH_USERNAME = os.environ.get('BASIC_AUTH_USERNAME')
    BASIC_AUTH_PASSWORD = os.environ.get('BASIC_AUTH_PASSWORD')

class DevelopmentConfig(Config):
    DEBUG = True

class TestConfig(DevelopmentConfig):
    TESTING = True
