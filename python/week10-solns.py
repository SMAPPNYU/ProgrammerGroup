"""
Programming Group week 10: Networks

Tasks: 

1 - Get some tweets (source? doesn't matter... Let's pick something we think will be good for:)
2 - Go over all tweets, find those that are retweets (remember: functions in utility.py)
3 - Store all retweet data: who retweeted who.
4 - Make a network: nodes = users, links = retweets. Weight? Number of retweets...
5 - Visualize the network
6 - Do some networky stuff...

How to make networks? Python has an incredible library: networkx
(it's already installed. Try 'import networkx')
    
    http://networkx.github.io/
    http://networkx.github.io/examples.html
    http://networkx.github.io/documentation/latest/reference/index.html

@auth dpb
@date 12/10/2013
"""

# 1 - Get some tweets
from utilities import jsonfile2tweets

tweetfile = "./data/ukraine_geo_1000.json.txt"
tweets = jsonfile2tweets(tweetfile)
print "Read {0} tweets from file {1}".format(len(tweets), tweetfile)


# 2 & 3 - Go over all tweets, checking on only retweets. Save retweeters and retweeted
# as users, and also a list of retweets, (retweeter, retweeted)

from retweet_util import is_retweet, get_user_retweeted

users_set = set()      # A set is just a unique list (no duplication)
retweets_list = []

for tweet in tweets:
    
    if not is_retweet(tweet):
        #print "Tweet is not a retweet, skipping"
        continue

    retweeter = tweet["user"]["screen_name"].encode("utf-8")
    retweeted_info = get_user_retweeted(tweet)

    if retweeted_info == None:
        print "User retweeted could not be found, skipping"
        continue
    retweeted = retweeted_info[1]

    users_set.add(retweeter)
    users_set.add(retweeted)
    retweets_list.append( (retweeter, retweeted) )

print "Total users retweeters + retweeted: {0}".format(len(users_set))
print "Total retweets: {0}".format(len(retweets_list))


# 4 - Make a network via networkx! "Directed network" (source->target is important!)
# Node: user (screen name)
# Link: retweet from user (retweeter) to user (retweeted)
import networkx as nx

DG = nx.DiGraph()

# Add users from the users set as nodes in the network
for user in users_set:
    DG.add_node(user, color="grey")   # Note: any attributes can go here

# Add links to the network for every retweet
for retweet in retweets_list:
    retweeter = retweet[0]
    retweeted = retweet[1]

    # Simple:
    #DG.add_edge(retweeter, retweeted, weight=1) # Again, can add ANY attributes

    # More fun:
    if DG.has_edge(retweeter, retweeted):
        old_weight = DG[retweeter][retweeted]["weight"]
        DG.add_edge(retweeter, retweeted, weight=old_weight + 1)
    else:
        DG.add_edge(retweeter, retweeted, weight=1)

print "\nRetweet Nodes: {0}".format(DG.nodes())
print "\nRetweet Edges: {0}".format(DG.edges(data=True))

# MANY SHORTCUTS: 
#   can add nodes and edges directly from a list (no loops)
#   can add only edges (nodes will be added automatically)


# 6 - Network properties?
print "\nOrder (number of nodes): {0}\n".format(DG.order())
print "Size (number of edges): {0}\n".format(DG.size())
print "Diameter: {0}\n".format(nx.diameter(DG))

print "In-degrees: {0}\n".format(DG.in_degree())
print "Out-degrees: {0}\n".format(DG.out_degree())

print "Connected components: {0}\n".format(nx.number_connected_components(DG.to_undirected()))

print "In-Degree Centralities: {0}\n".format(nx.in_degree_centrality(DG))
print "Betweenness Centralities: {0}\n".format(nx.betweenness_centrality(DG, normalized=True, weight="weight"))


# 5 - Visualize? I have a function...
from network_util import display_retweet_network
display_retweet_network(DG, show=True)


















