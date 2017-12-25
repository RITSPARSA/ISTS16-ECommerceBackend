"""
    Document to represent an item in the store
"""
from app import DB

class Item(DB.Model):
    """
    Represents a item

    :param uuid: the id of the item
    :param price: how much the item is worth
    """

    __tablename__ = 'items'
    uuid = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    price = DB.Column(DB.Integer)

    def __init__(self, price=None):
        self.price = price

    def __repr__(self):
        return '<Item id={} price={}>'.format(self.uuid, self.price)
