"""
    Main test file
"""
import unittest
from app import APP


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

        return self.app.post('/login', data=data)

    def test_login(self):
        """
        Test the login functionality of our app
        """
        result = self.login('testuser', 'testpass')
        assert result.status_code == 200

    def test_balance(self):
        """
        Test if we can get the balance of a user
        """
        self.login('testuser', 'testpass')
        data = dict(token='testusertestpass')
        result = self.app.post('/get-balance', data=data)
        assert result.status_code == 200
        assert 'balance' in result.data

    def test_expire_session(self):
        """
        Test if expiring a session functions correctly
        """
        self.login('testuser', 'testpass')
        data = dict(token='testusertestpass')
        result = self.app.post('/expire-session', data=data)
        assert result.status_code == 200
        
        # try to access endpoint after token expired, should fail
        result = self.app.post('/get-balance', data=data)
        assert result.status_code == 403

    def test_update_token(self):
        """
        Test if you can update a token
        """
        self.login('testuser', 'testpass')
        data = dict(old_token='testusertestpass', new_token='heythere')
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


if __name__ == '__main__':
    unittest.main()
