import time
import requests
import json

import tweepy
from tweepy.error import TweepError
from raven import Client

from settings import consumer_key, consumer_secret, key, secret, count, pubKey, payload_type, SENTRY_DSN,\
    overlap_count, waiting_period, speed_layer_endpoint_url, password, timeout, ssl_verification

client = Client(SENTRY_DSN)


class GetMentions(object):
    latest_tweet_id = 1
    since_id = 1
    api = None
    data = {"payloadType": payload_type, "pubKey": pubKey}
    overlap_count = overlap_count
    headers = {'content-type': 'application/json'}

    def authenticate(self):
        """
        Authenticate twitter credentials
        """
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(key, secret)
        self.api = tweepy.API(auth)

    def verify_credentials(self):
        """
        Return after Verifying twitter credentials
        """
        try:
            verified = self.api.verify_credentials()
        except TweepError, errors:
            client.captureException()
            for msg in errors.message:
                # If Rate limit exceeded, will retry after 15 minutes
                if msg['code'] == 88:
                    print "Sleeping for 15 minutes, Rate limit hit"
                    time.sleep(15 * 60)
                    return True
            return False
        else:
            return verified

    def get_mentions(self):
        """
        Fetch mentions from twitter
        """
        try:
            print "Fetching mentions"
            mentions = self.api.mentions_timeline(count=count, since_id=self.since_id)
        except TweepError, errors:
            client.captureException()
            for msg in errors.message:
                # If Rate limit exceeded, will retry after 15 minutes
                if msg['code'] == 88:
                    print "Sleeping for 15 minutes, Rate limit hit"
                    time.sleep(15 * 60)
                    break
                print msg
            return []
        else:
            return mentions

    def process_mentions(self):
        """
        Send the twitter mentions to rest end point server
        """
        mentions = self.get_mentions()
        for mention in mentions:
            self.data.update({"transactionId": mention.id, "transactionSent": mention.created_at.isoformat(),
                              "transactionData": mention._json})
            print "--------- Sending to Rest End point ---------"
            try:
                resp = requests.post(speed_layer_endpoint_url, auth=(pubKey, password), headers=self.headers, timeout=timeout,
                                     data=json.dumps(self.data), verify=ssl_verification)
            except Exception as e:
                print 'Failed to post to HTTP endpoint due to "%s"' % e.message
            if mention.id > self.latest_tweet_id:
                # get highest tweet id so that it could be used as since_id later
                self.latest_tweet_id = mention.id
                print "Latest mention ID so far: {0}".format(self.latest_tweet_id)
            print "Mentions Tweet ID: {0}".format(mention.id)
            print "Mentions Tweet: {0}".format(mention.text)

        if self.overlap_count:
            # Force duplicate tweets
            try:
                self.since_id = mentions[-1 * (overlap_count + 1)].id
            except IndexError:
                print "Mentions overlap index out of range"
                client.captureException()
                self.since_id = self.latest_tweet_id
        else:
            self.since_id = self.latest_tweet_id


if __name__ == "__main__":
    obj = GetMentions()
    obj.authenticate()
    while obj.verify_credentials():
        obj.process_mentions()
        print "Waiting for %s seconds" % waiting_period
        time.sleep(waiting_period)
    else:
        print "Verification Failed"
