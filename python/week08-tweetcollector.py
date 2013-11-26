"""
Programming Group week 08 - Python streaming collector

Simple script to access the twitter streaming API to fetch tweets (by certain filters). The script
uses the following resources:

Twitter Dev. Streaming API          https://dev.twitter.com/docs/streaming-apis
Tweepy, a python Twitter package    https://pypi.python.org/pypi/tweepy/
                                    http://pythonhosted.org/tweepy/html/
                                    https://github.com/tweepy/tweepy

Twitter Streaming params            https://dev.twitter.com/docs/streaming-apis/parameters
Good tutorial                       http://www.pythoncentral.io/introduction-to-tweepy-twitter-for-python/

@auth dpb
@date 10/20/2013
"""

##
# NOTE: To start a collection:
#
#   1 - Create a twitter app at dev.twitter.com (also create access token)
#   2 - Set your twitter keys and access token keys at the bottom of this script
#   3 - Create a "FileListener" with name of file to write tweets to
#   4 - Create a keywords/userlist/locations list, 
#   5 - Start the stream filtered with appropriate parameter(s) (track, follow, locations)
#
# All of this at the bottom of this script (in the __name__=="__main__" section)!
##


import tweepy
import simplejson as json
from bson.json_util import dumps

class FileOutListener(tweepy.streaming.StreamListener):
    """
    A basic listener class that inherits from Tweepy's StreamListener.

    Can override certain methods to obtain certain behavior. The basic stream listener
    handles data best. Note that 'status' really means 'tweet' (annoyingly)
    """
    def __init__(self, filename="tweets.json"):
        """
        Override the normal init functionality. Open the file to output collected tweets to.
        """
        super(tweepy.StreamListener, self).__init__()

        try:
            self.outhandle = open(filename, 'a')
        except Exception as e:
            print "Failed to open file {0} for storing tweets. Exiting.".format(filename)
            raise e


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

        # Dump tweet to file
        self.outhandle.write(dumps(status) + "\n")

    def on_limit(self, track):
        print "-!- Collection limit hit. {0} matching tweets not delivered".format(track)

    def on_error(self, status):
        print "-!- Error. Status: {0}".format(status)

    def on_disconnect(self, notice):
        print "-!- Disconnect recvd from Twitter. Reason: {0}".format(notice['reason'])
        return False


def print_tweet(tweet):
    if tweet['place'] != None:
        print "<Tweet: {0} | {1} | {2} | {3} | {4}>".format(
            tweet['id'], 
            tweet['created_at'],
            tweet['user']['screen_name'].encode('utf-8'), 
            tweet['place']['full_name'],
            tweet['text'].encode('utf-8'))
    else:
        print "<Tweet: {0} | {1} | {2} | {3}>".format(
            tweet['id'], 
            tweet['created_at'],
            tweet['user']['screen_name'].encode('utf-8'), 
            tweet['text'].encode('utf-8'))  


if __name__ == "__main__":

    # Go to http://dev.twitter.com and create an app.
    # The consumer key and secret will be generated for you (paste below)
    consumer_key = "YOUR_CONSUMER_KEY"
    consumer_secret = "YOUR_CONSUMER_SECRET"

    # Create an access token under the the "Your access token" section.
    # Refresh the app page to get the access token values (paste below)
    access_token = "YOUR_ACCESS_TOKEN"
    access_secret = "YOUR_ACCESS_SECRET"

    # Create a tweepy Authorization object with your twitter keys
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    # Create a listener object, to capture tweets and write them to a file
    listener = FileOutListener(filename="Tweets.json.txt")
 
    # Create an object representing the Twitter "stream." Must provide it with your
    # authorization object and listener objects.
    stream = tweepy.Stream(auth, listener)


    # Call the Stream filter. Can filter on users ('follow'), keywords ('track'), and 
    # locations. Can use any combinations of those three params. Considered logical-ORed 
    # together. EXAMPLES:

    # Create a list of keyword terms, call Stream filter with track
    keywords = ["iran", "irandeal", "iran deal" "iran nuclear deal", "nuke deal", "nuclear deal"]
    stream.filter(track=keywords, languages=["en"])

    # Create a list of users (IDs, NOT screennames), call Stream filter with follow
    # reppaulryan   18916432    
    # ryan4congress 240831627   
    # pryan         733751245   
    # paulryanpress 333692333
    #users = [18916432, 240831627, 733751245, 333692333, 1650976376]
    #stream.filter(follow=users, languages=["en"])

    # Create a locations list, call Stream filter with locations (tweets all geocoded)
    # (bounding box: SW-long, SW-lat, NE-long, NE-lat)
    # San Francisco:    -122.75,36.8,-121.75,37.8
    # New York:         -74,40,-73,41
    #locs = [-122.75, 36.8, -121.75, 37.8, -74, 40, -73, 41]
    #stream.filter(locations=locs, languages=["en"])

    # Filter on both users and keywords:
    #stream.filter(follow=users, track=keywords)

    # Filter on both keywords and locations. Remember, they are OR-joined (keywords or locs)
    #stream.filter(track=keywords, locations=locs)

