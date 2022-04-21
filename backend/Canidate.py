# Alexander C. Perez, acperez@syr.edu
import json


class setFromRow:
    def __init__(self, dateOfElection=None, county=None, contestName=None,
                 nameOnBallot=None, firstName=None, lastName=None, nickName=None,
                 streetAddress=None, city=None, state=None, zipCode=None,
                 businessPhone=None, email=None, candidacyDT=None,
                 partyContest=None, partyCandidate=None, isUnexpired=None,
                 hasPrimary=None, isPartisan=None, voteFor=None,
                 term=None, twitterusername=None, ID=None, data=None, screenName=None,
                 name=None, location=None, description=None, followersCount=None,
                 friendsCount=None, isVerified=None):
        self.dateOfElection = dateOfElection
        self.county = county
        self.contestName = contestName
        self.nameOnBallot = nameOnBallot
        self.firstName = firstName
        self.lastName = lastName
        self.nickName = nickName
        self.streetAddress = streetAddress
        self.city = city
        self.state = state
        self.zipCode = zipCode
        self.businessPhone = businessPhone
        self.email = email
        self.candidacyDT = candidacyDT
        self.partyContest = partyContest
        self.partyCandidate = partyCandidate
        self.isUnexpired = isUnexpired
        self.hasPrimary = hasPrimary
        self.isPartisan = isPartisan
        self.voteFor = voteFor
        self.term = term
        self.twitterusername = twitterusername
        self.ID = ID
        self.data = data
        self.screenName = screenName
        self.name = name
        self.location = location
        self.description = description
        self.followersCount = followersCount
        self.friendsCount = friendsCount
        self.isVerified = isVerified

    def setFromRow(self, row):
        self.dateOfElection = row[0]
        self.county = row[1]
        self.contestName = row[2]
        self.nameOnBallot = row[3]
        self.firstName = row[4]
        self.lastName = row[6]
        self.nickName = row[8]
        self.streetAddress = row[9]
        self.city = row[10]
        self.state = row[11]
        self.zipCode = row[12]
        self.businessPhone = row[15]
        self.email = row[16]
        self.candidacyDT = row[17]
        self.partyContest = row[18]
        self.partyCandidate = row[19]
        self.isUnexpired = row[20]
        self.hasPrimary = row[21]
        self.isPartisan = row[22]
        self.voteFor = row[23]
        self.term = row[24]

    def getTwitteruName(self):
        self.twitterusername = None

    def setTwitteruName(self, name):
        self.twitterusername = name

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
