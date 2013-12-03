"""
Programming Group week 09 - Reading raw tweets from file (such as those stored from a
streaming collection)

Tweets      -   https://dev.twitter.com/docs/platform-objects/tweets
OpenHeatMap -   http://www.openheatmap.com/

@auth dpb
@date 12/02/2013
"""

import simplejson as json
from json_util import ConcatJSONDecoder


# STEP 1: Read tweets in from file and store in a list of tweets
# There's a trick here... just use this ConcatJSONDecoder tool (can also do it line-by-line)
tweetfile = "UkraineGeoTweets.json.txt"
handle = open(tweetfile)
tweets = json.loads(handle.read(), cls=ConcatJSONDecoder)
handle.close()

# Line-by-line looks like this:
handle = open(tweetfile)
tweets = []
for line in handle:
    tweet = json.loads(line.rstrip())
    tweets.append(tweet)
handle.close()


# Super secret answers below. We want to:
# 1 - Loop over all tweets
# 2 - Check if each tweet is in fact a tweet
# 3 - Check for Language, Place, and Geocoded data
# 4 - Store each of Language occurrence, Country occurrence, and Coordinates
# 5 - Write each of these to very simple CSV files


