from pathlib import Path


class Configuration:
    APP_DIR = Path(__file__).resolve().parent
    BASE_DIR = APP_DIR.parent
    DATABASE = 'mysql://root:root@localhost:3306/honeybee'
    DB_FILE = str(BASE_DIR.joinpath('honeybee.db'))
    # DATABASE = f'sqliteext:///{DB_FILE}'
    SECRET_KEY = '123456abcdef'
    WTF_CSRF_ENABLED = False


class DevelopmentConfiguration(Configuration):
    DEBUG = True


class TestingConfiguration(Configuration):
    TESTING = True


class ProductionConfiguration(Configuration):
    DEBUG = False
    TESTING = False


config = {
    'development': DevelopmentConfiguration,
    'testing': TestingConfiguration,
    'production': ProductionConfiguration,
    'default': DevelopmentConfiguration
}