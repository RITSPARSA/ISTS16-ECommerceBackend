"""
    Entry point for API calls
"""
import time
from flask import request, jsonify, abort
from sqlalchemy import or_
from . import APP, DB, info_log, error_log
from .models.session import Session
from .models.users import Users
from .models.transaction import Transaction
from .models.item import Item
from . import errors
from .util import new_session, validate_request


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
        if data is None:
            abort(400)

    # make sure we have all the correct parameters
    params = ['username', 'token', 'password']
    validate_request(params, data)

    username = data['username']
    password = data['password']
    token = data['token']

    user = Users.query.filter_by(username=username, password=password).first()
    if user is None:
        raise errors.AuthError('Invalid username or password')

    new_session(user.uuid, token, request.remote_addr)
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
        if data is None:
            abort(400)

    # make sure we have all the correct parameters
    params = ['token']
    validate_request(params, data)

    token = data['token']
    session = Session.query.filter_by(token=token).first()
    if session is None:
        raise errors.AuthError('Invalid session')

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
    result = dict()
    data = request.get_json()
    if data is None:
        data = request.form
        if data is None:
            abort(400)

    # make sure we have all the correct parameters
    params = ['token', 'item_id']
    validate_request(params, data)

    token = data['token']
    item_id = data['item_id']
    session = Session.query.filter_by(token=token).first()
    if session is None:
        raise errors.AuthError('Invalid session')

    user = Users.query.filter_by(uuid=session.uuid).first()
    item = Item.query.filter_by(uuid=item_id).first()
    if item is None:
        raise errors.TransactionError('Item not be found', status_code=404)

    balance = user.balance
    if balance < item.price:
        raise errors.TransactionError('Insufficient funds')

    user.balance -= item.price
    # create our tranasction
    now = time.time()
    # dst = 0 because 0 is white team
    tx = Transaction(time=now, src=user.uuid, dst=0,
                     desc="bought item from shop", amount=item.price)
    DB.session.add(tx)
    DB.session.commit()
    result['transaction_id'] = tx.uuid

    return jsonify(result)

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
        if data is None:
            abort(400)

    # make sure we have all the correct parameters
    params = ['token']
    validate_request(params, data)

    token = data['token']
    session = Session.query.filter_by(token=token).first()
    if session is None:
        raise errors.AuthError('Invalid session')

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
        if data is None:
            abort(400)

    # make sure we have all the correct parameters
    params = ['old_token', 'new_token']
    validate_request(params, data)

    old_token = data['old_token']
    new_token = data['new_token']
    session = Session.query.filter_by(token=old_token).first()
    if session is None:
        raise errors.AuthError('Invalid session')

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
    result = dict()
    result['transactions'] = []
    data = request.get_json()
    if data is None:
        data = request.form
        if data is None:
            abort(400)

    # make sure we have all the correct parameters
    params = ['token']
    validate_request(params, data)

    token = data['token']
    session = Session.query.filter_by(token=token).first()
    if session is None:
        raise errors.AuthError('Invalid session')

    user = Users.query.filter_by(uuid=session.uuid).first()
    txs = Transaction.query.filter(or_(Transaction.src == user.uuid, Transaction.dst == user.uuid))
    for t in txs:
        result['transactions'].append(str(t.__dict__))

    return jsonify(result)

@APP.route('/transfer', methods=['POST'])
def transfers():
    """
    Transfer money from one teams account to another

    :param token: the auth token for the account
    :param recipient: the id of the team to send the funds to
    :param amount: amount to transfer
    :returns result: json dict containing the transaction id or an error
    """
    result = dict()
    data = request.get_json()
    if data is None:
        data = request.form
        if data is None:
            abort(400)

    # make sure we have all the correct parameters
    params = ['recipient', 'token', 'amount']
    validate_request(params, data)

    dst_id = data['recipient']
    amount = data['amount']
    token = data['token']

    session = Session.query.filter_by(token=token).first()
    if session is None:
        raise errors.AuthError('Invalid session')

    user = Users.query.filter_by(uuid=session.uuid).first()
    dst_user = Users.query.filter_by(uuid=dst_id).first()
    if dst_user is None:
        raise errors.TeamError("Team id not found", status_code=404)

    if user.balance < amount:
        raise errors.TransactionError('Insufficient funds')

    # transfer the funds
    user.balance -= amount
    dst_user.balance += amount

    # add the transaction
    now = time.time()
    # dst = 0 because 0 is white team
    tx = Transaction(time=now, src=user.uuid, dst=dst_id,
                     desc="transfer to team {}".format(dst_id), amount=amount)
    DB.session.add(tx)
    DB.session.commit()

    result['transaction_id'] = tx.uuid
    return jsonify(result)
