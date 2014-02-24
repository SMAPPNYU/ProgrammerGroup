"""
Basic code for week 02. Basic tasks: create a mongoDB client; access a database and list
collections; access tweet data; access by data, regular expression, geocode?; 

If time: write data to file (simple and json); do aggregates and counts; make chart

@auth dpb
@date 10/08/2013
"""

# Import: pull in "modules" containing external functions and variables
import pymongo
from pymongo import MongoClient

# A function...
def print_tweet(tweet):
    if tweet['place'] != None:
        print "<Tweet: {0} | {1} | {2} | {3} | {4} | {5}>".format(tweet['id'], tweet['created_at'],
            tweet['user']['screen_name'].encode('utf-8'), tweet['text'].encode('utf-8'), 
            tweet['retweet_count'], tweet['place']['full_name'])    
    else:
        print "<Tweet: {0} | {1} | {2} | {3} | {4}>".format(tweet['id'], tweet['created_at'],
            tweet['user']['screen_name'].encode('utf-8'), tweet['text'].encode('utf-8'), 
            tweet['retweet_count'])    


# Database variables
host = "HOSTNAME"
port = 27011
database_name = "test"
collection_name = "sample_tweets"

# Start a Mongo client
client = MongoClient("HOST", "PORT")   # With literal values (not saved)
client = MongoClient(host, port)                            # With variables (stored)

# Use a database (all equivalent!)
database = client["test"]                   # With a literal
database = client[database_name]            # With a variable
database = client.test                      # We can do this because we know 'test' is a database

# Authenticate (aka log in) - without this, any operation on the database will cause errors!
database.authenticate("readonly", "<super secret password!>")
print "All collections in database {0}:\n\t{1}".format(database_name, database.collection_names())

# Get a collection (all equivalent!)
collection = database[collection_name]      # With a variable

print "Accessing server at {0}:{1}, database {0}, collection {1}".format(host, port, database_name,
    collection_name)
print "Collection has {0} documents".format(collection.count())

# Get a tweet!
tweet = collection.find_one()
print "\n---\n"
print "Whole tweet: {0}".format(tweet)
print "\n---\n"

# Get all tweets from a user (loops and iteration, plus query documents)
print "All tweets from a user..."
user_tweets = collection.find({ 'user.screen_name': 'Centurion480' })
for t in user_tweets:
    print_tweet(t)
print "\n---\n"

# Get all "geocoded" tweets
print "All geocoded tweets..."
geo_tweets = collection.find({ 'place': { '$ne': None } })
for t in geo_tweets:
    print_tweet(t)
print "\n---\n"

# Get all tweets with word "bomb"
print "All tweets containing word 'bomb'..."
bomb_tweets = collection.find({ 'text' : { '$regex' : 'BOMB', '$options': 'i' } })
for t in bomb_tweets:
    print_tweet(t)
print "\n---\n"

# Get all tweets with word 'bomb' or 'drone'
print "All tweets with bomb or drone..."
be_tweets = collection.find({ 'text': { '$regex': 'BOMB|DRONE', '$options': 'i' } })
for t in be_tweets:
    print_tweet(t)
print "\n---\n"


# Get all tweets, and do something with them!
first_min = 0
second_min = 0
third_min = 0
for t in collection.find():
    minute = t['created_at'][14:16]
    if minute == '21':
        first_min += 1
    elif minute == '22':
        second_min += 1
    elif minute == '23':
        third_min += 1

import matplotlib.pyplot as plt

plt.title("Tweets/Minute re: Syria, Obama")
plt.xlabel("Minute")
plt.ylabel("Tweets")

plt.plot([1,2,3], [first_min, second_min, third_min], 'm-', linewidth=2.0, label="Syria/Obama")
plt.plot([1,2,3], [96,100,109], 'r-.', linewidth=2.0, label="Random Baseline")

plt.legend(loc='upper left')
plt.show()









