"""
A simple script to demonstrate storing tweets to a MongoDB database and collection. Resources used
in this code:

MongoDB         http://www.mongodb.org/
                http://docs.mongodb.org/manual/
PyMongo         http://api.mongodb.org/python/current/                
(A python interface to MongoDB)

@auth dpb
@date 10/20/2013
"""

from pymongo import MongoClient

class Tweet2Mongo():
    """
    A simple class for handling adding tweets to a mongoDB instance.
    """

    def __init__(self, host, port, database, collection):
        """
        Store variables
        """
        self.host = host
        self.port = int(port)
        self.database = database
        self.collection = collection
        
        self.client = None
        self.dbh = None
        self.colh = None
        self.connected = False

    def connect(self, user, password):
        """Connect to a MongoDB instance"""
        if self.connected:
            return True

        # Create a client connection to your mongo instance on 'host' at 'port'
        self.client = MongoClient(self.host, self.port)
        self.dbh = self.client[self.database]

        if not self.dbh.authenticate(user, password):
            return False
        
        self.colh = self.dbh[self.collection]
        self.connected = True
        return self.connected

    def add_tweet(self, tweet):
        """Takes a json tweet object, adds it to the instance's database and collection"""
        if not self.connected:
            raise Exception("Database not connected. Call 'connect(user, pwd)' first")

        # Basic, basic tweet integrity check. Something more sophisticated is better
        if 'created_at' not in tweet:
            raise Exception("Tweet {0} not valid".format(tweet))

        # Add the tweet to the collection via collection handler. Can use 'save' or 'insert' 
        # (see docs for difference: http://docs.mongodb.org/manual/reference/method/db.collection.insert/)
        self.colh.insert(tweet, safe=True)










