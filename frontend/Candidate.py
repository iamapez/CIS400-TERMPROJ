<<<<<<< HEAD
# Alexander C. Perez, acperez@syr.edu
import json
import Constants


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

        self.ECONOMYavg = []
        self.CORONAavg = []
        self.HEALTHCAREavg = []
        self.NATSECURITYavg = []
        self.CLIMATEavg = []
        self.IMMIGRATIONavg = []

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def Average(self, lst):
        try:
            return sum(lst) / len(lst)
        except ZeroDivisionError:
            return 0

    def setAverages(self):
        # set economy
        self.ECONOMYavg = self.Average(self.ECONOMYscores)
        # set corona
        self.CORONAavg = self.Average(self.CORONAscores)
        # set healthcare
        self.HEALTHCAREavg = self.Average(self.HEALTHCAREscores)
        # natsecurity
        self.NATSECURITYavg = self.Average(self.NATSECURITYscores)
        # climate
        self.CLIMATEavg = self.Average(self.CLIMATEscores)
        # immigration
        self.IMMIGRATIONavg = self.Average(self.IMMIGRATIONscores)


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
=======
# Alexander C. Perez, acperez@syr.edu
import json
import backend.Constants


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

        self.ECONOMYavg = []
        self.CORONAavg = []
        self.HEALTHCAREavg = []
        self.NATSECURITYavg = []
        self.CLIMATEavg = []
        self.IMMIGRATIONavg = []

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def Average(self, lst):
        try:
            return sum(lst) / len(lst)
        except ZeroDivisionError:
            return 0

    def setAverages(self):
        # set economy
        self.ECONOMYavg = self.Average(self.ECONOMYscores)
        # set corona
        self.CORONAavg = self.Average(self.CORONAscores)
        # set healthcare
        self.HEALTHCAREavg = self.Average(self.HEALTHCAREscores)
        # natsecurity
        self.NATSECURITYavg = self.Average(self.NATSECURITYscores)
        # climate
        self.CLIMATEavg = self.Average(self.CLIMATEscores)
        # immigration
        self.IMMIGRATIONavg = self.Average(self.IMMIGRATIONscores)


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
>>>>>>> 0f36cb1 (ready to display data to frontend)
