# Alexander C. Perez, acperez@syr.edu
# this will serve as the main python file for the twitter api


import os
import twitterapi
import json
from Candidate import Candidate
from googlesearch import search


class Constants:
    Arizona = 'Arizona'
    Georgia = 'Georgia'
    Florida = 'Florida'
    Nevada = 'Nevada'
    Wisconsin = 'Wisconsin'
    North_Carolina = 'North Carolina'
    Pennsylvania = 'Pennsylvania'
    Ohio = 'Ohio'
    Democrat = 'Democrat'
    Republican = 'Republican'


def refreshOurObjects():
    """
    When we want to refresh our objects
    :return: list of refreshed Candidate objects
    """
    d = os.getcwd()
    os.chdir('assets/CandidateData')
    d = os.getcwd()

    listOfObjects = list()
    for filename in os.listdir(os.getcwd()):
        f = os.path.join(os.getcwd(), filename)
        # checking if it is a file
        if os.path.isfile(f):
            f = open(f)
            data = json.load(f)
            tempObject = Candidate(data['name'], data['state'], data['party'])
            if len(data['tweets']) > 0:
                tempObject.tweets = data['tweets']
            if data['twitterusername'] is not None:
                tempObject.twitterusername = data['twitterusername']

            listOfObjects.append(tempObject)

    return listOfObjects

def updateCandidateJSON(localCandidate):
    try:
        d = os.getcwd()
        os.chdir('assets/CandidateData')
        d = os.getcwd()

        localPATHName = localCandidate.name.replace(" ", "") + 'objDATA.json'
        with open(localPATHName, 'w') as outfile:
            outfile.write(localCandidate.toJSON())

    except Exception as e:
        print('Exception Thrown!', e)
        return -1

    return 1


def outputCandidatesToJSON(CandidateObjects):
    """
    Generate Each Candidates json file in assets/CandidateData/<name>+objDATA.json
    :return: -1 if exception caught, 1 if good
    """
    try:
        d = os.getcwd()
        os.chdir('assets/CandidateData')
        d = os.getcwd()
        for i in CandidateObjects:
            localPATHName = i.name.replace(" ", "") + 'objDATA.json'
            with open(localPATHName, 'w') as outfile:
                outfile.write(i.toJSON())
    except Exception as e:
        print('Exception Thrown!', e)
        return -1

    return 1


def populateDataFromJSON():
    pathToDataJSON = 'assets/CLEANED_DATA.json'
    d = os.getcwd()  # change directories to access the json file containing the data
    os.chdir("..")

    listOfObjects = list()

    # Opening JSON file
    f = open('assets/CLEANED_DATA.json')
    data = json.load(f)
    stateElections = data['state_elections']['states']
    for i in stateElections:
        localState = i['state_name']
        for dems in i['democrats']:
            listOfObjects.append(Candidate(dems, localState, Constants.Democrat))
        for repubs in i['republicans']:
            listOfObjects.append(Candidate(repubs, localState, Constants.Republican))

    print('here')
    return listOfObjects


def main():
    """
    Entry point for our backend code.
    :return: exit code status
    """

    # electionObjects = updateJSONData()            # only run this is we want to re initalize our data from the csv data file

    apez_Authenticated = twitterapi.getAuthenticated()  # authenticate apez api key and store it here

    CandidateObjects = populateDataFromJSON()

    # only run when we need to update ALL candidate objects
    # Generate our json files in assets/CandidateData/
    # if outputCandidatesToJSON(CandidateObjects) == -1:
    #     exit(-1)
    # else:
    #     pass


    # when we made changes to one candidate data call:
    #
    # if updateCandidateJSON(CandidateObjects[0]) == -1:
    #     exit(-1)
    # else:
    #     pass

    newObjects = refreshOurObjects()
    print()


    exit(1)


if __name__ == "__main__":
    main()
