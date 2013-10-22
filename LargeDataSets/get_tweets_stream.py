"""
Simple script to access the twitter streaming API to fetch tweets (by certain filters). The script
uses the following resources:

Twitter Dev. Streaming API          https://dev.twitter.com/docs/streaming-apis
Tweepy, a python Twitter package    https://pypi.python.org/pypi/tweepy/
                                    http://pythonhosted.org/tweepy/html/
                                    https://github.com/tweepy/tweepy

Twitter Streaming filter params     https://dev.twitter.com/docs/api/1.1/post/statuses/filter
Good tutorial                       http://www.pythoncentral.io/introduction-to-tweepy-twitter-for-python/

@auth dpb
@date 10/20/2013
"""

import tweepy
import simplejson as json


# Go to http://dev.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key = "YOUR CONSUMER KEY"
consumer_secret = "YOUR CONSUMER SECRET"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token = "YOUR ACCESS TOKEN"
access_secret = "YOUR ACCESS TOKEN SECRET"


class StdOutListener(tweepy.streaming.StreamListener):
    """
    A basic listener class that inherits from Tweepy's StreamListener.
    
    REVIEW THE STREAMLISTENER CLASS for all functionality:
        https://github.com/tweepy/tweepy/blob/master/tweepy/streaming.py

    Can override certain methods to obtain certain behavior. The basic stream listener
    handles data best. Note that 'status' really means 'tweet' (annoyingly)
    """
    def on_connect(self):
        """Called when connected to stream, before data read loop starts"""
        print "Connected to a tweet stream!"

    def on_data(self, raw_data):
        """Called when raw data is received from connection. Overridden to avoid tweepy parsing data"""
        data = json.loads(raw_data)

        if 'in_reply_to_status_id' in data:
            if self.on_status(data) is False:
                return False
        elif 'delete' in data:
            delete = data['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False
        elif 'limit' in data:
            if self.on_limit(data['limit']['track']) is False:
                return False
        elif 'disconnect' in data:
            if self.on_disconnect(data['disconnect']) is False:
                return False
        else:
            print "-!- Unknown message type: {0}".format(raw_data)

    def on_status(self, status):
        """Status is a tweet. Do something with it"""

        # Print tweet
        print_tweet(status)

        # Dump tweet to file (assuming you have a handle open somewhere...)
        # from bson.json_util import dumps; handle.write(dumps(tweet))

        # Push to a database? Yes.

    def on_limit(self, track):
        print "-!- Collection limit hit. {0} matching tweets not delivered".format(track)

    def on_error(self, status):
        print "-!- Error. Status: {0}".format(status)

    def on_disconnect(self, notice):
        print "-!- Disconnect recvd from Twitter. Reason: {0}".format(notice['reason'])
        return False


def print_tweet(tweet):
    if tweet['place'] != None:
        print "<Tweet: {0} | {1} | {2} | {3} | {4} | {5}>".format(tweet['id'], tweet['created_at'],
            tweet['user']['screen_name'].encode('utf-8'), tweet['text'].encode('utf-8'), 
            tweet['retweet_count'], tweet['place']['full_name'])    
    else:
        print "<Tweet: {0} | {1} | {2} | {3} | {4}>".format(tweet['id'], tweet['created_at'],
            tweet['user']['screen_name'].encode('utf-8'), tweet['text'].encode('utf-8'), 
            tweet['retweet_count'])  


if __name__ == "__main__":
    # Create an instance of the AuthHandler object
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    # Create an instance of the Listener object
    listener = StdOutListener()
 
    # Create an instance of a twitter Stream (what actually pulls data in). Pass it your auth
    # and listener objects (listener will be given the incoming stream the data)
    stream = tweepy.Stream(auth, listener)

    # Call the stream filter. Can filter on users ('follow' param), keywords ('track'), and locations
    # Can use any combinations of those three params. Considered 'OR'ed together
    stream.filter(track=["manchester united", "MUFC", "manutd" "moyes"], languages=["en"])








