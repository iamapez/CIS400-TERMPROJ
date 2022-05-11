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
    for i in CandidateDataFromExistingJSON:
        updateObjectsPresetData(i)
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

def getSentimentPresent(listofurls):
    # takes in a url and gets tweet id
    # lookup tweet id get text
    # return avg
    tweets = []
    sentimentValues = []
    sentimentAvg = 0
    for url in listofurls:
        pass
        tweet = twitterapi.show_status(id=id_of_tweet)
        print(tweet['text'])
        # sentiment on tweet
        # append sentiment to list

    # return average of list

    return tweets, sentimentAvg

def updateObjectsPresetData(obj):
    bronvichtweetsEconomy = []
    bronvichtweetsCoronavirus = []
    bronvichtweetsHealthcare = []
    bronvichtweetsNational = []
    bronvichtweetsClimate = []
    bronvichtweetsImmigration = []
    kellytweetsEconomy = []
    kellytweetsCoronavirus = []
    kellytweetsHealthcare = []
    kellytweetsNational = []
    kellytweetsClimate = []
    kellytweetsImmigration = []
    warnocktweetsEconomy = []
    warnocktweetsCoronavirus = []
    warnocktweetsHealthcare = []
    warnocktweetsNational = []
    warnocktweetsClimate = []
    warnocktweetsImmigration = []
    warnock = [warnocktweetsImmigration, warnocktweetsClimate, warnocktweetsNational, warnocktweetsHealthcare,
               warnocktweetsCoronavirus, warnocktweetsEconomy]
    kelly = [kellytweetsEconomy, kellytweetsCoronavirus, kellytweetsHealthcare, kellytweetsNational, kellytweetsClimate,
             kellytweetsImmigration]
    bronvich = [bronvichtweetsEconomy, bronvichtweetsImmigration, bronvichtweetsClimate, bronvichtweetsNational,
                bronvichtweetsHealthcare, bronvichtweetsCoronavirus]
    walkertweetsEconomy = []
    walkertweetsCoronavirus = []
    walkertweetsHealthcare = []
    walkertweetsNational = []
    walkertweetsClimate = []
    walkertweetsImmigration = []
    walker = [walkertweetsImmigration, walkertweetsClimate, walkertweetsNational, walkertweetsHealthcare,
              walkertweetsCoronavirus, walkertweetsEconomy]
    demingstweetsEconomy = []
    demingstweetsCoronavirus = []
    demingstweetsHealthcare = []
    demingstweetsNational = []
    demingstweetsClimate = []
    demingstweetsImmigration = []
    demings = [demingstweetsImmigration, demingstweetsClimate, demingstweetsNational, demingstweetsEconomy,
               demingstweetsHealthcare, demingstweetsCoronavirus]
    rubiotweetsEconomy = []
    rubiotweetsCoronavirus = []
    rubiotweetsHealthcare = []
    rubiotweetsNational = []
    rubiotweetsClimate = []
    rubiotweetsImmigration = []
    rubio = [rubiotweetsImmigration, rubiotweetsClimate, rubiotweetsNational, rubiotweetsHealthcare,
             rubiotweetsCoronavirus, rubiotweetsEconomy]
    mastotweetsEconomy = []
    mastotweetsCoronavirus = []
    mastotweetsHealthcare = []
    mastotweetsNational = []
    mastotweetsClimate = []
    mastotweetsImmigration = []
    masto = [mastotweetsImmigration, mastotweetsClimate, mastotweetsNational, mastotweetsHealthcare,
             mastotweetsCoronavirus, mastotweetsEconomy]
    browntweetsEconomy = []
    browntweetsCoronavirus = []
    browntweetsHealthcare = []
    browntweetNationals = []
    browntweetsClimate = []
    browntweetsImmigration = []
    brown = [browntweetsImmigration, browntweetsClimate, browntweetsHealthcare, browntweetsCoronavirus,
             browntweetsEconomy, browntweetNationals]
    barnestweetsEconomy = []
    barnestweetsCoronavirus = []
    barnestweetsHealthcare = []
    barnestweetsNational = []
    barnestweetsClimate = []
    barnestweetsImmigration = []
    barnes = [barnestweetsImmigration, barnestweetsClimate, barnestweetsNational, barnestweetsHealthcare,
              barnestweetsCoronavirus, barnestweetsEconomy]
    johnsontweetsEconomy = []
    johnsontweetsCoronavirus = []
    johnsontweetsHealthcare = []
    johnsontweetsNational = []
    johnsontweetsClimate = []
    johnsontweetsImmigration = []
    johnson = [johnsontweetsImmigration, johnsontweetsClimate, johnsontweetsNational, johnsontweetsHealthcare,
               johnsontweetsCoronavirus, johnsontweetsEconomy]
    beasleytweetsEconomy = []
    beasleytweetsCoronavirus = []
    beasleytweetsHealthcare = []
    beasleytweetsNational = []
    beasleytweetsClimate = []
    beasleytweetsImmigration = []
    beasley = [beasleytweetsNational, beasleytweetsImmigration, beasleytweetsClimate, beasleytweetsHealthcare,
               beasleytweetsCoronavirus, beasleytweetsEconomy]
    buddtweetsEconomy = []
    buddtweetsCoronavirus = []
    buddtweetsHealthcare = []
    buddtweetsNational = []
    buddtweetsClimate = []
    buddtweetsImmigration = []
    budd = [buddtweetsImmigration, buddtweetsClimate, buddtweetsNational, buddtweetsHealthcare, buddtweetsCoronavirus,
            buddtweetsEconomy]
    fettermantweetsEconomy = []
    fettermantweetsCoronavirus = []
    fettermantweetsHealthcare = []
    fettermantweetsNational = []
    fettermantweetsClimate = []
    fettermantweetsImmigration = []
    fetterman = [fettermantweetsImmigration, fettermantweetsClimate, fettermantweetsNational, fettermantweetsHealthcare,
                 fettermantweetsCoronavirus, fettermantweetsEconomy]
    mccormicktweetsEconomy = []
    mccormicktweetsCoronavirus = []
    mccormicktweetsHealthcare = []
    mccormicktweetsNational = []
    mccormicktweetsClimate = []
    mccormicktweetsImmigration = []
    mccormick = [mccormicktweetsImmigration, mccormicktweetsClimate, mccormicktweetsNational, mccormicktweetsHealthcare,
                 mccormicktweetsCoronavirus, mccormicktweetsEconomy]
    mandeltweetsEconomy = []
    mandeltweetsCoronavirus = []
    mandeltweetsHealthcare = []
    mandeltweetsNational = []
    mandeltweetsClimate = []
    mandeltweetsImmigration = []
    madel = [mandeltweetsImmigration, mandeltweetsClimate, mandeltweetsNational, mandeltweetsEconomy,
             mandeltweetsHealthcare, mandeltweetsCoronavirus, mandeltweetsImmigration]
    ryantweetsEconomy = []
    ryantweetsCoronavirus = []
    ryantweetsHealthcare = []
    ryantweetsNational = []
    ryantweetsClimate = []
    ryantweetsImmigration = []
    ryan = [ryantweetsImmigration, ryantweetsClimate, ryantweetsNational, ryantweetsHealthcare, ryantweetsCoronavirus,
            ryantweetsEconomy, ryantweetsImmigration]

    if obj.name == 'Mark Kelly':
        kellytweetsEconomy.append('1519722592503881733')
        kellytweetsEconomy.append('1519003784919232514')
        kellytweetsCoronavirus.append('1519051671250292740')
        kellytweetsCoronavirus.append('1511537706404356098')
        kellytweetsHealthcare.append('1524156795601702912')
        kellytweetsHealthcare.append('1524114791500902401')
        kellytweetsNational.append('1515067554737307651')
        kellytweetsNational.append('1520758073182326784')
        kellytweetsNational.append('1520580641003388929')
        kellytweetsClimate.append('1522188699576025089')
        kellytweetsClimate.append('1522350010783965190')
        kellytweetsClimate.append('1522042951156871169')
        kellytweetsImmigration.append('1514304518409887751')
        kellytweetsImmigration.append('1490747189802323969')
        kellytweetsImmigration.append('1357496951944720387')

    elif obj.name == 'Mark Bronvich':
        bronvichtweetsImmigration.append('1470098435835453441')
        bronvichtweetsImmigration.append('1513012167661875206')
        bronvichtweetsClimate.append('1470098435835453441')
        bronvichtweetsClimate.append('1395468751865319425')
        bronvichtweetsClimate.append('1389649399760838657')
        bronvichtweetsNational.append('1488986277772873728')
        bronvichtweetsHealthcare.append('1470963469302198272')
        bronvichtweetsCoronavirus.append('1518701574389833728')
        bronvichtweetsEconomy.append('1492200524191395841')

    elif obj.name == 'Raphael Warnock':
        warnocktweetsImmigration.append('1335985325433376771')
        warnocktweetsImmigration.append('1512044837670903815')
        warnocktweetsClimate.append('1339000238372229121')
        warnocktweetsNational.append('1341799638383390726')
        warnocktweetsHealthcare.append('1425916945199677446')
        warnocktweetsCoronavirus.append('1345172961762766848')
        warnocktweetsEconomy.append('1335405096012800003 ')
    elif obj.name == 'Herschel Walker':
        walkertweetsImmigration.append('1521537727023439872')
        walkertweetsClimate.append('1517566811826438144')
        walkertweetsNational.append('1521651031557349376')
        walkertweetsHealthcare.append('1521372160266162176')
        walkertweetsCoronavirus.append('1520022578684993536')
        walkertweetsEconomy.append('1477697068403769391')
    elif obj.name == 'Val Demings':
        demingstweetsImmigration.append('1515299549966999553')
        demingstweetsImmigration.append('1511658119457394689')
        demingstweetsClimate.append('1462160518114807809')
        demingstweetsNational.append('1224369410892275713')
        demingstweetsHealthcare.append('1522356239656792065')
        demingstweetsCoronavirus.append('1265023222434725888')
        demingstweetsEconomy.append('1443623332545536010')
    elif obj.name == 'Marco Rubio':
        rubiotweetsImmigration.append('1521235656990597120')
        rubiotweetsClimate.append('1522257145416359940')
        rubiotweetsNational.append('1523355850483453952')
        rubiotweetsHealthcare.append('1522332453930688512')
        rubiotweetsCoronavirus.append('1522299013621600256')
        rubiotweetsEconomy.append('1521232886342602754')
        rubiotweetsImmigration.append('1521476293434519552')
        rubiotweetsClimate.append('1522349837601042433')
        rubiotweetsNational.append('1522448607584133123')
        rubiotweetsHealthcare.append('1523584354685165568')
        rubiotweetsCoronavirus.append('1520365573359771654')
        rubiotweetsEconomy.append('1521232886342602754')
    elif obj.name == 'Catherine Cortez Masto':
        mastotweetsImmigration.extend(['836416231091679233','1487971427147870212'])
        mastotweetsClimate.append('1486048817841508352')
        mastotweetsNational.append('1105206239238283269')
        mastotweetsHealthcare.append('1518617322285518849')
        mastotweetsCoronavirus.append('1285336431720665088')
        mastotweetsEconomy.append('1486048817841508352')
    elif obj.name == 'Sam Brown':
        browntweetsImmigration.append('e214/24071261842')
        browntweetsClimate.extend(['1207017493190995968','1207117429920260096'])
        browntweetNationals.append('1315483345740947459')
        browntweetsHealthcare.append('994786873766760448')
        browntweetsCoronavirus.extend(['1476605807110373379','1441109803326005251'])
        browntweetsEconomy.extend(['265994917917122561','1441125470687293446'])
    elif obj.name == 'Mandela Barnes':
        barnestweetsImmigration.append('1043336090029936640')
        barnestweetsClimate.append('1262737798861373441')
        barnestweetsNational.append('1521915268624232448')
        barnestweetsHealthcare.append('1516029122853720065')
        barnestweetsCoronavirus.append('1248679683782316033')
        barnestweetsEconomy.append('1490865252296269824')
    elif obj.name == 'Ron Johnson':
        johnsontweetsImmigration.extend(['1523671884096675840','1522125199730171904'])
        johnsontweetsClimate.extend(['1523055412706422784','1522713337225793536'])
        johnsontweetsNational.extend(['1520614300360056832','1522293138311856135'])
        johnsontweetsHealthcare.extend(['1522188110129475585','1523671884096675840'])
        johnsontweetsCoronavirus.extend(['1521601793796497414','1522232054724931585'])
        johnsontweetsEconomy.extend(['1480757497933697026','1444105166580600833','1437295683262877698'])
    elif obj.name == 'Cheri Beasley':
        beasleytweetsImmigration.append('1409508511608979457')
        beasleytweetsClimate.append('1490784055968759812')
        beasleytweetsNational.append('1205850235152543744')
        beasleytweetsHealthcare.append('1521872495934124032')
        beasleytweetsCoronavirus.append('1283772129016778759')
        beasleytweetsEconomy.append('1468211432957390848')
    elif obj.name == 'Ted Budd':
        buddtweetsImmigration.append('859458781834616832')
        buddtweetsClimate.append('967967708968079360')
        buddtweetsNational.append('1283576834869714944')
        buddtweetsHealthcare.append('861936472861134848')
        buddtweetsCoronavirus.append('1245408805690769409')
        buddtweetsEconomy.append('1208158148932059137')
    elif obj.name == 'John Fetterman':
        fettermantweetsImmigration.extend(['1014517531472785408','1490413307907432450'])
        fettermantweetsClimate.extend(['1522651322981310464','1524162010409279495'])
        fettermantweetsNational.extend(['1524037796524134402','1524139931840532480'])
        fettermantweetsHealthcare.append('1521375588157636609')
        fettermantweetsCoronavirus.extend(['1523053059265675264','1522426458005778432','1521617891686334464'])
        fettermantweetsEconomy.extend(['1524171098774024195','1522720739329290240','1523380428912082945'])
    elif obj.name == 'David Mccormick':
        mccormicktweetsImmigration.extend(['1513087044318216193','1524154946341511168'])
        mccormicktweetsClimate.extend(['1512083258174894083','1511110882889289738','1217190730432569344'])
        mccormicktweetsNational.extend(['1501338873712058369','1516804130672570373'])
        mccormicktweetsHealthcare.extend(['1520038499000496128','1521312283628027904'])
        mccormicktweetsCoronavirus.extend(['1521312283628027904','1522271408411324420'])
        mccormicktweetsEconomy.extend(['1522013639900868614','1523770947840331776'])
    elif obj.name == 'Tim Ryan':
        ryantweetsImmigration.extend(['1524082747026788352','1522928623350599680'])
        ryantweetsClimate.extend(['1524158711505240065','1524051948353331200'])
        ryantweetsNational.extend(['1524191365588045826','1524178803760713734'])
        ryantweetsHealthcare.extend(['1523327912828563459','1523671803352485888'])
        ryantweetsCoronavirus.extend(['1524146267902726144','1524021946303881216'])
        ryantweetsEconomy.extend(['1524091864978182145','1523808274453307392'])
    elif obj.name == 'Josh Mandel':
        mandeltweetsImmigration.extend(['1521179968100728832','1520796850252615680'])
        mandeltweetsClimate.append('1520831644327989248')
        mandeltweetsNational.extend(['1522271801551769600','1522045992702459904'])
        mandeltweetsHealthcare.append('1521280096799268865')
        mandeltweetsCoronavirus.extend(['1521569538889854976', '1521280096799268865'])
        mandeltweetsEconomy.append('1521846813233401856')

    cands = [kelly, ryan, madel, mccormick, fetterman, budd, beasley, johnson, barnes, brown, masto, rubio, demings,
             walker, warnock, bronvich]

    global CandidateDataFromExistingJSON
    for i in CandidateDataFromExistingJSON:
        if i.name == 'Mark Kelly':
            tweets = []
            tweets, sentiment = getSentimentPresent(cands[0][0])
            i.ECONOMYtweets.extend(tweets)
            i.ECONOMYavg = sentiment

            i.CORONAtweets.extend(cands[0][1])
            i.HEALTHCAREtweets.extend(cands[0][2])
            i.NATSECURITYtweets.extend(cands[0][3])
            i.CLIMATEtweets.extend(cands[0][4])
            i.IMMIGRATIONtweets.extend(cands[0][5])
        elif i.name == 'Mark Bronvich':
            i.ECONOMYtweets.extend(cands[0][0])
            i.CORONAtweets.extend(cands[0][1])
            i.HEALTHCAREtweets.extend(cands[0][2])
            i.NATSECURITYtweets.extend(cands[0][3])
            i.CLIMATEtweets.extend(cands[0][4])
            i.IMMIGRATIONtweets.extend(cands[0][5])
        elif i.name == 'Raphael Warnock':
            i.ECONOMYtweets.extend(cands[0][0])
            i.CORONAtweets.extend(cands[0][1])
            i.HEALTHCAREtweets.extend(cands[0][2])
            i.NATSECURITYtweets.extend(cands[0][3])
            i.CLIMATEtweets.extend(cands[0][4])
            i.IMMIGRATIONtweets.extend(cands[0][5])
        elif i.name == 'Herschel Walker':
            i.ECONOMYtweets.extend(cands[0][0])
            i.CORONAtweets.extend(cands[0][1])
            i.HEALTHCAREtweets.extend(cands[0][2])
            i.NATSECURITYtweets.extend(cands[0][3])
            i.CLIMATEtweets.extend(cands[0][4])
            i.IMMIGRATIONtweets.extend(cands[0][5])
        elif i.name == 'Val Demings':
            i.ECONOMYtweets.extend(cands[0][0])
            i.CORONAtweets.extend(cands[0][1])
            i.HEALTHCAREtweets.extend(cands[0][2])
            i.NATSECURITYtweets.extend(cands[0][3])
            i.CLIMATEtweets.extend(cands[0][4])
            i.IMMIGRATIONtweets.extend(cands[0][5])
        elif i.name == 'Marco Rubio':
            i.ECONOMYtweets.extend(cands[0][0])
            i.CORONAtweets.extend(cands[0][1])
            i.HEALTHCAREtweets.extend(cands[0][2])
            i.NATSECURITYtweets.extend(cands[0][3])
            i.CLIMATEtweets.extend(cands[0][4])
            i.IMMIGRATIONtweets.extend(cands[0][5])
        elif i.name == 'Catherine Cortez Masto':
            i.ECONOMYtweets.extend(cands[0][0])
            i.CORONAtweets.extend(cands[0][1])
            i.HEALTHCAREtweets.extend(cands[0][2])
            i.NATSECURITYtweets.extend(cands[0][3])
            i.CLIMATEtweets.extend(cands[0][4])
            i.IMMIGRATIONtweets.extend(cands[0][5])
        elif i.name == 'Sam Brown':
            i.ECONOMYtweets.extend(cands[0][0])
            i.CORONAtweets.extend(cands[0][1])
            i.HEALTHCAREtweets.extend(cands[0][2])
            i.NATSECURITYtweets.extend(cands[0][3])
            i.CLIMATEtweets.extend(cands[0][4])
            i.IMMIGRATIONtweets.extend(cands[0][5])
        elif i.name == 'Mandela Barnes':
            i.ECONOMYtweets.extend(cands[0][0])
            i.CORONAtweets.extend(cands[0][1])
            i.HEALTHCAREtweets.extend(cands[0][2])
            i.NATSECURITYtweets.extend(cands[0][3])
            i.CLIMATEtweets.extend(cands[0][4])
            i.IMMIGRATIONtweets.extend(cands[0][5])
        elif i.name == 'Ron Johnson':
            i.ECONOMYtweets.extend(cands[0][0])
            i.CORONAtweets.extend(cands[0][1])
            i.HEALTHCAREtweets.extend(cands[0][2])
            i.NATSECURITYtweets.extend(cands[0][3])
            i.CLIMATEtweets.extend(cands[0][4])
            i.IMMIGRATIONtweets.extend(cands[0][5])
        elif i.name == 'Cheri Beasley':
            i.ECONOMYtweets.extend(cands[0][0])
            i.CORONAtweets.extend(cands[0][1])
            i.HEALTHCAREtweets.extend(cands[0][2])
            i.NATSECURITYtweets.extend(cands[0][3])
            i.CLIMATEtweets.extend(cands[0][4])
            i.IMMIGRATIONtweets.extend(cands[0][5])
        elif i.name == 'Ted Budd':
            i.ECONOMYtweets.extend(cands[0][0])
            i.CORONAtweets.extend(cands[0][1])
            i.HEALTHCAREtweets.extend(cands[0][2])
            i.NATSECURITYtweets.extend(cands[0][3])
            i.CLIMATEtweets.extend(cands[0][4])
            i.IMMIGRATIONtweets.extend(cands[0][5])
        elif i.name == 'John Fetterman':
            i.ECONOMYtweets.extend(cands[0][0])
            i.CORONAtweets.extend(cands[0][1])
            i.HEALTHCAREtweets.extend(cands[0][2])
            i.NATSECURITYtweets.extend(cands[0][3])
            i.CLIMATEtweets.extend(cands[0][4])
            i.IMMIGRATIONtweets.extend(cands[0][5])
        elif i.name == 'David Mccormick':
            i.ECONOMYtweets.extend(cands[0][0])
            i.CORONAtweets.extend(cands[0][1])
            i.HEALTHCAREtweets.extend(cands[0][2])
            i.NATSECURITYtweets.extend(cands[0][3])
            i.CLIMATEtweets.extend(cands[0][4])
            i.IMMIGRATIONtweets.extend(cands[0][5])
        elif i.name == 'Tim Ryan':
            i.ECONOMYtweets.extend(cands[0][0])
            i.CORONAtweets.extend(cands[0][1])
            i.HEALTHCAREtweets.extend(cands[0][2])
            i.NATSECURITYtweets.extend(cands[0][3])
            i.CLIMATEtweets.extend(cands[0][4])
            i.IMMIGRATIONtweets.extend(cands[0][5])
        elif i.name == 'Josh Mandel':
            i.ECONOMYtweets.extend(cands[0][0])
            i.CORONAtweets.extend(cands[0][1])
            i.HEALTHCAREtweets.extend(cands[0][2])
            i.NATSECURITYtweets.extend(cands[0][3])
            i.CLIMATEtweets.extend(cands[0][4])
            i.IMMIGRATIONtweets.extend(cands[0][5])
    return

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
