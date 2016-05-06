import os

from utils import sitename_from_readme, splitcamel

class Config(object):
    # configuration
    NAME = "DEBUG"
    SECRET_KEY = 'shh'
    DEBUG = True
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_USERNAME = "KentonCountyLibrary@gmail.com"
    MAIL_PASSWORD = "CincyPyCoders"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_DEFAULT_SENDER = "KentonCountyLibrary@gmail.com"

    SQLALCHEMY_DATABASE_URI = "sqlite:///library.db"

    SITENAME = sitename_from_readme()
    if not SITENAME:
        raise RuntimeError("The site's name not found in README.")
    SITENAMEPARTS = splitcamel(SITENAME)

    def __init__(self):
        print "Config environment is: " + self.NAME

class TestConfig(Config):
    NAME = "TEST"
    SQLALCHEMY_DATABASE_URI = "sqlite://"

config = None
if os.environ.get("LIBRARY_ENV") == "test":
    config = TestConfig()
else:
    config = Config()
