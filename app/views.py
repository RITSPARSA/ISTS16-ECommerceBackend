"""
    Entry point for API calls
"""
from . import APP
from .models.session import Session
from .models.users import Users
from flask import request, jsonify, render_template