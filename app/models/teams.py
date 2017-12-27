"""
    Document to represent a team
"""
from app import DB

class Team(DB.Model):
    """
    Represents a team in our database

    :param id: the id of the team
    :param username: the username of the team
    :param password: the teams password
    :param balance: the balance of their account
    :param pin: the pin to access their bank account
    """
    __tablename__ = 'teams'
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
        return '<Team id={} balance={}>'.format(self.uuid, self.balance)
