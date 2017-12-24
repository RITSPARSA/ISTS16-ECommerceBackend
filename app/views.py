"""
    Entry point for API calls
"""
import time
from flask import request, jsonify, abort
from . import APP, DB
from .models.session import Session
from .models.users import Users
from .models.transaction import Transaction
from .models.item import Item
from . import errors


@APP.route('/login', methods=['POST'])
def login():
    """
    Verifies if a the submitted credentials are correct

    :param username: username of the team
    :param password: teams password
    :param token: the auth token to be attached to this account

    :returns result: json dict containing either a success or and error
    """
    result = dict()
    data = request.get_json()
    if data is None:
        data = request.form
    # ADD CHECK IF NO DATA

    username = data['username']
    password = data['password']

    user = Users.query.filter_by(username=username, password=password).first()
    if user is None:
        raise errors.AuthError('Invalid username or password')
    else:
        new_session(user.uuid, data['token'], request.remote_addr)
        result['success'] = "Successfully logged in"

    return jsonify(result)

@APP.route('/get-balance', methods=['POST'])
def get_balance():
    """
    Gets the balance of a team

    :param token: the auth token for that team

    :returns result: json dict containing either the account balance or an error
    """
    result = dict()
    data = request.get_json()
    if data is None:
        data = request.form

    token = data['token']
    session = Session.query.filter_by(token=token).first()
    if session is None:
        raise errors.AuthError('Invalid session')
    else:
        uuid = session.uuid
        user = Users.query.filter_by(uuid=uuid).first()
        balance = user.balance
        result['balance'] = balance

    return jsonify(result)


@APP.route('/buy', methods=['POST'])
def buy():
    """
    Buys a item from the white team store

    :param token: the auth token for the team
    :param item_id: the id of the item to buy

    :return result: json dict containg either the id of the transaction or an error
    """
    pass

@APP.route('/expire-session', methods=['POST'])
def expire_session():
    """
    Set a teams auth token to NULL, essentially expiring their session

    :param token: the authentication token to expire, must be valid

    :return result: json dict containing either a success or an error
    """
    result = dict()
    data = request.get_json()
    if data is None:
        data = request.form

    token = data['token']
    session = Session.query.filter_by(token=token).first()
    if session is None:
        raise errors.AuthError('Invalid session')
    else:
        session.token = None
        DB.session.commit()
        result['success'] = 'Token expired'

    return jsonify(result)

@APP.route('/update-session', methods=['POST'])
def update_session():
    """
    Updates a teams auth token from an old one to a new one.

    :param old_token: the old auth token, must be valid
    :param new_token: the new token to be set

    :returns result: json dict containg either a success or a error
    """
    result = dict()
    data = request.get_json()
    if data is None:
        data = request.form

    old_token = data['old_token']
    new_token = data['new_token']
    session = Session.query.filter_by(token=old_token).first()
    if session is None:
        raise errors.AuthError('Invalid session')
    else:
        session.token = new_token
        DB.session.commit()
        result['success'] = 'Token updated'

    return jsonify(result)

@APP.route('/transactions', methods=['POST'])
def transactions():
    """
    Get a list of transactions made by the account

    :param token: the auth token for the account

    :returns result: json dict containing either an array of the transactions or an error.
    """
    pass


## HELPER FUNCTIONS

def new_session(uuid, token, src):
    """
    Enters a new session for a user

    :param uuid: the users id
    :param token: the token to attach to their session
    :param src: the source ip of the request
    """
    now = time.time()
    session = Session.query.filter_by(uuid=uuid).first()
    session.token = token
    session.time = now
    session.src = src
    DB.session.commit()
