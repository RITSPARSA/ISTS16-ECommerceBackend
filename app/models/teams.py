"""
    Document to represent a team
"""
from app import DB

class Team(DB.Model):
    """
    Represents a team in our database

    :param uuid: the id of the team
    :param username: the username of the team
    :param password: the teams password
    :param balance: the balance of their account
    :param pub_key: public key for the jenkins builds
    :param private_key: key to identify teams
    :param ship_one: number of the first ship
    :param ship_two: number of the second ship
    :param ship_three: number of third ship
    """
    __tablename__ = 'teams'
    uuid = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(64))
    password = DB.Column(DB.String(64))
    balance = DB.Column(DB.Float())
    pub_key = DB.Column(DB.String(2048))
    private_key = DB.Column(DB.String(2048))
    ship_one = DB.Column(DB.Integer)
    ship_two = DB.Column(DB.Integer)  
    ship_three = DB.Column(DB.Integer)


    def __init__(self, uuid, username, password, balance, pub_key, private_key,
                 ship_one=0, ship_two=0, ship_three=0):
        self.uuid = uuid
        self.username = username
        self.password = password
        self.balance = balance
        self.pub_key = pub_key
        self.private_key = private_key
        self.ship_one = ship_one
        self.ship_two = ship_two
        self.ship_three = ship_three

    def __repr__(self):
        return '<Team uuid={} balance={}>'.format(self.uuid, self.balance)
