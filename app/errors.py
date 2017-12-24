"""
    Errors our API can raise
"""
from flask import jsonify
from . import APP

class AuthError(Exception):
    """Custom error class for invalid credentials"""
    def __init__(self, message=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = 403

    def to_dict(self):
        rv = dict()
        rv['error'] = self.message
        return rv


@APP.errorhandler(AuthError)
def handle_authentication_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
