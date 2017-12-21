"""
    Entry point for API calls
"""
from . import APP as app
from .models.session import Session
from .models.users import Users
from flask import request, jsonify, render_template

@app.route('/login', methods=['POST'])
def login():
    """
    Verifies if a the submitted credentials are correct

    :param username: username of the team
    :param password: teams password
    :param token: the auth token to be attached to this account

    :returns result: json dict containing either a success or and error
    """
    pass

@app.route('/get-balance', methods=['POST'])
def get_balance():
    """
    Gets the balance of a team

    :param token: the auth token for that team

    :returns result: json dict containing either the account balance or an error
    """
    pass

@app.route('/buy', methods=['POST'])
def buy():
    """
    Buys a item from the white team store

    :param token: the auth token for the team
    :param item_id: the id of the item to buy

    :return result: json dict containg either the id of the transaction or an error
    """
    pass

@app.route('/expire-session', methods=['POST'])
def expire_session():
    """
    Set a teams auth token to NULL, essentially expiring their session

    :param token: the authentication token to expire, must be valid

    :return result: json dict containing either a success or an error
    """
    pass

@app.route('/update-session', methods=['POST'])
def update_session():
    """
    Updates a teams auth token from an old one to a new one.

    :param old_token: the old auth token, must be valid
    :param new_token: the new token to be set

    :returns result: json dict containg either a success or a error
    """
    pass

@app.route('/transactions', methods=['POST'])
def transactions():
    """
    Get a list of transactions made by the account

    :param token: the auth token for the account

    :returns result: json dict containing either an array of the transactions or an error.
    """
    pass
