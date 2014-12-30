# Count of tweets to fetch in one go, Max 200 will work for mentions.
# See https://dev.twitter.com/rest/public/rate-limiting for more.
count = 200

# Setting overlap_count to any value > 0 will cause the sensor to read N duplicate tweets (where N = overlap_count)
# on every poll to Twitter. "Real life" sensors frequently send duplicate data. "Real life" Lambda Architectures see
# this behavior as well.
#
# Savi's IOT Adapter screens out duplicate data to protect against this. To see this duplicate filtering in action 
# set overlap_count to a value that would cause about ~8-16% duplicates (to simulate a hardware sensor), 
# or at ~1-3% (to simulate a Lambda feed).
overlap_count = 0

payload_type = "tweet" # SMF payload type for type-based routing to data mapping and aggregation topologies

# Waiting period between each api call in seconds
waiting_period = 60

ssl_verification = True

# request timeout
timeout = 20

# Developer Note:
# In general, use of 'import *' is a no-no. However, in this case we are using it to import a bound, very small
# set of configuration variables, either from local.py (either set by the repo or the automated deployment tool.
# As such, it is ok here.
try:
    from local import *
except ImportError:
    pass
