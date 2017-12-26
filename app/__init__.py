"""
    Initialize our database and flask app
"""
import logging.config
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .config import SQLALCHEMY_DATABASE_URI, LOG_CONFIG

# Set up our logger
logging.config.dictConfig(LOG_CONFIG)
logging.getLogger().setLevel(logging.DEBUG)
logger = logging.getLogger('api_log')


APP = Flask(__name__)

try:
    print "Establishing database connection"
    APP.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB = SQLAlchemy(APP)

except Exception as e:
    print e
    print "ERROR: Could not connect to database"
    sys.exit()

from .views import *
