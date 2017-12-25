from app import DB
from app.models.users import Users
from app.models.session import Session
from app.models.transaction import Transaction
from app.models.item import Item
DB.create_all()