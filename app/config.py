"""
Configuration settings.
"""
import os
import logging
import sys
import string
import random

class InfoFilter(logging.Filter):
    def filter(self, rec):
        return rec.levelno == logging.INFO

class ErrorFilter(logging.Filter):
    def filter(self, rec):
        return rec.levelno == logging.ERROR

NUMBER_OF_TEAMS = 12
DEFAULT_PASSWORD = 'Changeme-2018'
DEFAULT_BALANCE = 1000
DEFAULT_PINS = [''.join(random.choice(string.digits) for _ in range(4))
                for _ in range(NUMBER_OF_TEAMS + 1)]
SQLALCHEMY_DATABASE_URI = 'mysql://root:youwontguess23$@localhost/ists'

LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(message)s'
        },
    },
    'filters': {
        'info_filter': {
            '()': InfoFilter,
        },
        'error_filter': {
            '()': ErrorFilter,
        }
    },
    'handlers': {
        'info': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename':  '/var/www/ISTS16-Backend/app/logs/info.log',
            'mode': 'a',
            'backupCount': '16',
            'filters': ['info_filter']
        },
        'error': {
            'level': 'ERROR',
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename':  '/var/www/ISTS16-Backend/app/logs/error.log',
            'mode': 'a',
            'backupCount': '16',
            'filters': ['error_filter']
        },
    },
    'loggers': {
        'api_log': {'handlers': ['info', 'error'], 'level': 'DEBUG', 'propagate': False},
    }
}

TEAMS = [x for x in range(1, NUMBER_OF_TEAMS+1)]

ITEMS = [
    {
        'name': 'MICAH HUG',
        'price': 10
    },
    {
        'name': 'JOES LOVE',
        'price': 69
    },
    {
        'name': 'DON RANT',
        'price': 200
    }
]
