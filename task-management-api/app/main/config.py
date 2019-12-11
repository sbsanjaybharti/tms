import os

# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:

    """
    Environmental variable configurations
    """

    """
    MySQL connection variable
    """
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
    DATA_PERPAGE = 10
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')

    """
    Security secret key
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')

    """
    Auth0 connection variable
    """
    DOMAIN = os.getenv('DOMAIN')

    """
    Mail config
    """
    # MAIL_SERVER = 'smtp.gmail.com'
    # MAIL_PORT = 25
    # MAIL_USE_TLS = 587
    # MAIL_USE_SSL = 852
    # # MAIL_DEBUG = app.debug
    # MAIL_USERNAME = 'bhartisanjay646@gmail.com'
    # MAIL_PASSWORD = 'Sanjay@123'
    # MAIL_DEFAULT_SENDER = 'bhartisanjay646@gmail.com'
    # MAIL_MAX_EMAILS = None
    # # MAIL_SUPPRESS_SEND = app.testing
    # MAIL_ASCII_ATTACHMENTS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config_by_name = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig
)

key = Config.SECRET_KEY
