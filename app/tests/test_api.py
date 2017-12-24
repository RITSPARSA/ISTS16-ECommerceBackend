import unittest
from app import APP, views


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
        result = self.app.post('/get-balance', data=data)
        assert result.status_code == 403


if __name__ == '__main__':
    unittest.main()
