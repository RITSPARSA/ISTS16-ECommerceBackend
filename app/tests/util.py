"""
    Util functions and class for each test to use
"""
import json
import unittest
from app import APP

class ApiTestCases(unittest.TestCase):
    """Collection of unit tests for the different API endpoints"""

    def setUp(self):
        """
        Set up our testing client
        """
        APP.testing = True
        self.app = APP.test_client()

    def login(self, username, password):
        """
        Helper function to log in

        :param username: username of the team
        :param password: passsword of the team

        :return result: the result of the login post request
        """
        token = username + password
        data = dict(username=username, password=password, token=token)

        result = self.app.post('/login', data=data)
        assert result.status_code == 200

        return token

    def get_balance(self, token):
        """
        Helper function to get account balance

        :param token: auth token for the account

        :returns balance: balance of the account
        """
        data = dict(token=token)
        result = self.app.post('/get-balance', data=data)
        result = json.loads(result.data)
        return result['balance']
