# -*- coding:utf-8 -*-

"""A set of Flask extensions use in Quote Generator
"""

from flask_sqlalchemy import SQLAlchemy
from flask_msearch import Search
from flask_misaka import Misaka

db = SQLAlchemy()
search = Search()
misika = Misaka(footnotes=True, tables=True, fenced_code=True, autolink=True, quote=True)
