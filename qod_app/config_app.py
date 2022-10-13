# -*- coding:utf-8 -*-

"""
config_app.py

Groups Flask configuration environment to init app and api according
to the selected mode (prod, dev, test)
"""


import os
import json
import logging

from flask import Flask

from .extensions import (db,
                         search,
                         misika)
from .routes.app import APP_BP
from .routes.api import API_BP
from .routes.errors_handlers import handler_error
from .models.quote import Quote
from .models.users import User
from .constants import (TEMPLATES,
                        STATICS,
                        PATH,
                        DEV_TEST_DB,
                        PRODUCTION_DB)

# Create a new debug logger
LOGGER = logging.getLogger('[Quote Generator]')
formatter = logging.Formatter(
    "[%(asctime)s][%(name)s][%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(stream_handler)


class BaseConfig:
    """Configuration used in production mode."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
    SQLALCHEMY_DATABASE_URI = PRODUCTION_DB
    JSON_SORT_KEYS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ENV = "production"


class DevConfig(BaseConfig):
    """Configuration used in development mode."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = DEV_TEST_DB
    FLASK_ENV = "development"


class TestConfig(BaseConfig):
    """Configuration used in test mode."""
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = DEV_TEST_DB
    FLASK_ENV = "testing"


def init_db(app) -> None:
    """initialise a new database
    :param app: a Flask app
    :return: None
    """
    # we initialise database in a specific
    # context/environment config thats why
    # we use a context manager here
    with app.app_context():
        # erase all previous database (precaution)
        db.drop_all()
        # create a new database if not exists
        db.create_all()

        # load preprocess quotes data from json
        with open(os.path.join(PATH, 'data/quotes_preprocess.json'),
                  mode='r',
                  encoding='UTF-8') as data_preprocess:
            data_quote = json.loads(data_preprocess.read())

        # bulk insert in database (better than a loop for huge dataset)
        db.session.execute(Quote.__table__.insert(), data_quote)

        # commit the new insert in database
        db.session.commit()

        # For test purpose we create a fictional admin credentials to test/dev mode
        # for prod mode you can use: admin / admin (if you don't recreate
        # database in production) else use test-admin / test-admin
        user = User(username="test-admin", role="admin")
        user.hash_password("test-admin")
        User.add_user(user)


def create_app(mode: str = "dev", erase_db: bool = False):
    """Initialise Quote Generator application
    with a default config
    :param mode: mode use to create a new app according to a config
    :type: str
    :param erase_db: erase and recreate db
    :type: bool
    :return: Flask application
    :rtype: Flask
    """
    # create an instance of class
    quote_generator_app = Flask('quote_of_the_day_app',
                                template_folder=TEMPLATES,
                                static_folder=STATICS,
                                instance_relative_config=True)

    # register subdomains services (API/APP) with blueprints to set
    # different URL rules
    quote_generator_app.register_blueprint(API_BP, url_prefix='/api')
    quote_generator_app.register_blueprint(APP_BP)

    # init config for app (production/dev/test)
    if mode == "dev":
        LOGGER.debug('Initialize dev mode...')
        quote_generator_app.config.from_object(DevConfig)
    elif mode == "test":
        LOGGER.debug('Initialize test mode...')
        quote_generator_app.config.from_object(TestConfig)
    elif mode == "prod":
        LOGGER.debug('Initialize production mode...')
        quote_generator_app.config.from_object(BaseConfig)

    # register common errors
    quote_generator_app.register_error_handler(400, handler_error)
    quote_generator_app.register_error_handler(404, handler_error)
    quote_generator_app.register_error_handler(405, handler_error)
    quote_generator_app.register_error_handler(500, handler_error)

    # initialise an application for the use with this database setup
    db.init_app(quote_generator_app)

    # clear, recreate & populate db if necessary
    if mode != "prod" or erase_db:
        LOGGER.debug('database is recreate...')
        init_db(quote_generator_app)

    # initialise extensions for Flask app
    search.init_app(quote_generator_app)
    misika.init_app(quote_generator_app)

    return quote_generator_app
