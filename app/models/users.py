"""
    Document to represent a user/team
"""
from app import DB

class Users(DB.Model):
    """
    Represents a user (team) in our database

    :param id: the id of the user (team number)
    :param username: the username of the user (team)
    :param password: the users password
    :param balance: the balance of their account
    :param pin: the pin to access their bank account
    """
    __tablename__ = 'users'
    uuid = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(64))
    password = DB.Column(DB.String(64))
    balance = DB.Column(DB.Float())
    pin = DB.Column(DB.Integer)

    def __init__(self, uuid, username, password, balance, pin):
        self.uuid = uuid
        self.username = username
        self.password = password
        self.balance = balance
        self.pin = pin

    def __repr__(self):
        return '<User id={} balance={}>'.format(self.uuid, self.balance)
