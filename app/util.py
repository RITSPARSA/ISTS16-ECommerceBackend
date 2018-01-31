"""
    File to hold utility functions
"""
import requests
from .config import AUTH_API_URL, SLACK_URI, CHANNEL, SLACK_USERNAME, ICON_EMOJI
from .models.item import Item
from .errors import RequestError, AuthError, TransactionError

def validate_session(token):
    """
    Sends token to auth server to validate, should recieve
    associated team number if it is valid

    :param token: the session token to validate

    :return team_id: the id of the team the token is attached to
    """
    post_data = dict()
    post_data['token'] = token
    resp = auth_api_request('validate-session', post_data)
    if 'success' not in resp:
        raise AuthError(resp['error'])

    team_id = resp['success']
    return team_id

def auth_api_request(endpoint, data):
    """
    Makes a request to our api and returns the response

    :param endpoint: the api endpoint to hit
    :param data: the data to send in dictionary format
    :param url: the url of the api

    :returns resp: the api response
    """
    print data
    url = "{}/{}".format(AUTH_API_URL, endpoint)

    resp = requests.post(url, data=data)
    if resp.status_code == 400:
        raise RequestError("Bad request sent to API")

    if resp.status_code == 403:
        raise AuthError(resp.json()['error'])

    elif resp.status_code != 200:
        raise RequestError("API returned {} for /{}".format(
            resp.status_code, endpoint))

    resp_data = resp.json()
    return resp_data

def get_item_price(item_id):
    """
    Returns the price of an item from the database

    :param item_id: id of the item

    :returns price: price of the item
    """
    item = Item.query.filter_by(uuid=item_id).first()
    if item is None:
        raise TransactionError("Item not found", status_code=404)

    return item.price

def validate_request(params, data):
    """
    Verifies all the required parameters are in the request

    :param params: an array of the required parameters
    :param data: the json data in the post request
    """
    for p in params:
        if p not in data:
            raise RequestError("Missing {}".format(p), status_code=400)

    return True

def post_slack(message):
    """
    Posts a message to our white team slack

    :param message: the message to post to slack
    """
    post_data = dict({
        "text":  message,
        "channel": CHANNEL,
        "link_names": 1,
        "username": SLACK_USERNAME,
        "icon_emoji": ICON_EMOJI
    })
    requests.post(SLACK_URI, json=post_data)
