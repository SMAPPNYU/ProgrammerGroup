"""
Week 05 Programming Group Demo
"""

from pymongo import MongoClient, ASCENDING, DESCENDING

client = MongoClient("smapp.politics.fas.nyu.edu", 27011)
database = client["US_LEGISLATOR"]
database.authenticate("readonly", "smappnyu")
collection = database["legislator_tweets"]


# Grab a single sample tweet (extra: sort by timestamp descending)
some_tweet = collection.find_one(sort=[("timestamp", DESCENDING)])


# Two styles of import: "all" and "named"
import utilities
utilities.print_tweet(some_tweet)

from utilities import print_tweet
print_tweet(some_tweet)

