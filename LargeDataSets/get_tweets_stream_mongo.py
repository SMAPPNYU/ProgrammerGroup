"""
Simple script to access the twitter streaming API to fetch tweets (by certain filters). Then, store
tweets in a MongoDB database. The script uses the following resources:

Twitter Dev. Streaming API          https://dev.twitter.com/docs/streaming-apis
Tweepy, a python Twitter package    https://pypi.python.org/pypi/tweepy/
                                    http://pythonhosted.org/tweepy/html/
                                    https://github.com/tweepy/tweepy

@auth dpb
@date 10/20/2013
"""

import tweepy
import simplejson as json

from tweet2mongo import Tweet2Mongo

# Set up twitter authentication. Go to http://dev.twitter.com and create an app, etc.
consumer_key = "YOUR CONSUMER KEY"
consumer_secret = "YOUR CONSUMER SECRET"
access_token = "YOUR ACCESS TOKEN"
access_secret = "YOUR ACCESS TOKEN SECRET"

# For now, simple global DB variables
host = "localhost"                  # host = "smapp.politics.fas.nyu.edu"
port = 27017                        # port = 27011
database = "LargeDataSets"          # database = "test"     user = "dpb"
collection = "manu_tweets"          # collection = "lds"    password = "<Super Secret Password>"


class ToMongoListener(tweepy.streaming.StreamListener):
    """
    A basic listener that sends tweets to a MongoDB when received, via the tweet2mongo module
    """

    def __init__(self):
        """Override the init function: set up a MongoDB connection via our tweet2mongo code"""
        super(tweepy.StreamListener, self).__init__()

        self.db = Tweet2Mongo(host, port, database, collection)

        # Call connect method on Tweet2Mongo instance. If needed, provide user and password
        if not self.db.connect():
            raise Exception("Failed to initiate database connection, exiting")

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

        # Push tweet to database
        self.db.add_tweet(status)

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
    listener = ToMongoListener()
 
    # Create an instance of a twitter Stream (what actually pulls data in). Pass it your auth
    # and listener objects (listener will be given the incoming stream the data)
    stream = tweepy.Stream(auth, listener)

    # Call the stream filter. Can filter on users ('follow' param), keywords ('track'), and locations
    # Can use any combinations of those three params. Considered 'OR'ed together
    stream.filter(track=["manchester united", "MUFC", "manutd" "moyes"], languages=["en"])








