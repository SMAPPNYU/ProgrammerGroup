"""
A script to show simple ways of accessing Tweet data in Mongo DBs. Simple queries, simple analysis.
Resources used:

MongoDB query docs  http://docs.mongodb.org/manual/reference/method/db.collection.find/  
PyMongo             http://api.mongodb.org/python/current/                
(A python interface to MongoDB)

@auth dpb
@date 10/20/2013
"""

from pymongo import MongoClient
from get_tweets_stream import print_tweet

# Set up connection to DB via client
host = "localhost"
port = 27017
database_name = "LargeDataSets"
collection_name = "manu_tweets"

client = MongoClient(host, port)    # MongoClient(host) works as well. Port default=27017
database = client[database_name]


# Authenticate if necessary (if a user/pwd is set up restricting access)
# database.authenticate("<user name>", "<super secret password>")


# Show all collections in the database
print "All collections in database {0}:\n\t{1}".format(database_name, database.collection_names())


# Access a particular collection of data
collection = database[collection_name]


# Print some status info
print "Accessing server at {0}:{1}, database {0}, collection {1}".format(host, port, database_name,
    collection_name)
print "Collection has {0} documents".format(collection.count())


# Fetch a single tweet from the collection
tweet = collection.find_one()
print "\n---\nWhole tweet: {0}\n---\n".format(tweet)


## Some sample queries:

# Get all tweets from a user
print "All tweets from a user..."
user_tweets = collection.find({ 'user.screen_name': 'SCREEN NAME HERE' })
for t in user_tweets:
    print_tweet(t)
print "\n---\n"

# Get all "geocoded" tweets
print "All geocoded tweets..."
geo_tweets = collection.find({ 'place': { '$ne': None } })
for t in geo_tweets:
    print_tweet(t)
print "\n---\n"

# Get all tweets with word "win"
print "All tweets containing word 'win'..."
win_tweets = collection.find({ 'text' : { '$regex' : 'WIN', '$options': 'i' } })
for t in win_tweets:
    print_tweet(t)
print "\n---\n"




