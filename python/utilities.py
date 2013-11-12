"""
Programmer Group utility functions
"""

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

        filestring = "{0},{1},{2}\n".format( 
            tweet['user']['screen_name'].encode('utf-8'),
            tweet['created_at'],
            tweet['text'].encode('utf-8').replace(",", "")
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
