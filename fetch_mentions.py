import time
import requests
import json
from datetime import datetime

import tweepy
from tweepy.error import TweepError
from raven import Client

from settings import consumer_key, consumer_secret, key, secret, count, pubKey, payload_type, SENTRY_DSN,\
    overlap_count, waiting_period, speed_layer_endpoint_url, password, timeout, ssl_verification,\
    twitter_app_name, twitter_app_id, instance_id

client = Client(SENTRY_DSN)


class GetMentions(object):
    latest_tweet_id = 0
    since_id = 1
    api = None
    data = {"payloadType": payload_type, "pubKey": pubKey}
    overlap_count = overlap_count
    headers = {'content-type': 'application/json'}
    query_data = {"type": "get_mentions"}
    sensor = {"appName": twitter_app_name, "appId": twitter_app_id, "instanceId": instance_id}

    def authenticate(self):
        """
        Authenticate twitter credentials
        """
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(key, secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    def verify_credentials(self):
        """
        Return after Verifying twitter credentials
        """
        print "Verifying twitter auth"
        try:
            verified = self.api.verify_credentials()
        except TweepError, errors:
            client.captureException()
            print errors.message
            return False
        else:
            self.sensor.update({"appAccount": verified.screen_name})
            return verified

    def get_mentions(self):
        """
        Fetch mentions from twitter
        """
        try:
            print "Fetching mentions"
            self.query_data.update({"dateTime": datetime.utcnow().isoformat()})
            mentions = self.api.mentions_timeline(count=count, since_id=self.since_id)
            self.query_data.update({"argument": {"count": count, "since_id": self.since_id}})
        except TweepError, errors:
            client.captureException()
            print errors.message
            return []
        else:
            return mentions

    def process_mentions(self):
        """
        Send the twitter mentions to rest end point server
        """
        transaction_data = {}
        transaction_data['sensor'] = self.sensor
        mentions = self.get_mentions()
        for mention in mentions:
            transaction_data['rawData'] = mention._json
            transaction_data['query'] = self.query_data
            self.data.update({"transactionId": mention.id, "transactionSent": mention.created_at.isoformat(),
                              "transactionData": transaction_data})
            print "--------- Sending to Rest End point ---------"
            print json.dumps(self.data)
            print "---------------------------------------------"
            try:
                resp = requests.post(url, auth=(pubKey, password), headers=self.headers, timeout=timeout,
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
