import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'yandexlyceum_secret_key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://kqmjcjomubuvyd:52f4b6cd242a446fefb3e45fe3de66845a178fda77561544dbc609526459b35a@ec2-35-171-171-27.compute-1.amazonaws.com:5432/d4qt4et60i3rlj'
