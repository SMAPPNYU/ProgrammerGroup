"""
Simple script to access the twitter REST API (eg., search) to fetch tweets
This script uses the following resources:

Twitter Dev. REST API               https://dev.twitter.com/docs/api/1.1
Tweepy, a python Twitter package    https://pypi.python.org/pypi/tweepy/
                                    http://pythonhosted.org/tweepy/html/
                                    https://github.com/tweepy/tweepy

Twitter REST search     https://dev.twitter.com/docs/api/1.1/get/search/tweets
Tweepy search docs      http://pythonhosted.org/tweepy/html/api.html#help-methods

@auth dpb
@date 10/20/2013
"""

import tweepy

# Authorization keys. Always use OAuth! (Also, can fetch the access token in code if you want)
# To make: go to dev.twitter.com, log in, create an "application", and request an access token
consumer_key = "YOUR CONSUMER KEY"
consumer_secret = "YOUR CONSUMER SECRET"
access_token = "YOUR ACCESS TOKEN"
access_secret = "YOUR ACCESS TOKEN SECRET"


# Set up OAuth via tweepy's handler object, and create an instance of the Tweepy API with auth
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)


# Grab a "cursor" of data - much like an iterator. Pass the API call type you want to Cursor(...)
# Then can "iterate" over the search results, paging handled for you. Pass cursor other api call params
search_cursor = tweepy.Cursor(api.search, q="tottenham OR arsenal", include_entities=True, lang="en")

# Can also 'limit' results by passing an int to items()
for tweet in search_cursor.items(10):
    # Print them!
    print "<Tweet: {0}\t{1}\t{2}>".format(tweet.created_at, 
                                          tweet.user.screen_name.encode('utf-8'), 
                                          tweet.text.encode('utf-8'))

    # Write to file? Maybe. Write a CSV, raw json, custom json, etc.
    # Store them in a database? Yes. Sort of (need to get raw data from REST API).

print "\n---Completed fetching tweets---\n"


