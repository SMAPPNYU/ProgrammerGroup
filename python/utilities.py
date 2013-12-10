"""
Programmer Group utility functions

@auth dpb
@date 10/20/2013+
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


def print_tweet(tweet):
    """A pretty-print function for tweet display"""
    if tweet['place'] != None:
        print "<Tweet: {0} | {1} | {2} | {3} | {4}>".format(
            tweet['id'], 
            tweet['created_at'],
            tweet['user']['screen_name'].encode('utf-8'), 
            tweet['place']['full_name'],
            tweet['text'].encode('utf-8'))
    else:
        print "<Tweet: {0} | {1} | {2} | {3}>".format(
            tweet['id'], 
            tweet['created_at'],
            tweet['user']['screen_name'].encode('utf-8'), 
            tweet['text'].encode('utf-8'))


def print_tweet_extras(tweet, score, retweet):
    print "{0}\t{1}\t{2}\t{3}\t{4}".format(
        tweet['user']['screen_name'].encode('utf-8'), 
        tweet['created_at'],
        score,
        retweet,
        tweet['text'].encode('utf-8'))


def tweet2json(tweets, outfile, append=True):
    """
    A function that takes a collection of tweets and writes all to a raw bson/json
    file. 
    Parameters:
        tweets      - A collection of tweet objects
        outfile     - A string representing the file to write to (eg: "leg-tweets.csv")
        append      - A True/False value to indicate overwrite (False) or append (True)
    """
    from bson.json_util import dumps

    # Open the file to write to, either appending or overwriting
    if append:
        outhandle = open(outfile, 'a')
    else:
        outhandle = open(outfile, 'w')

    # Go over all tweets, dumping each to file with the 'dumps' utility
    for tweet in tweets:
        if '_id' in tweet:
            del tweet['_id']
        outhandle.write(dumps(tweet) + "\n")
    outhandle.close()


def tweets2csv(tweets, outfile, append=True):
    """
    A function that takes a collection of tweets and writes all to simple CSV file.
    Parameters:
        tweets      - A collection of tweet objects
        outfile     - A string representing the file to write to (eg: "leg-tweets.csv")
        append      - A True/False value to indicate overwrite (False) or append (True)
    NOTE: There will be problems here. When? EG: when tweet 'text' contains a comma. Others?
    SOLN: Remove all punctuation and newline chars from tweet text before writing.
    """
    # Open the file to write to, either appending or overwriting
    if append:
        outhandle = open(outfile, 'a')
    else:
        outhandle = open(outfile, 'w')

    # Write header for fields included
    handle.write("USER,DATE,TWEET\n")

    # Go over all tweets, writing each one to file
    for tweet in tweets:

        # Get the cleaned tweet text
        clean_text = clean_tweet_text(tweet["text"])

        # Build string (a "row" of the CSV file) to write to file
        csv_string = "{0},{1},{2}\n".format(
            tweet['user']['screen_name'].encode('utf-8'),
            tweet['created_at'],
            clean_text)

        # Write csv string to file
        outhandle.write(csv_string)

    # Close file and stop
    outhandle.close()


def clean_tweet_text(text):
    """
    Takes text (representing a tweet), removes punctuation and extra whitespace, and 
    encodes it properly. Returns cleaned text as a utf-8 string
    """
    replace_dict = {
        "\n": " ",
        "\t": " ",
        ",": " ",
        #TODO: Add more here, as desired/necessary. EG:
        #"can't": "can not",
        #"w/": "with ", BUT WATCH OUT FOR URLS
    }

    clean_text = tweet["text"].encode("utf-8")
    for bad_char in replace_dict:
        clean_text = clean_text.replace(bad_char, replace_dict[bad_char])

    return clean_text


def jsonfile2tweets(infile):
    """
    Takes a raw JSON file of tweets, reads them in, and returns a list of tweets.
    """
    from bson.json_util import loads
    from json_util import ConcatJSONDecoder

    inhandle = open(infile)
    tweets = loads(inhandle.read(), cls=ConcatJSONDecoder)
    inhandle.close()
    return tweets


def csvfile2lists(infile):
    """
    Takes a CSV file as input, returning a list of lists, where the top-level list
    represents the rows of the csv, and the internal list represents each column of the 
    CSV.
    EG: return = 
        [
            ['USER', 'DATE', 'TWEET'],
            ['BobTwit', 'CREATED AT XX:YY:ZZ', 'I like to tweet about stuff'],
            ['JuanPablo', 'CREATED AT II:JJ:KK', 'Political science hooray'],
        ]

    return[0] is the first row (['USER', 'DATE', 'TWEET'])
    return[1] is the second row, etc. (['BobTwit', ...])
    len(return) is the number of rows (3)
    return[0][0] is the first column of the first row ('USER')
    return[1][2] is the third column of the second row ('Political science hooray')
    """
    inhandle = open(infile)
    column_list = []
    for line in infile:
        row_list = line.rstrip().split(",")
        column_list.append(row_list)
    inhandle.close()
    return column_list






