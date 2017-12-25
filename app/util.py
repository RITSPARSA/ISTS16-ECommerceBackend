"""
    File to hold utility functions
"""
import time
from . import APP, DB
from .models.session import Session
from .models.users import Users
from .models.transaction import Transaction
from .models.item import Item
from . import errors


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

def get_item_price(item_id):
    """
    Returns the price of an item from the database

    :param item_id: id of the item

    :returns price: price of the item
    """
    item = Item.query.filter_by(uuid=item_id).first()
    if item is None:
        raise errors.TransactionError("Item not found", status_code=404)

    return item.price

def validate_request(params, data):
    """
    Verifies all the required parameters are in the request

    :param params: an array of the required parameters
    :param data: the json data in the post request
    """
    for p in params:
        if p not in data:
            raise errors.RequestError("Missing {}".format(p), status_code=400)

    return True
