# Alexander C. Perez, acperez@syr.edu
import json


class Candidate:

    def __init__(self, name, state, party, twitterUsername=None):
        self.name = name
        self.state = state
        self.party = party
        self.twitterusername = twitterUsername
        self.tweets = []

    def addTweet(self,tweetAsString):
        self.tweets.append(tweetAsString)

    def getTweets(self):
        return self.tweets

    def getTwitteruName(self):
        self.twitterusername = None

    def setTwitteruName(self, name):
        self.twitterusername = name

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
