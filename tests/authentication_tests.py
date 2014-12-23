import unittest

import tweepy

from settings import consumer_key, consumer_secret, key, secret
from fetch_mentions import GetMentions


class AuthenticationTestCase(unittest.TestCase):
    """
    Test Cases for twitter authentication
    """

    def authenticate(self, *args):
        """
        Authenticate twitter credentials
        """
        auth = tweepy.OAuthHandler(args[0], args[1])
        auth.set_access_token(args[2], args[3])
        api = tweepy.API(auth)
        return api

    def test_twitter_successful_authentication(self):
        """
        Test Case for successful twitter authentication
        """
        obj = GetMentions()
        obj.authenticate()
        self.assertIsNot(False, obj.verify_credentials())

    def test_twitter_consumer_key_failure(self):
        """
        Test Case for failed twitter authentication when provided with wrong consumer key
        """
        wrong_consumer_key = "wrong key"
        api = self.authenticate(wrong_consumer_key, consumer_secret, key, secret)
        obj = GetMentions()
        obj.api = api
        self.assertFalse(obj.verify_credentials())

    def test_twitter_consumer__secret_key_failure(self):
        """
        Test Case for failed twitter authentication when provided with wrong consumer secret key
        """
        wrong_consumer_secret = "wrong key"
        api = self.authenticate(consumer_key, wrong_consumer_secret, key, secret)
        obj = GetMentions()
        obj.api = api
        self.assertFalse(obj.verify_credentials())

    def test_twitter_access_token_failure(self):
        """
        Test Case for failed twitter authentication when provided with wrong token
        """
        wrong_key = "wrong key"
        api = self.authenticate(consumer_key, consumer_secret, wrong_key, secret)
        obj = GetMentions()
        obj.api = api
        self.assertFalse(obj.verify_credentials())

    def test_twitter_access_token_secret_key_failure(self):
        """
        Test Case for failed twitter authentication when provided with wrong token secret key
        """
        wrong_secret_key = "wrong key"
        api = self.authenticate(consumer_key, consumer_secret, key, wrong_secret_key)
        obj = GetMentions()
        obj.api = api
        self.assertFalse(obj.verify_credentials())

if __name__ == '__main__':
    unittest.main()
