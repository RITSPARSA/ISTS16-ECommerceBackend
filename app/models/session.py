"""
    Document to represent a users session
"""
from app import DB

class Session(DB.Model):
    """
    Represents a users session

    :param id: the id of the user (the team number)
    :param token: there unique session id
    :param time: the timestamp this session was created
    :param src: the src ip that initiated this session
    """

    __tablename__ = 'session'
    uuid = DB.Column(DB.Integer, primary_key=True)
    token = DB.Column(DB.String(128))
    time = DB.Column(DB.Float())
    src = DB.Column(DB.String(16))

    def __init__(self, uuid=None, token=None, time=None, src=None):
        self.uuid = uuid
        self.token = token
        self.time = time
        self.src = src

    def __repr__(self):
        return '<Session id={} token={} time={} ip={}>'.format(self.uuid, self.token, self.time, self.src)
