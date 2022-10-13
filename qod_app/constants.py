# -*- coding:utf-8 -*-

"""A set of constants use in Quote Generator
"""

import os

# Define path constants
PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(PATH, 'templates')
STATICS = os.path.join(PATH, 'statics')
API_DOC = os.path.join(PATH, 'documentation/API_service.md')


PRODUCTION_DB = "sqlite:////" + os.path.join(PATH, "db_store/db_prod.sqlite")
DEV_TEST_DB = "sqlite:////" + os.path.join(PATH, "db_store/db.sqlite")

BASE_API_RESPONSE = {
    "info": {
     "name": "Quote Generator API",
     "version": "1.0",
     "status": True,
    }
}
