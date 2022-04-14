# Alexander C. Perez, acperez@syr.edu
import json


class Candidate:
    def __init__(self):
        self.dateOfElection = None
        self.county = None
        self.contestName = None
        self.nameOnBallot = None
        self.firstName = None
        self.lastName = None
        self.nickName = None
        self.streetAddress = None
        self.city = None
        self.state = None
        self.zipCode = None
        self.businessPhone = None
        self.email = None
        self.candidacyDT = None
        self.partyContest = None
        self.partyCandidate = None
        self.isUnexpired = None
        self.hasPrimary = None
        self.isPartisan = None
        self.voteFor = None
        self.term = None

    def __init__(self, row):
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

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
