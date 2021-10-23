import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'yandexlyceum_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ['POSTGRES_DATABASE_URL']
