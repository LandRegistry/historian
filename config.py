import os

# TODO bring os.environ calls from code into this module

class Config(object):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestConfig(DevelopmentConfig):
    TESTING = True
