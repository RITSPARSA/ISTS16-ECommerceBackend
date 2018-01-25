"""
Configuration settings.
"""
import os
import logging
import sys

class InfoFilter(logging.Filter):
    def filter(self, rec):
        return rec.levelno == logging.INFO

class ErrorFilter(logging.Filter):
    def filter(self, rec):
        return rec.levelno == logging.ERROR

AUTH_API_URL = "http://lilbite.org:9000"

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
            'filename':  '/home/dosh/ISTS16-Backend/app/logs/info.log',
            'mode': 'a',
            'backupCount': '16',
            'filters': ['info_filter']
        },
        'error': {
            'level': 'ERROR',
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename':  '/home/dosh/ISTS16-Backend/app/logs/error.log',
            'mode': 'a',
            'backupCount': '16',
            'filters': ['error_filter']
        },
    },
    'loggers': {
        'api_log': {'handlers': ['info', 'error'], 'level': 'DEBUG', 'propagate': False},
    }
}

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
    },
    {
        'name': 'Red teamer hands off keyboard for 10 minutes',
        'price': 100
    },
    {
        'name': 'Red team advice',
        'price': 100
    },
    {
        'name': 'White team advice',
        'price': 100
    },
    {
        'name': 'Snapshot',
        'price': 100
    },
    {
        'name': 'Fresh config file for a server',
        'price': 100
    },
    {
        'name': "Turn off another team's power",
        'price': 100
    },
    {
        'name' : 'Spaceships',
        'price': 100
    },
    {
        'name': 'Upgrade your colony',
        'price': 100
    },
    {
        'name': 'Backdoor into the KOTH VMs',
        'price': 100
    },
    {
        'name': 'Back door into other teams servers',
        'price': 100
    },
    {
        'name': 'Power Bill',
        'price': 100
    }
]
