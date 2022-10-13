# -*- coding:utf-8 -*-

"""Errors controllers
"""

from typing import (Union,
                    Tuple)

from werkzeug import exceptions
from flask import (jsonify,
                   request,
                   render_template,
                   wrappers)


def handler_error(error: exceptions) -> Union[Tuple[str, int], Tuple[wrappers.Response, int]]:
    """A generic handler for HTTP error

    :param error: catch error from HTTP response
    :type: werkzeug.exceptions
    :return: HTML template with error (APP) or a JSON formatted error response
    """
    # Error come from API
    if request.path.startswith("/api/"):
        return jsonify({
            "error": error.code,
            "type": error.description
        }), error.code
    # Error come from APP
    return render_template("pages/generic_error.html", e=error), error.code
