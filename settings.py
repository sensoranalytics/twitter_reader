# Count of tweets to fetch in one go, Max 200 will work for mentions
count = 200

# to test the duplicate checking feature, will force to get duplicate tweets
overlap_count = 0

payload_type = "tweet"

# Waiting period between each api call in seconds
waiting_period = 60

ssl_verification = True

# request timeout
timeout = 20

try:
    from local import *
except ImportError:
    pass
