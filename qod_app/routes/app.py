# -*- coding:utf-8 -*-

"""Quote generator application controllers
"""

from flask import (Blueprint,
                   render_template)

APP_BP = Blueprint('app', __name__)


@APP_BP.route('/')
def home():
    """Returns views to generate a random quote
    """
    return render_template('pages/home.html')


@APP_BP.route('/advanced_search')
def search_quote():
    """Returns views for full text search in quotes database
    """
    return render_template('pages/advanced_search.html')


"""
@APP_BP.route('/suggest_quote', methods=['GET', 'POST'])
def suggest_quote():
    # just for the demo
    # a new quote will be save nowhere here
    if request.method == "POST":
        flash("Thanks for your contributing, please wait until our team check your quote.")
    return render_template('pages/suggest_quote.html')
"""
