"""
Programming Group week09 part 2 - solutions to suggestions

@auth dpb
@date 12/02/2013
"""

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

# Make plot of language?