import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'yandexlyceum_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ['POSTGRES_DATABASE_URL']
    VAPID_PUBLIC_KEY = "BEFv0LWfGe9QYxnKmh4vSwXZn0UCiCS4VwOy44cRPrhbfG5sqbAZTY1huECnTTBtzjeXcBsiqBVl1RWyUrEtnDk"
    VAPID_PRIVATE_KEY = "7vcBxJXcpIKNeVD7cUlcLTuyJA1lPskXxPC1CnKoU5I"
    VAPID_CLAIM_EMAIL = "abcd@gmail.com"
