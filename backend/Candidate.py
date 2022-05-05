# Alexander C. Perez, acperez@syr.edu
import json
from Constants import Constants


class Candidate:

    def __init__(self, name=None, state=None, party=None, twitterUsername=None, my_dict=None, **kwargs):
        if my_dict:
            for key in my_dict:
                setattr(self, key, my_dict[key])
            setattr(self, key, my_dict[key])

        self.name = name
        self.state = state
        self.party = party

        self.twitterusername = twitterUsername

        self.ECONOMYtweets = []
        self.CORONAtweets = []
        self.HEALTHCAREtweets = []
        self.NATSECURITYtweets = []
        self.CLIMATEtweets = []
        self.IMMIGRATIONtweets = []

        self.ECONOMYscores = []
        self.CORONAscores = []
        self.HEALTHCAREscores = []
        self.NATSECURITYscores = []
        self.CLIMATEscores = []
        self.IMMIGRATIONscores = []

        self.ECONOMYavg = self.calculateavg(self.ECONOMYscores)
        self.CORONAavg = self.calculateavg(self.CORONAscores)
        self.HEALTHCAREavg = self.calculateavg(self.HEALTHCAREscores)
        self.NATSECURITYavg = self.calculateavg(self.HEALTHCAREscores)
        self.CLIMATEavg = self.calculateavg(self.CLIMATEscores)
        self.IMMIGRATIONavg = self.calculateavg(self.IMMIGRATIONscores)

    def calculateavg(self, listofscores):
        try:
            val = sum(listofscores) / len(listofscores)
        except ZeroDivisionError as e:
            return 0
        return val

    def addTweetToCategory(self, category, tweet):
        if category == Constants.CORONA_VIRUS:
            self.CORONAtweets.append(tweet)

        elif category == Constants.ECONOMY:
            self.ECONOMYtweets.append(tweet)

        elif category == Constants.CLIMATE_CHANGE:
            self.CLIMATEtweets.append(tweet)

        elif category == Constants.HEALTH_CARE:
            self.HEALTHCAREtweets.append(tweet)

        elif category == Constants.IMMIGRATION:
            self.IMMIGRATIONtweets.append(tweet)

        elif category == Constants.NATIONAL_SECURITY:
            self.NATSECURITYtweets.append(tweet)

    def getTweetsByCategory(self, category):
        if category == Constants.CORONA_VIRUS:
            return self.CORONAtweets

        elif category == Constants.ECONOMY:
            return self.ECONOMYtweets

        elif category == Constants.CLIMATE_CHANGE:
            return self.CLIMATEtweets

        elif category == Constants.HEALTH_CARE:
            return self.HEALTHCAREtweets

        elif category == Constants.IMMIGRATION:
            return self.IMMIGRATIONtweets

        elif category == Constants.NATIONAL_SECURITY:
            return self.NATSECURITYtweets

    def addSentimentVal(self, category, score):
        if category == Constants.CORONA_VIRUS:
            self.CORONAscores.append(score)

        elif category == Constants.ECONOMY:
            self.ECONOMYscores.append(score)

        elif category == Constants.CLIMATE_CHANGE:
            self.CLIMATEscores.append(score)

        elif category == Constants.HEALTH_CARE:
            self.HEALTHCAREscores.append(score)

        elif category == Constants.IMMIGRATION:
            self.IMMIGRATIONscores.append(score)

        elif category == Constants.NATIONAL_SECURITY:
            self.NATSECURITYscores.append(score)

    def getCategoryAverage(self, category):
        if category == Constants.CORONA_VIRUS:
            return self.CORONAavg
        elif category == Constants.ECONOMY:
            return self.ECONOMYavg
        elif category == Constants.CLIMATE_CHANGE:
            return self.CLIMATEavg
        elif category == Constants.HEALTH_CARE:
            return self.HEALTHCAREavg
        elif category == Constants.IMMIGRATION:
            return self.IMMIGRATIONavg
        elif category == Constants.NATIONAL_SECURITY:
            return self.NATSECURITYavg

    def getTwitteruName(self):
        self.twitterusername = None

    def setTwitteruName(self, name):
        self.twitterusername = name

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
