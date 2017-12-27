"""
    Create our database and fill it with the starting data
"""
from app import DB
from app.models.teams import Team
from app.models.session import Session
from app.models.transaction import Transaction
from app.models.item import Item
from app.config import TEAMS, ITEMS, DEFAULT_PASSWORD, DEFAULT_BALANCE, DEFAULT_PINS
DB.create_all()

print "Adding teams..."
for team, pin in zip(TEAMS, DEFAULT_PINS):
    new_team = Team(uuid=team, username='team{}'.format(team),
                    password=DEFAULT_PASSWORD, balance=DEFAULT_BALANCE,
                    pin=pin)

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
