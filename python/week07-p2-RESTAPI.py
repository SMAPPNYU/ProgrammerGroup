"""
PART 2

Python code for Programming Group week 07. Two parts:

1, Query Syria dataset between 8/25 and 9/06 for all tweets with "intervene/intervention"
Write these to CSV file

2, Read CSV file, break into component values (need to know how to do this). Will go
through manual code, also reference library:

	http://docs.python.org/2/library/csv.html

Then, use twitter REST api via Tweepy to get each user's (demo: one or two) last N
tweets. Write these to user-titled CSV file. Twitter & Tweepy docs:

	https://dev.twitter.com/docs/api/1.1/get/statuses/user_timeline
	http://pythonhosted.org/tweepy/html/api.html#api-reference
	http://pythonhosted.org/tweepy/html/cursor_tutorial.html

Plot: How many of user's last 100 tweets were about Syria?

@auth dpb
@date 11/18/2013
"""

import tweepy

# First, open CSV file and read lines from it. Each line (except first) represents one
# tweet. Store user screen name info, and how many times each occurs.
# NOTE AGAIN that there is a library to do this sort of stuff for you. Can use it.
handle = open("usleg-syria-intervene.csv")
tweets_per_user = {}

# .next() gets a single line from the open file. Takes it away from the file (the next
# time you call next(), you will be given the subsequent line)
column_key = handle.next()

# Looping or iterating over an open file gives you each line in turn
for line in handle:
	# Want to "split" each line by its separator (a comma)
	fields = line.rstrip().split(",")

	# Always expecting at least three fields (user, time, text)
	if len(fields) < 3:
		print "Line\n\t{0}\nincorrectly formatted. Skipping..".format(line)
		continue

	# 'fields' is a list. fields[0] is User Screen Name, fields[1] is CreatedAt, etc
	user = fields[0]
	date = fields[1]
	text = fields[2]
	
	# Add to user dictionary for counting tweets in set
	if user in tweets_per_user:
		tweets_per_user[user] += 1
	else:
		tweets_per_user[user] = 1
handle.close()


# Sort command to find user with most tweets
sorted_users = sorted(tweets_per_user.items(), key=lambda u: u[1], reverse=True)
most_active_user = sorted_users[0]

print "The most active user in the set is {0}, with {1} tweets".format(
	most_active_user[0], most_active_user[1])


# Twitter API Authentication configuration
consumer_key = "fay80GlqqPtNNyGgnwkYw"
consumer_secret = "zgbLl2DQU8HXMpUEdNj5rphN3ogDSL1xFxVtW8Kns"
access_token = "1650976376-pmDLQDvy1icJJLVQrT88usDGxkAMaugnDxQefz0"
access_secret = "G2fEkbsUYZNG65toB3FeS2kIndXpXKhf7uTFAldhDE"

# Set up OAuth via tweepy's handler object, and create an instance of the Tweepy API 
# with authorization just created
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

# Grab a "cursor" of data - much like an iterator. Pass the API call type you want to 
# Cursor(...), then can "iterate" over the search results, paging handled for you. Pass 
# cursor other api call parameters (user id, etc. See twitter user timeline docs for
# more)
cursor = tweepy.Cursor(api.user_timeline, id=most_active_user[0])
backtweets = 2000

print "last {0} tweets from {1}:".format(backtweets, most_active_user[0])

for tweet in cursor.items(backtweets):
	print "{0}".format(tweet.text.encode('utf-8'))

# Can we get his/her tweets from a certain time period? Ref: twitter docs!
# https://dev.twitter.com/docs/api/1.1/get/statuses/user_timeline
# (No. But, since id?)
# ((sneaky...))




