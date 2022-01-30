import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '66b49769-1259-473d-8409-cc48876dbb0b'
    ENV = os.environ.get('ENV') or 'development'
    HEADERS = 'Access-Control-Allow-Origin:*'
