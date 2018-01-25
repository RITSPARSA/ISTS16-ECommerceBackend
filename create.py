"""
    Create our database and fill it with the starting data
"""
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from app import DB
from app.models.teams import Team
from app.models.session import Session
from app.models.transaction import Transaction
from app.models.item import Item
from app.config import TEAMS, ITEMS, DEFAULT_PASSWORD, DEFAULT_BALANCE
DB.create_all()

print "Adding teams..."
for team in TEAMS:
    key = rsa.generate_private_key(
        backend=default_backend(),
        public_exponent=65537,
        key_size=2048
    )
    private_key = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption())

    public_key = key.public_key().public_bytes(
        serialization.Encoding.OpenSSH,
        serialization.PublicFormat.OpenSSH
    )

    print private_key
    print public_key

    new_team = Team(uuid=team, username='team{}'.format(team),
                    password=DEFAULT_PASSWORD, balance=DEFAULT_BALANCE,
                    pub_key=public_key, private_key=private_key)

    new_session = Session(uuid=team)

    DB.session.add(new_team)
    DB.session.add(new_session)

print 'Done'
print 'Adding items...'
for item in ITEMS:
    new_item = Item(name=item['name'], price=item['price'])
    DB.session.add(new_item)

print 'Done'
DB.session.commit()
