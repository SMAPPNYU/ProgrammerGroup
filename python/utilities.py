"""
Programmer Group utility functions
"""


def is_retweet(tweet):
    """Takes a python-native tweet obect (a dict). Returns True if a tweet is any kind of retweet"""
    import re
    
    # Define manual retweet patterns
    rt_manual_pattern = r"^RT @"
    rt_partial_pattern = r" RT @"

    if 'retweeted_status' in tweet:
        return True
    elif re.search(rt_manual_pattern, tweet['text'].encode('utf-8')):
        return True
    elif re.search(rt_partial_pattern, tweet['text'].encode('utf-8')):
        return True
    return False


def print_tweet_extras(tweet, score, retweet):
    print "{0}\t{1}\t{2}\t{3}\t{4}".format(
        tweet['user']['screen_name'].encode('utf-8'), 
        tweet['created_at'],
        score,
        retweet,
        tweet['text'].encode('utf-8'))


def write_csv(tweets, filename):
    """
    A function that takes a collection of tweets and writes all to file.
    Parameters:
        tweets      - A collection of tweet objects
        filename    - A string representing the file to write to (eg: "legislator-tweets.csv")
    NOTE: There will be problems here. When? EG: when tweet 'text' contains a comma. Others?
    """
    handle = open(filename, "w")
    handle.write("USER,DATE,TWEET\n")

    for tweet in tweets:

        filestring = "{0},{1},{2}\n".format( 
            tweet['user']['screen_name'].encode('utf-8'),
            tweet['created_at'],
            tweet['text'].encode('utf-8').replace(",", "").replace("\n", " ")
            )
        handle.write(filestring)
    handle.close()


def print_tweet(tweet):
    """A function to print a tweet in a nice way"""
    # Don't forget to 'encode' tweet values that might have non-standard characters (text, username)
    print "{0}\t{1}\t{2}".format(
        tweet['user']['screen_name'].encode('utf-8'), 
        tweet['created_at'], 
        tweet['text'].encode('utf-8'))
