"""
    Main test file
"""
import json
import unittest
from app import APP, get_item_price

class ApiTestCases(unittest.TestCase):
    """
    Collection of unit tests for the different API endpoints
    """

    def setUp(self):
        """
        Set up our testing client
        """
        APP.testing = True
        self.app = APP.test_client()

    # executed after each test
    def tearDown(self):
        pass

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

    def test_login(self):
        """
        Test the login functionality of our app
        """
        result = self.login('testuser', 'testpass')
        assert result is not None

    def test_balance(self):
        """
        Test if we can get the balance of a user
        """
        token = self.login('testuser', 'testpass')
        balance = self.get_balance(token)
        assert balance is not None

    def test_expire_session(self):
        """
        Test if expiring a session functions correctly
        """
        token = self.login('testuser', 'testpass')
        data = dict(token=token)
        result = self.app.post('/expire-session', data=data)
        assert result.status_code == 200

        # try to access endpoint after token expired, should fail
        result = self.app.post('/get-balance', data=data)
        assert result.status_code == 403

    def test_update_token(self):
        """
        Test if you can update a token
        """
        token = self.login('testuser', 'testpass')
        data = dict(old_token=token, new_token='heythere')
        result = self.app.post('/update-session', data=data)
        assert result.status_code == 200

        # try to access endpoint with old token, should fail
        data['token'] = data['old_token']
        result = self.app.post('/get-balance', data=data)
        assert result.status_code == 403

        # try to access endpoint with new token, should succeed
        data['token'] = data['new_token']
        result = self.app.post('/get-balance', data=data)
        assert result.status_code == 200

    def test_buying_item(self):
        """
        Test if we can buy an item from the store
        """
        token = self.login('testuser', 'testpass')
        item_price = get_item_price(1)
        data = dict(token=token, item_id=1)
        current_balance = self.get_balance(token)

        result = self.app.post('/buy', data=data)
        print result.data

        # Verify we get the transaction id
        assert result.status_code == 200
        assert 'transaction_id' in result.data

        # verify the correct money was reducted from the account
        new_balance = self.get_balance(token)
        assert (current_balance - item_price) == new_balance


if __name__ == '__main__':
    unittest.main()
