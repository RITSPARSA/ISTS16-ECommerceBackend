"""
    Document to represent a transactions
"""
from app import DB

class Transaction(DB.Model):
    """
    Represents a transaction

    :param uuid: the id of the transaction
    :param time: the timestamp this session was created
    :param src: who initiated the transaction
    :param dst: who the transaction is to
    :param desc: a description of the transaction
    :param amount: the amount the transaction is for
    """

    __tablename__ = 'transactions'
    uuid = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    time = DB.Column(DB.Float())
    src = DB.Column(DB.Integer)
    dst = DB.Column(DB.Integer)
    desc = DB.Column(DB.String(128))
    amount = DB.Column(DB.Integer)


    def __init__(self, time=None, src=None, dst=None, desc=None, amount=None):
        self.time = time
        self.src = src
        self.dst = dst
        self.desc = desc
        self.amount = amount

    def __repr__(self):
        return '<Transaction id={} time={} src={} dst={} amount={} desc={}>'.format(
            self.uuid, self.time, self.src, self.dst, self.amount, self.desc)
