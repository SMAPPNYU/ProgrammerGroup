"""
Programming Group week 09 - Reading raw tweets from file (such as those stored from a
streaming collection)

Tweets      -   https://dev.twitter.com/docs/platform-objects/tweets
OpenHeatMap -   http://www.openheatmap.com/

@auth dpb
@date 12/02/2013
"""

import simplejson as json
from json_util import ConcatJSONDecoder


# STEP 1: Read tweets in from file and store in a list of tweets
# There's a trick here... just use this ConcatJSONDecoder tool (can also do it line-by-line)
tweetfile = "ukraine_geo_1000.json.txt"
handle = open(tweetfile)
tweets = json.loads(handle.read(), cls=ConcatJSONDecoder)
handle.close()

# Line-by-line looks like this:
#handle = open(tweetfile)
#tweets = []
#for line in handle:
#    tweet = json.loads(line.rstrip())
#    tweets.append(tweet)
#handle.close()


# We want to:
# 1 - Loop over all tweets
# 2 - Check if each tweet is in fact a tweet
# 3 - Check for Language, Place, and Geocoded data
# 4 - Store each of Language occurrence, Country occurrence, and Coordinates
# 5 - Write each of these to very simple CSV files

# STEP 2: Do something interesting with the tweets
# (Store language and country counts, an a list of GPS coords)
langs = {}
countries = {}
coords = []

for tweet in tweets:

    # Make sure it's a tweet (if it isn't, skip it)
    if "in_reply_to_status_id" not in tweet:
        print "Warning:\n\t{0}\nnot a valid tweet".format(tweet)
        continue

    # Check for language ("und" represents undeterminable)
    if tweet["lang"] != None and tweet["lang"] != "und":
        language = tweet["lang"]
        if language not in langs:
            langs[language] = 1
        else:
            langs[language] += 1

    # Check for Place information 
    if tweet["place"] != None:
        country = tweet["place"]["country_code"]
        if country not in countries:
            countries[country] = 1
        else:
            countries[country] += 1

    # Check for Geo location
    if tweet["coordinates"] != None:
        lat = tweet["coordinates"]["coordinates"][1]
        lon = tweet["coordinates"]["coordinates"][0]
        coords.append((lat, lon))

print "Languages and occurence: {0}\n".format(langs)
print "Countries: {0}\n".format(countries)
print "Geolocated tweets: {0}\n".format(len(coords))


# STEP 3: Output gathered values to use in external tools
countryfile = "ukraine_countries.csv"
handle = open(countryfile, 'w')
handle.write("Country,Value\n")
for c in countries:
    handle.write("{0},{1}\n".format(c, countries[c]))
handle.close()

coordsfile = "ukraine_geo.csv"
handle = open(coordsfile, 'w')
handle.write("lat,lon,value\n")
for c in coords:
    handle.write("{0},{1},{2}\n".format(c[0], c[1], 1))
handle.close()



