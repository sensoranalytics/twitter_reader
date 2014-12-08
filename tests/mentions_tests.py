import unittest

from fetch_mentions import GetMentions


class TwitterMentionsTestCase(unittest.TestCase):
    """
    Test Cases for twitter mentions
    """

    def test_twitter_mentions(self):
        """
        Test Case for fetching twitter mentions
        """
        obj = GetMentions()
        obj.authenticate()
        mentions = obj.get_mentions()
        self.assertIsNot(mentions, None)
