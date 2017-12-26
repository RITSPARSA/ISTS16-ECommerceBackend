"""
Configuration settings.
"""
import os
import sys

SQLALCHEMY_DATABASE_URI = 'mysql://root:youwontguess23$@localhost/ists'

LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(message)s'
        },
    },
    'handlers': {
        'info': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename':  os.path.join(sys.path[0], 'app/logs/info.log'),
            'mode': 'a',
            'backupCount': '16'
        },
        'error': {
            'level': 'ERROR',
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename':  os.path.join(sys.path[0], 'app/logs/error.log'),
            'mode': 'a',
            'backupCount': '16'
        },
    },
    'loggers': {
        'info_log': {'handlers': ['info'], 'level': 'INFO', 'propagate': False},
        'error_log': {'handlers': ['error'], 'level': 'ERROR', 'propagate': False},
    }
}
