"""
Python code for week 04: as review, connect to MongoDB instance, store client, database, and
document collection in variables; write functions to print a single tweet, and to write a collection
of tweets to a file; query by date range via python datetime objects.

Tutorial on Python functions:   http://www.codecademy.com/tracks/python
(Lesson 7: Functions)

@auth dpb
@date 10/29/2013
"""

from datetime import datetime
from pymongo import MongoClient


def write_csv(tweets, filename):
    """
    A function that takes a collection of tweets and writes all to file.
    Parameters:
        tweets      - A collection of tweet objects
        filename    - A string representing the file to write to (eg: "legislator-tweets.csv")
    NOTE: There will be problems here. When? EG: when tweet 'text' contains a comma. Others?
    """
    handle = open(filename, 'w')
    handle.write("USER,DATE,TWEET\n")

    for tweet in tweets:
        handle.write("{0},{1},{2}\n".format(
            tweet['user']['screen_name'].encode('utf-8'), 
            tweet['created_at'], 
            tweet['text'].encode('utf-8')))
    handle.close()


def print_tweet(tweet):
    """A function to print a tweet in a nice way"""
    # Don't forget to 'encode' tweet values that might have non-standard characters (text, username, etc)
    print "{0}\t{1}\t{2}".format(
        tweet['user']['screen_name'].encode('utf-8'), 
        tweet['created_at'], 
        tweet['text'].encode('utf-8'))


## Outside of functions:

# Access the database
client = MongoClient("smapp.politics.fas.nyu.edu", 27011)
database = client["US_LEGISLATOR"]
database.authenticate("readonly", "smappnyu")
collection = database["legislator_tweets"]

# Create a start and end date
start = datetime(2013, 9, 20, 0, 0, 0)
end = datetime(2013, 10, 16, 0, 0, 0)

# Query the collection for tweets in our date range
shutdown_tweets = collection.find( {'timestamp': {"$gte": start, "$lt": end } } )

print "Tweets found: {0}".format(shutdown_tweets.count(with_limit_and_skip=True))

# Print all tweets via function call 
# NOTE: once you access all tweets in a find() result, they are gone. 
# NOTE: IE, after using the for loop below, 'shutdown_tweets' will be empty
#for t in shutdown_tweets:
#    print_tweet(t)

# Write tweets to outfile via function call
print "Writing tweets to file"
write_csv(shutdown_tweets, "/Users/dpb/Desktop/legislator-shutdown.csv")














