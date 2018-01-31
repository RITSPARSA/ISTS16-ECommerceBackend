"""
    Entry point for API calls
"""
from flask import request, jsonify, abort
from sqlalchemy import or_
from . import APP, DB, logger
from .models.teams import Team
from .models.transaction import Transaction
from .models.item import Item
from . import errors
from .util import validate_request, validate_session, post_slack


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
    team_id = validate_session(token)

    user = Team.query.filter_by(uuid=team_id).first()
    balance = user.balance
    result['balance'] = balance
    result['team_id'] = team_id
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
    team_id = validate_session(token)
    user = Team.query.filter_by(uuid=team_id).first()
    item = Item.query.filter_by(uuid=item_id).first()
    if item is None:
        raise errors.TransactionError('Item not be found', status_code=404)

    balance = user.balance
    if balance < item.price:
        raise errors.TransactionError('Insufficient funds')

    user.balance -= item.price
    # create our tranasction
    # dst = 0 because 0 is white team
    description = "{} bought {} from shop".format(user.username, item.name)
    tx = Transaction(src=user.uuid, dst=0,
                     desc=description, amount=item.price)
    DB.session.add(tx)
    DB.session.commit()
    post_slack(description)
    result['transaction_id'] = tx.uuid

    logger.info("Team %d bought item %s - [tx id: %d]", user.uuid, item.name, tx.uuid)
    return jsonify(result)


@APP.route('/transactions', methods=['POST'])
def transactions():
    """
    Get a list of transactions made by the team

    :param token: the auth token for the team

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
    team_id = validate_session(token)

    user = Team.query.filter_by(uuid=team_id).first()
    txs = Transaction.query.filter(or_(Transaction.src == user.uuid, Transaction.dst == user.uuid))
    for t in txs:
        tx_dict = t.__dict__
        del tx_dict['_sa_instance_state']
        result['transactions'].append(tx_dict)

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
    amount = float(data['amount'])
    token = data['token']
    team_id = validate_session(token)
    user = Team.query.filter_by(uuid=team_id).first()
    dst_user = Team.query.filter_by(uuid=dst_id).first()
    if dst_user is None:
        raise errors.TeamError("Team id not found", status_code=404)

    print amount
    print user.balance
    if user.balance < amount:
        raise errors.TransactionError('Insufficient funds')

    # transfer the funds
    user.balance -= amount
    dst_user.balance += amount

    # dst = 0 because 0 is white team
    tx = Transaction(src=user.uuid, dst=dst_id,
                     desc="transfer to team {}".format(dst_id), amount=amount)
    DB.session.add(tx)
    DB.session.commit()

    logger.info("Team %d transfered %f$ to Team %d - [tx id: %d]",
                int(user.uuid), amount, int(dst_id), int(tx.uuid))
    result['transaction_id'] = tx.uuid
    return jsonify(result)


@APP.route('/items', methods=['POST'])
def get_items():
    """
    Items and their price from the white team store

    :return result: json dict containg either the id of the transaction or an error
    """
    result = dict()
    result['items'] = []
    items = Item.query.all()
    for i in items:
        item_dict = dict()
        item_dict['name'] = i.__dict__['name']
        item_dict['price'] = i.__dict__['price']
        item_dict['uuid'] = i.__dict__['uuid']
        result['items'].append(item_dict)

    return jsonify(result)
