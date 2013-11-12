"""
Python code for Programming Group week06. This week:

0, Use pip to install a data science package, the Data Science Toolkit (on the command 
line, not in Python): http://www.datasciencetoolkit.org/

1, Re: Syria in the US House and Senate:
Find all tweets from US_LEGISLATOR data set with keyword 'syria' from date range 
8/30/2013 - 9/06/2013 (warships to gulf, wait for congress permission - senate approves 
force bill)

Excuse the wikipedia:
http://en.wikipedia.org/wiki/Timeline_of_the_Syrian_civil_war_(from_May_2013)#21_August

2, Compute sentiment scores for all the tweets found! At the same time, compute basic 
aggregates, such as number of tweets v. number of retweets, and sentiment-per-day

3, Hopefully, plot some stuff (http://matplotlib.org/)

@auth dpb
@date 11/12/2013
"""

from dstk import DSTK
from datetime import datetime
from pymongo import MongoClient

from utilities import is_retweet, print_tweet_extras


# Start database client, connect to Syria DB, and authenticate
client = MongoClient("smapp.politics.fas.nyu.edu", 27011)
usleg_db = client["US_LEGISLATOR"]
usleg_db.authenticate("readonly", "smappnyu")

# Create datetime objects to represent start and end of range of interest
start = datetime(2013, 8, 30)
end = datetime(2013, 9, 6)

# Find tweets of interest in the database
tweets = usleg_db.legislator_tweets.find({ 
	"timestamp": {"$gte": start, "$lt": end}, 
	"text": {"$regex": "syria", "$options": "i"}
	})

print "Found {0} tweets from US Legislators on Syria from {1} to {2}".format(
	tweets.count(with_limit_and_skip=True), start, end)


# Pre-create aggregate variables. Note: BEFORE the loop!
#	Number of tweets vs retweets (via function in utilities!)
#	Sentiment per day (sentiment via DataScienceToolkit)
#	Number of tweets with valid sentiment per day (for avg)

num_tweets = 0
num_retweets = 0
total_tweets = 0
daily_sentiment = {}
tweets_per_day = {}

# Start a DSTK session (like making a client to our MongoDB) to get sentiment
dstk = DSTK()

# Go over all tweets, adding to our aggregate variables
for tweet in tweets:

	# Add to tweet/retweet aggregate variable
	if is_retweet(tweet):
		num_retweets += 1
	else:
		num_tweets += 1
	total_tweets += 1

	# Get sentiment score from DSTK. Note: doing in a "try-catch" block (so if it fails,
	# our program will not break. Instead, we print the error and move on)
	try:
		score = dstk.text2sentiment(tweet["text"].encode("utf-8"))
	except Exception as e:
		print "Failed to query DSTK for sentiment (error: {0})".format(e)
		continue
	tweet_score = score["score"]

	# Add sentiment to by-day aggregate (done by day, b/c we don't have overlapping days)
	# Also add to tweets_per_day count
	tweet_day = tweet["timestamp"].day
	if tweet_day in daily_sentiment:
		daily_sentiment[tweet_day] += tweet_score
		tweets_per_day[tweet_day] += 1
	else:
		daily_sentiment[tweet_day] = tweet_score
		tweets_per_day[tweet_day] = 1

	# Print tweet CSV-like info, with sentiment score and whether it is a retweet
	# HINT: Could write to CSV file here instead...
	if is_retweet(tweet):
		print_tweet_extras(tweet, tweet_score, "Retweet")
	else:
		print_tweet_extras(tweet, tweet_score, "NotRetw")
		

# At this point, we've computed all our aggregates. Now we need to chart them!
import matplotlib.pyplot as plt

# Plot tweets v. retweets
labels = 'Tweets', 'Retweets (All)'
sizes = [num_tweets, num_retweets]
colors = ['lightskyblue', 'lightcoral']
explode = (0, 0.1) # only "explode" the 2nd slice (i.e. 'Retweets')

plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)

# Set aspect ratio to be equal so that pie is drawn as a circle.
plt.axis('equal')

# Save, show, and close
plt.savefig("usleg-syria-tweets.png")
plt.show()
plt.close()


# Average sentiment per day (first compute averages)
day_list = range(len(daily_sentiment))

sentiment_averages = []

for day in daily_sentiment.keys():
	avg_sentiment = daily_sentiment[day] / tweets_per_day[day]
	sentiment_averages.append(avg_sentiment)

plt.title("Sentiment per Day of US-Syria")
plt.xticks(day_list, ("8/30", "8/31", "9/01", "9/02", "9/03", "9/04", "9/05"))
plt.xlabel("Day")
plt.ylabel("Average Sentiment [-5 negative to 5 positive]")

plt.plot(day_list, sentiment_averages, 'ko')
plt.plot(day_list, sentiment_averages, 'm-', linewidth=2.0, 
	label="Legislator Sentiment")

plt.legend(loc='upper left')
plt.savefig("usleg-syria-sentiment.png")
plt.show()

