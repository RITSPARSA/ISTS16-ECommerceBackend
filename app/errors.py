"""
    Errors our API can raise
"""
from flask import jsonify
from . import APP

class AuthError(Exception):
    """Custom error class for invalid credentials"""
    def __init__(self, message=None, status_code=403):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        rv = dict()
        rv['error'] = self.message
        return rv

class TransactionError(Exception):
    """Custom error class for when buying things"""
    def __init__(self, message=None, status_code=403):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        rv = dict()
        rv['error'] = self.message
        return rv

@APP.errorhandler(AuthError)
def handle_authentication_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@APP.errorhandler(TransactionError)
def handle_transaction_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
