"""
PART 1

Python code for Programming Group week 07. Two parts:

1, Query US_LEG. dataset between 8/21 and 9/06 for all tweets with "intervene/intervention"
regarding Syria. Write these to CSV file

2, Read CSV file, break into component values (need to know how to do this). Will go
through manual code, also reference library:

	http://docs.python.org/2/library/csv.html

Then, use twitter REST api via Tweepy to get each user's (demo: one or two) last N
tweets. Write these to user-titled CSV file.

Plot: How many of user's last 100 tweets were about Syria?

@auth dpb
@date 11/18/2013
"""

from datetime import datetime
from pymongo import MongoClient

from utilities import write_csv

# Connect to DB and authenticate. Y'all know this by now
client = MongoClient("smapp.politics.fas.nyu.edu", 27011)
usleg_db = client["US_LEGISLATOR"]
usleg_db.authenticate("readonly", "smappnyu")

# Query for tweets - more complex than we're used to. Using AND.
# (NOTE that mongo explicitly ANDs multiple comma-separated search clauses, 
# however, if two clauses on the same field with the same operator, must use $and)
start = datetime(2013, 8, 21)
end = datetime(2013, 9, 7)

results = usleg_db.legislator_tweets.find({ 
	"timestamp": {"$gte": start, "$lt": end},
	"$and": [
		{"text": {"$regex": "syria", "$options": "i"}},
		{"text": {"$regex": "interven", "$options": "i"}}
		]
	})

print "Found {0} tweets on topic. Writing to CSV file".format(
	results.count(with_limit_and_skip=True))

write_csv(results, "usleg-syria-intervene.csv")









