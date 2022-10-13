# -*- coding:utf-8 -*-

"""API controllers
"""
import random

from flask import (Blueprint,
                   request,
                   jsonify,
                   abort,
                   render_template)
from flask_httpauth import HTTPBasicAuth

from ..models.quote import Quote
from ..models.users import User
from ..constants import BASE_API_RESPONSE, API_DOC


API_BP = Blueprint('api', __name__)
AUTH = HTTPBasicAuth()

# collection of utils functions #


def create_response(results: dict = None, parameters: dict = None) -> dict:
    """Build and returns a serialized response with parameters and
    results

    :param results: data results
    :type: dict
    :param parameters: parameters to HTTP method
    :type: dict
    :return: a serialized response that contains all information
    :rtype: dict
    """
    # prevent update from API response template
    response = dict(BASE_API_RESPONSE)
    # update API response template with
    # parameters and response
    if parameters is not None:
        response['parameters'] = parameters
    if results is not None:
        response['results'] = results
    return response


def fulltext_search(query: str, exact_match: bool = False, limit_threshold: int = None) -> list:
    """Query exact or fuzzy match quotes in database and limit or not the return results

    :param query: user query
    :type: str
    :param exact_match: set to True to exact match else fuzzy is activated
    :type: bool
    :param limit_threshold: limit the number of resuls
    :type: int
    :return: list of quotes matched
    :type: list
    """
    # Exact string matching
    if exact_match:
        return Quote.query.filter(Quote.quote.like(f"% {query} %")).limit(limit_threshold)
    # Fuzzy string matching (using msearch)
    return Quote.query.msearch(query, fields=['quote']).limit(limit_threshold)


def make_search_response(parameters: dict) -> dict:
    """Analyze request if query parameter is set or not
    and returns data to user

    :param parameters: parameters provided  by a user
    :type: dict
    :return: data results
    :rtype: dict
    """
    # search with query string (exact or fuzzy)
    # we can create a more complex interface that includes
    # complex clauses with boolean operators like OR / AND
    # eg. <query> OR <category> AND <author>
    if parameters['q'] != "":
        data = [quote_obj.serialize for quote_obj in fulltext_search(
            query=parameters['q'],
            exact_match=parameters['exact'],
            limit_threshold=parameters['rows']
        )]
    else:
        # return data with limit by default
        data = Quote.get_all_quotes(limit_threshold=parameters['rows'])

    total_data = len(data)

    results = {
        "TotalQuotes": total_data,
        "quotes": data
    }
    return results


def check_cast_bool(arg: str) -> bool:
    """Check and cast boolean value from JS
    :param arg: boolean arg from parameters provided from JS
    :type arg: str
    :return: a boolean value
    """
    if arg is not None:
        # prevent uppercase True or true
        arg = arg.lower()
        if arg == "true":
            return True
    return False


def check_params_post_request(base_params: dict, params_to_check: dict) -> dict:
    """Check and verify if parameters from user is allowed or not
    and returns parameters if correct

    :param base_params: parameters accepted by the request
    :type: dict
    :param params_to_check: parameters from user that check
    :type: dict
    :return: parameters checked (correct parameters) or empty dict (incorrect parameters provided)
    """
    for param, value in params_to_check.items():
        if param in base_params.keys():
            # fill the base params with value associated
            base_params[param] = value
        else:
            # case if params in POST request is wrong
            return {}
    return base_params


@API_BP.route('/', methods=['GET'])
def service_quote_api():
    """Base endpoint
    """
    if request.method == 'GET':
        return jsonify(create_response()), 200
    return abort(405)


@API_BP.route('/search', methods=['GET', 'POST'])
def search_quotes():
    """Endpoint that provided an interface for searching in quotes database
    """
    # return all quotes by default
    parameters = {
        "rows": None,
        "q": "",
        "exact": False
    }
    if request.method == "GET":
        # fetch args from user parameters submitted in dict form
        parameters = {
            "rows": request.args.get('rows', None, type=int),
            "q": request.args.get('q', "", type=str),
            "exact": check_cast_bool(request.args.get('exact'))
        }

    elif request.method == "POST":
        # check if user provided data in JSON else return
        # all quote with default dict parameters
        if request.is_json:
            parameters = check_params_post_request(base_params=parameters,
                                                   params_to_check=request.json)
            if len(parameters) == 0:
                # case if params in POST request is wrong
                return abort(400)
    else:
        return abort(405)

    return jsonify(
        create_response(
            parameters=parameters,
            results=make_search_response(parameters=parameters)
        )), 200


@API_BP.route('/random', methods=['GET', 'POST'])
def random_quote():
    """Endpoint that returns a random quote from database (a query parameter can be set)
    """
    # return a random quote by default
    parameters = {"q": ""}
    if request.method == 'GET':
        keyword = request.args.get('q', "", type=str)
    elif request.method == 'POST':
        # check if user provided data in JSON else return
        # a random quote with empty q parameter
        if request.is_json:
            # check if parameters are valid
            parameters = check_params_post_request(base_params=parameters,
                                                   params_to_check=request.json)
            # case if params in POST request are wrong:
            # > return an 400 error
            if len(parameters) == 0:
                return abort(400)

        # get the term from parameters
        keyword = parameters['q']
    else:
        return abort(405)
    # if term is empty from parameters return a random quote
    if keyword == "":
        quotes = Quote.get_all_quotes()
    # returns a list of quotes that match with
    # the term
    else:
        quotes = [
            quote_obj.serialize for quote_obj in fulltext_search(query=keyword,
                                                                 exact_match=True)
        ]

    # case if neither quotes match with a term
    if len(quotes) == 0:
        return abort(404, f"sorry there is no quote for the "
                          f"query '{keyword}', you can suggest one.")

    return jsonify(
        create_response(
            # use random module to select a random quote
            # from list of quotes
            results=random.choice(quotes),
            parameters={"q": keyword}
        )), 200


@API_BP.route('/authors', methods=['GET'])
def get_unique_authors():
    """Endpoint that returns a list of available authors
    """
    if request.method == "GET":
        return jsonify(
            create_response(results={
                "authors": Quote.get_unique_authors()
            })), 200
    return abort(405)


@API_BP.route('/categories', methods=['GET'])
def get_unique_categories():
    """Endpoint that returns a list of available categories
    """
    if request.method == "GET":
        return jsonify(
            create_response(results={
                "categories": Quote.get_unique_categories()
            })), 200
    return abort(405)


@API_BP.route('/sources', methods=['GET'])
def get_unique_sources():
    """Endpoint that returns a list of available sources
    """
    if request.method == "GET":
        return jsonify(
            create_response(results={
                "sources": Quote.get_unique_sources()
            })), 200
    return abort(405)


# I propose these methods as experimental features
# and can be requires authentication
# (in test/dev mode use credentials: ['test-admin', 'test-admin'])
@API_BP.route('/suggest_quote', methods=['POST'])
def suggest_quote():
    """Endpoint for suggest a new quote
    """
    if request.method == "POST":
        parameters_accepted = {
            "author": "",
            "quote": "",
            "source": ""
        }
        # check if request is json serialized
        if request.is_json:
            quote_user = request.json
            parameters = check_params_post_request(base_params=parameters_accepted,
                                                   params_to_check=request.json)
            if len(parameters) == 0:
                # case if params in POST request are wrong
                return abort(400)
        # case if json not provided
        else:
            return abort(400)
        # check if author or quote is empty
        if parameters['quote'] == "" or parameters['author'] == "":
            return jsonify({
                "type": "sorry your quote is rejected because author or quote fields are empty.",
                "quote_submitted": quote_user
            }), 400
        return jsonify(
            {"type": "Your quote is submitted, our team "
                     "check this new quote before add it to database",
             "quote_submitted": quote_user}
        ), 200
    return abort(405)


@AUTH.verify_password
def check_password(username: str, password: str) -> bool:
    """Use by flask_httpauth to control authentification
    before request

    :param username: plain username
    :type: str
    :param password: plain password
    :type: str
    :return: True if credentials are correct
    :rtype: bool
    """
    user = User.query.filter_by(username=username).first()
    # check if user not exists or if password is not correct or user has no admin role
    if not user or not user.verify_password(password) or not user.role == "admin":
        return False
    return True


@API_BP.route('/delete_quote/<int:quote_id>', methods=['GET', 'DELETE'])
@AUTH.login_required()
def delete_quote(quote_id):
    """Endpoint for delete a quote (authorization required)
    """
    # It seems better to separate DELETE and GET method here
    # GET: only to retrieve quote we want to delete
    # DELETE: delete completely quote from database (?)
    if request.method in ("DELETE", "GET"):
        try:
            # get the quote that removed
            old_quote = Quote.delete_quote(quote_id)
            status = 200
        except (AttributeError, KeyError):
            old_quote = "The quote not exists or already removed from the database."
            status = 400
        return jsonify(
            create_response(
                results={'quote_delete': old_quote},
                parameters={"quote_id": quote_id}
            )
        ), status
    return abort(405)


@API_BP.route('/update_quote', methods=['PUT', 'POST'])
@AUTH.login_required()
def update_quote():
    """Endpoint for update a quote (authorization required)
    """
    parameters_accepted = {
        "quote_id": "",
        "author": "",
        "quote": "",
        "source": "",
        "category": ""
    }

    if request.method in ("PUT", "POST"):
        parameters = check_params_post_request(base_params=parameters_accepted,
                                               params_to_check=request.json)
        try:
            # get the quote that updated
            quote_to_update = Quote.updated_quote(new_values=parameters)
            status = 200
        except (AttributeError, KeyError):
            quote_to_update = "The quote cannot be updated, please check parameters."
            status = 400
        return jsonify(
            create_response(
                results={"quote_updated": quote_to_update},
                parameters=parameters
            )
        ), status
    return abort(405)


@API_BP.route('/users', methods=['POST'])
def new_user():
    """Endpoint for create a new user"""
    if request.method == 'POST':
        # get credentials from headers
        username = request.json.get('username')
        password = request.json.get('password')
        if username is None or password is None:
            return abort(400)  # missing arguments
        if User.query.filter_by(username=username).first() is not None:
            return abort(400)  # existing user
        # add new user to the database
        user = User(username=username, role='invite')
        user.hash_password(password)
        User.add_user(user)
        return jsonify({'username': user.username}), 200
    return abort(405)


@API_BP.route('/docs', methods=['GET'])
def api_doc():
    """Endpoint to retrieve the API doc"""
    if request.method == 'GET':
        with open(API_DOC, "r", encoding="utf-8") as input_file:
            text = input_file.read()
        return render_template('pages/doc_api.html', mkd_text=text)
    return abort(405)
