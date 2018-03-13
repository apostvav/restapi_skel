import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = b'\x15\x01\xf7\x1b]\xce\xf1I\xc3\xc8\xb5^\x05\x9f\xc2\xe6\xd8,-\x06\xe7Z\xb7\xe0'
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'restapi_skel.db')


class TestingConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'restapi_skel_testing.db')


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'restapi_skel_prod.db')


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)
