# Alexander C. Perez, acperez@syr.edu
# this will serve as the main python file for the twitter api


import os
import twitterapi
import json
from Candidate import Candidate
from googlesearch import search
import twitterAPIcredents
import shutil
from Constants import *
import threading
import queue
import SentimentAnalysis as SA
import time
import pickle

global CandidateDataFromExistingJSON


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


def getUserObjectsFromCandidateData():
    pathToDataJSON = 'assets/CandidateData'
    # iterate over files in
    # that directory

    os.chdir('../assets/Persistance')

    listOfUserObjects = list()
    for filename in os.listdir(os.getcwd()):
        dataFILE = open(filename)
        UserAsDICT = json.load(dataFILE)
        UserObject = Candidate(my_dict=UserAsDICT)
        UserObject.name = UserAsDICT['name']
        UserObject.state = UserAsDICT['state']
        UserObject.party = UserAsDICT['party']
        UserObject.twitterusername = UserAsDICT['twitterusername']

        UserObject.ECONOMYtweets = UserAsDICT['ECONOMYtweets']
        UserObject.CORONAtweets = UserAsDICT['CORONAtweets']
        UserObject.HEALTHCAREtweets = UserAsDICT['HEALTHCAREtweets']
        UserObject.NATSECURITYtweets = UserAsDICT['NATSECURITYtweets']
        UserObject.CLIMATEtweets = UserAsDICT['CLIMATEtweets']
        UserObject.IMMIGRATIONtweets = UserAsDICT['IMMIGRATIONtweets']

        UserObject.ECONOMYscores = UserAsDICT['ECONOMYscores']
        UserObject.CORONAscores = UserAsDICT['CORONAscores']
        UserObject.HEALTHCAREscores = UserAsDICT['HEALTHCAREscores']
        UserObject.NATSECURITYscores = UserAsDICT['NATSECURITYscores']
        UserObject.CLIMATEscores = UserAsDICT['CLIMATEscores']
        UserObject.IMMIGRATIONscores = UserAsDICT['IMMIGRATIONscores']

        UserObject.ECONOMYavg = UserAsDICT['ECONOMYavg']
        UserObject.CORONAavg = UserAsDICT['CORONAavg']
        UserObject.HEALTHCAREavg = UserAsDICT['HEALTHCAREavg']
        UserObject.NATSECURITYavg = UserAsDICT['NATSECURITYavg']
        UserObject.CLIMATEavg = UserAsDICT['CLIMATEavg']
        UserObject.IMMIGRATIONavg = UserAsDICT['IMMIGRATIONavg']

        listOfUserObjects.append(UserObject)

    return listOfUserObjects


def main():
    """
    Entry point for our backend code.
    :return: exit code status
    """

    apez_Authenticated = twitterapi.oauth_login(twitterAPIcredents.apez_consumerKey,
                                                twitterAPIcredents.apez_consumerSecret,
                                                twitterAPIcredents.apez_oauthtoken,
                                                twitterAPIcredents.apez_oauthsecret)  # authenticate apez api key and store it here

    kyleB_Authenticated = twitterapi.oauth_login(twitterAPIcredents.kyleB_consumerKey,
                                                 twitterAPIcredents.kyleB_consumerSecret,
                                                 twitterAPIcredents.kyleB_oauthtoken,
                                                 twitterAPIcredents.kyleB_oauthsecret)

    liz_Authenticated = twitterapi.oauth_login(twitterAPIcredents.liz_consumerKey,
                                               twitterAPIcredents.liz_consumerSecret,
                                               twitterAPIcredents.liz_oauthtoken,
                                               twitterAPIcredents.liz_oauthsecret)

    # New method to get the users from the CandidateData folder
    global CandidateDataFromExistingJSON
    CandidateDataFromExistingJSON = getUserObjectsFromCandidateData()
    localClassifier = SA.setup()

    # assign Alex thread to CandidateDataFromExistingJSON to 0-2
    # assign KyleM thread to CandidateDataFromExistingJSON to 3-5
    # assign KyleB thread to CandidateDataFromExistingJSON to 6-8
    # assign Liz thread to CandidateDataFromExistingJSON to 9-11
    # assign Kayla thread to CandidateDataFromExistingJSON to 12-14
    # assign Fiona thread to CandidateDataFromExistingJSON to 15-16
    while True:
        for localCandidate in CandidateDataFromExistingJSON:
            response = twitterapi.getTweetsJSONByKeyword(liz_Authenticated, localCandidate.twitterusername)
            for tweetData in response:
                if any(ext in tweetData['text'] for ext in Constants.ECONOMY_KEYWORDS):
                    localTweet = tweetData['text']
                    print('checking', localTweet)
                    isdup = False
                    for i in localCandidate.ECONOMYtweets:
                        first23tweet = localTweet[:-23]
                        verifyString = i[:-23]
                        if localTweet[:-23] == i[:-23]:
                            print('DUPLICATE!!')
                            isdup = True
                            break
                    if not isdup:
                        print('added to{}{}'.format(localCandidate.name, Constants.ECONOMY))
                        localCandidate.ECONOMYtweets.append(localTweet)
                        localSentiment = SA.getSentimentOnTweet(localClassifier, localTweet)
                        print('Classification:', localSentiment)
                        if localSentiment == 'Positive':
                            localCandidate.ECONOMYscores.append(1)
                        else:
                            localCandidate.ECONOMYscores.append(0)
                        print()

                elif any(ext in tweetData['text'] for ext in Constants.CORONA_VIRUS_KEYWORDS):
                    localTweet = tweetData['text']
                    print('checking', localTweet)
                    first23tweet = localTweet[:-23]
                    isdup = False
                    for i in localCandidate.CORONAtweets:
                        verifyString = i[:-23]
                        if localTweet[:-23] == i[:-23]:
                            print('DUPLICATE!!')
                            isdup = True
                            break
                    if not isdup:
                        print('added to{}{}'.format(localCandidate.name, Constants.CORONA_VIRUS))
                        localCandidate.CORONAtweets.append(localTweet)
                        localSentiment = SA.getSentimentOnTweet(localClassifier, localTweet)
                        print('Classification:', localSentiment)
                        if localSentiment == 'Positive':
                            localCandidate.CORONAscores.append(1)
                        else:
                            localCandidate.CORONAscores.append(0)
                        print()

                elif any(ext in tweetData['text'] for ext in Constants.HEALTH_CARE_KEYWORDS):
                    localTweet = tweetData['text']
                    print('checking', localTweet)
                    first23tweet = localTweet[:-23]
                    isdup = False
                    for i in localCandidate.HEALTHCAREtweets:
                        verifyString = i[:-23]
                        if localTweet[:-23] == i[:-23]:
                            print('DUPLICATE!!')
                            isdup = True
                            break
                    if not isdup:
                        print('added to{}{}'.format(localCandidate.name, Constants.HEALTH_CARE))
                        localCandidate.HEALTHCAREtweets.append(localTweet)
                        localSentiment = SA.getSentimentOnTweet(localClassifier, localTweet)
                        print('Classification:', localSentiment)
                        if localSentiment == 'Positive':
                            localCandidate.HEALTHCAREscores.append(1)
                        elif localSentiment == 'Negative':
                            localCandidate.HEALTHCAREscores.append(0)
                        print()

                elif any(ext in tweetData['text'] for ext in Constants.NATIONAL_SECURITY_KEYWORDS):
                    localTweet = tweetData['text']
                    print('checking', localTweet)
                    first23tweet = localTweet[:-23]
                    isdup = False
                    for i in localCandidate.NATSECURITYtweets:
                        verifyString = i[:-23]
                        if localTweet[:-23] == i[:-23]:
                            print('DUPLICATE!!')
                            isdup = True
                            break
                        if not isdup:
                            print('added to{}{}'.format(localCandidate.name, Constants.NATIONAL_SECURITY))
                            localCandidate.NATSECURITYtweets.append(localTweet)
                            localSentiment = SA.getSentimentOnTweet(localClassifier, localTweet)
                            print('Classification:', localSentiment)
                            if localSentiment == 'Positive':
                                localCandidate.NATSECURITYscores.append(1)
                            else:
                                localCandidate.NATSECURITYscores.append(0)
                            print()

                elif any(ext in tweetData['text'] for ext in Constants.CLIMATE_CHANGE_KEYWORDS):
                    localTweet = tweetData['text']
                    print('checking', localTweet)
                    first23tweet = localTweet[:-23]
                    isdup = False
                    for i in localCandidate.CLIMATEtweets:
                        verifyString = i[:-23]
                        if localTweet[:-23] == i[:-23]:
                            print('DUPLICATE!!')
                            isdup = True
                            break
                    if not isdup:
                        print('added to{}{}'.format(localCandidate.name, Constants.CLIMATE_CHANGE))
                        localCandidate.CLIMATEtweets.append(localTweet)
                        localSentiment = SA.getSentimentOnTweet(localClassifier, localTweet)
                        print('Classification:', localSentiment)
                        if localSentiment == 'Positive':
                            localCandidate.CLIMATEscores.append(1)
                        else:
                            localCandidate.CLIMATEscores.append(0)
                        print()

                elif any(ext in tweetData['text'] for ext in Constants.IMMIGRATION_KEYWORDS):
                    localTweet = tweetData['text']
                    print('checking', localTweet)
                    first23tweet = localTweet[:-23]
                    isdup = False
                    for i in localCandidate.IMMIGRATIONtweets:
                        verifyString = i[:-23]
                        if localTweet[:-23] == i[:-23]:
                            print('DUPLICATE!!')
                            isdup = True
                            break
                    if not isdup:
                        print('added to{}{}'.format(localCandidate.name, Constants.IMMIGRATION))
                        localCandidate.IMMIGRATIONtweets.append(localTweet)
                        localSentiment = SA.getSentimentOnTweet(localClassifier, localTweet)
                        print('Tweet:', localTweet)
                        print('Classification:', localSentiment)
                        if localSentiment == 'Positive':
                            localCandidate.IMMIGRATIONscores.append(1)
                        else:
                            localCandidate.IMMIGRATIONscores.append(0)
                        print()

        time_wait = 60 * 5
        print('Sleeping for{}'.format(time_wait))
        time.sleep(time_wait)  # wait 10 minutes before re-running


def getUserFromFirstFour(str):
    global CandidateDataFromExistingJSON
    for i in CandidateDataFromExistingJSON:
        if str == i.name.replace(" ", "").strip()[0:5]:
            return i


if __name__ == "__main__":
    try:
        main()  # enter the main loop
    except KeyboardInterrupt:
        # catch when the program tries to exit
        # print('Interrupted')
        global CandidateDataFromExistingJSON

        # update the averages of each object
        for obj in CandidateDataFromExistingJSON:
            obj.setAverages()

        tmp = os.getcwd()
        os.chdir('../CandidateData')
        for filename in os.listdir(os.getcwd()):
            userObject = getUserFromFirstFour(filename[0:5])
            outfile = open(filename, 'wb')
            pickle.dump(userObject, outfile)
            outfile.close()

            # write this to a json file now in CandidateDataJSON folder
        print()
        exit(1)
        # export objects to json
