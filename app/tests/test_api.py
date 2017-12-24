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
        print result
        assert result.status_code == 200

if __name__ == '__main__':
    unittest.main()
