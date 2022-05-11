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
        kellytweetsEconomy.append('https://twitter.com/CaptMarkKelly/status/1519722592503881733')
        kellytweetsEconomy.append('https://twitter.com/favour8854/status/1519003784919232514')
        kellytweetsCoronavirus.append('https://twitter.com/NeverAgainActn/status/1519051671250292740')
        kellytweetsCoronavirus.append('https://twitter.com/TheBabylonFlea/status/1511537706404356098')
        kellytweetsHealthcare.append('https://twitter.com/TgNgsti/status/1524156795601702912')
        kellytweetsHealthcare.append('https://twitter.com/CaptMarkKelly/status/1524114791500902401')
        kellytweetsNational.append('https://twitter.com/LMerritt1/status/1515067554737307651')
        kellytweetsNational.append('https://twitter.com/ResisterSis20/status/1520758073182326784')
        kellytweetsNational.append('https://twitter.com/jmrbux2/status/1520580641003388929')
        kellytweetsClimate.append('https://twitter.com/toronai22/status/1522188699576025089')
        kellytweetsClimate.append('https://twitter.com/PinkerbellPixie/status/1522350010783965190')
        kellytweetsClimate.append('https://twitter.com/TrainAdmirer54/status/1522042951156871169')
        kellytweetsImmigration.append('https://twitter.com/SavingAZ/status/1514304518409887751')
        kellytweetsImmigration.append('https://twitter.com/_JustinOlson/status/1490747189802323969')
        kellytweetsImmigration.append('https://twitter.com/postingtwink/status/1357496951944720387')

    elif obj.name == 'Mark Bronvich':
        bronvichtweetsImmigration.append('https://twitter.com/eloisetaylor700/status/1470098435835453441')
        bronvichtweetsImmigration.append('https://twitter.com/rghoover1/status/1513012167661875206')
        bronvichtweetsClimate.append('https://twitter.com/eloisetaylor700/status/1470098435835453441')
        bronvichtweetsClimate.append('https://twitter.com/LmckCdaUsa/status/1395468751865319425')
        bronvichtweetsClimate.append('https://twitter.com/CPO_JOE/status/1389649399760838657')
        bronvichtweetsNational.append('https://twitter.com/mojoman04/status/1488986277772873728')
        bronvichtweetsHealthcare.append('https://twitter.com/DaveMoore20/status/1470963469302198272')
        bronvichtweetsCoronavirus.append('https://twitter.com/CodyLillich/status/1518701574389833728')
        bronvichtweetsEconomy.append('https://twitter.com/rachelleingang/status/1492200524191395841')

    elif obj.name == 'Raphael Warnock':
        warnocktweetsImmigration.append('https://twitter.com/JacobRubashkin/status/1335985325433376771')
        warnocktweetsImmigration.append('https://twitter.com/evamckend/status/1512044837670903815')
        warnocktweetsClimate.append('https://twitter.com/ZerlinaShow/status/1339000238372229121')
        warnocktweetsNational.append('https://twitter.com/DavidNir/status/1341799638383390726')
        warnocktweetsHealthcare.append('https://twitter.com/Sbh08Mae/status/1425916945199677446')
        warnocktweetsCoronavirus.append('https://twitter.com/kylegriffin1/status/1345172961762766848')
        warnocktweetsEconomy.append('https://twitter.com/gsjh59/status/1335405096012800003 ')
    elif obj.name == 'Herschel Walker':
        walkertweetsImmigration.append('https://twitter.com/mattyhoovee/status/1521537727023439872')
        walkertweetsClimate.append('https://twitter.com/legalweed4sc/status/1517566811826438144')
        walkertweetsNational.append('https://twitter.com/acyn/status/1521651031557349376')
        walkertweetsHealthcare.append('https://twitter.com/dawnblueberry/status/1521372160266162176')
        walkertweetsCoronavirus.append('https://twitter.com/peeotus_donald/status/1520022578684993536')
        walkertweetsEconomy.append('https://twitter.com/leslieoo7/status/1477697068403769391')
    elif obj.name == 'Val Demings':
        demingstweetsImmigration.append('https://twitter.com/kellySueMcM/status/1515299549966999553')
        demingstweetsImmigration.append('https://twitter.com/marcorubio/status/1511658119457394689')
        demingstweetsClimate.append('https://twitter.com/ProudAFAmerican/status/1462160518114807809')
        demingstweetsNational.append('https://twitter.com/ABC/status/1224369410892275713')
        demingstweetsHealthcare.append('https://twitter.com/TonyHussein4/status/1522356239656792065')
        demingstweetsCoronavirus.append('https://twitter.com/AAReports/status/1265023222434725888')
        demingstweetsEconomy.append('https://twitter.com/rklotz/status/1443623332545536010')
    elif obj.name == 'Marco Rubio':
        rubiotweetsImmigration.append('https://twitter.com/Thenina77/status/1521235656990597120')
        rubiotweetsClimate.append('https://twitter.com/LivviesJam/status/1522257145416359940')
        rubiotweetsNational.append('https://twitter.com/SenRickScott/status/1523355850483453952')
        rubiotweetsHealthcare.append('https://twitter.com/MsDFernandez/status/1522332453930688512')
        rubiotweetsCoronavirus.append('https://twitter.com/SharinStone/status/1522299013621600256')
        rubiotweetsEconomy.append('https://twitter.com/bobhasdogsagain/status/1521232886342602754')
        rubiotweetsImmigration.append('https://twitter.com/Skyward_Link/status/1521476293434519552')
        rubiotweetsClimate.append('https://twitter.com/huthml/status/1522349837601042433')
        rubiotweetsNational.append('https://twitter.com/FoxBusiness/status/1522448607584133123')
        rubiotweetsHealthcare.append('https://twitter.com/VirginiaLoughn1/status/1523584354685165568')
        rubiotweetsCoronavirus.append('https://twitter.com/GrandRevivalYay/status/1520365573359771654')
        rubiotweetsEconomy.append('https://twitter.com/FGomez7')
    elif obj.name == 'Catherine Cortez Masto':
        mastotweetsImmigration.extend(['https://twitter.com/kylegriffin1/status/836416231091679233','https://twitter.com/doglips13/status/1487971427147870212'])
        mastotweetsClimate.append('https://twitter.com/doglips13/status/1486048817841508352')
        mastotweetsNational.append('https://twitter.com/EENewsUpdates/status/1105206239238283269')
        mastotweetsHealthcare.append('https://twitter.com/doglips13/status/1518617322285518849')
        mastotweetsCoronavirus.append('https://twitter.com/NevadaPEP/status/1285336431720665088')
        mastotweetsEconomy.append('https://twitter.com/doglips13/status/1486048817841508352')
    elif obj.name == 'Sam Brown':
        browntweetsImmigration.append('https://twitter.com/jme214/status/24071261842')
        browntweetsClimate.extend(['https://twitter.com/mrmcplad/status/1207017493190995968','https://twitter.com/owenwitesman/status/1207117429920260096'])
        browntweetNationals.append('https://twitter.com/mandy_pops/status/1315483345740947459')
        browntweetsHealthcare.append('https://twitter.com/palmerreuther/status/994786873766760448')
        browntweetsCoronavirus.extend(['https://twitter.com/michaelcweir/status/1476605807110373379','https://twitter.com/PharmerCody/status/1441109803326005251'])
        browntweetsEconomy.extend(['https://twitter.com/MYSTIK999/status/265994917917122561','https://twitter.com/timatotoro/status/1441125470687293446'])
    elif obj.name == 'Mandela Barnes':
        barnestweetsImmigration.append('https://twitter.com/js_newswatch/status/1043336090029936640')
        barnestweetsClimate.append('https://twitter.com/MSNBC/status/1262737798861373441')
        barnestweetsNational.append('https://twitter.com/kinley_brenda/status/1521915268624232448')
        barnestweetsHealthcare.append('https://twitter.com/bambooshooti/status/1516029122853720065')
        barnestweetsCoronavirus.append('https://twitter.com/WI_Justice/status/1248679683782316033')
        barnestweetsEconomy.append('https://twitter.com/3M_MarkM/status/1490865252296269824')
    elif obj.name == 'Ron Johnson':
        johnsontweetsImmigration.extend(['https://twitter.com/thehill/status/1523671884096675840','https://twitter.com/planetd1/status/1522125199730171904'])
        johnsontweetsClimate.extend(['https://twitter.com/AngelicRadical/status/1523055412706422784','https://twitter.com/Kenosha_News/status/1522713337225793536'])
        johnsontweetsNational.extend(['https://twitter.com/smb_democracy/status/1520614300360056832','https://twitter.com/AndrewDesiderio/status/1522293138311856135'])
        johnsontweetsHealthcare.extend(['https://twitter.com/AmerIndependent/status/1522188110129475585','https://twitter.com/thehill/status/1523671884096675840'])
        johnsontweetsCoronavirus.extend(['https://twitter.com/pbump/status/1521601793796497414','https://twitter.com/nathaliejacoby1/status/1522232054724931585'])
        johnsontweetsEconomy.extend(['https://twitter.com/leslsenior/status/1480757497933697026','https://twitter.com/SenRonJohnson/status/1444105166580600833','https://twitter.com/mmpadellan/status/1437295683262877698'])
    elif obj.name == 'Cheri Beasley':
        beasleytweetsImmigration.append('https://twitter.com/BlueAmericaProj/status/1409508511608979457')
        beasleytweetsClimate.append('https://twitter.com/AymannJames/status/1490784055968759812')
        beasleytweetsNational.append('https://twitter.com/NCPublicSafety/status/1205850235152543744')
        beasleytweetsHealthcare.append('https://twitter.com/kinley_brenda/status/1521872495934124032')
        beasleytweetsCoronavirus.append('https://twitter.com/NCCourts/status/1283772129016778759')
        beasleytweetsEconomy.append('https://twitter.com/NCStateAFLCIO/status/1468211432957390848')
    elif obj.name == 'Ted Budd':
        buddtweetsImmigration.append('https://twitter.com/akoren/status/859458781834616832')
        buddtweetsClimate.append('https://twitter.com/adivawoman/status/967967708968079360')
        buddtweetsNational.append('https://twitter.com/v3vjelly/status/1283576834869714944')
        buddtweetsHealthcare.append('https://twitter.com/TimH3401/status/861936472861134848')
        buddtweetsCoronavirus.append('https://twitter.com/Cornpop4Trump45/status/1245408805690769409')
        buddtweetsEconomy.append('https://twitter.com/BizRoundtable/status/1208158148932059137')
    elif obj.name == 'John Fetterman':
        fettermantweetsImmigration.extend(['https://twitter.com/JohnFetterman/status/1014517531472785408','https://twitter.com/bright1950start/status/1490413307907432450'])
        fettermantweetsClimate.extend(['https://twitter.com/robmonk/status/1522651322981310464','https://twitter.com/MFreyPGA/status/1524162010409279495'])
        fettermantweetsNational.extend(['https://twitter.com/Bowiegrrl1/status/1524037796524134402','https://twitter.com/kshap69/status/1524139931840532480'])
        fettermantweetsHealthcare.append('https://twitter.com/parthenonwin/status/1521375588157636609')
        fettermantweetsCoronavirus.extend(['https://twitter.com/BillyBobBillyJ/status/1523053059265675264','https://twitter.com/ShaneShoemaker6/status/1522426458005778432','https://twitter.com/BwCueball/status/1521617891686334464'])
        fettermantweetsEconomy.extend(['https://twitter.com/BluishCheckMark/status/1524171098774024195','https://twitter.com/kbabz2/status/1522720739329290240','https://twitter.com/edziu7777777/status/1523380428912082945'])
    elif obj.name == 'David Mccormick':
        mccormicktweetsImmigration.extend(['https://twitter.com/MillerStream/status/1513087044318216193','https://twitter.com/Calebej37/status/1524154946341511168'])
        mccormicktweetsClimate.extend(['https://twitter.com/RetiredLady7/status/1512083258174894083','https://twitter.com/PatBelam/status/1511110882889289738','https://twitter.com/ipatch012/status/1217190730432569344'])
        mccormicktweetsNational.extend(['https://twitter.com/DaveMcCormickPA/status/1501338873712058369','https://twitter.com/DaveMcCormickPA/status/1516804130672570373'])
        mccormicktweetsHealthcare.extend(['https://twitter.com/votethemout13/status/1520038499000496128','https://twitter.com/Gresh7D/status/1521312283628027904'])
        mccormicktweetsCoronavirus.extend(['https://twitter.com/Gresh7D/status/1521312283628027904','https://twitter.com/dw_subbed/status/1522271408411324420'])
        mccormicktweetsEconomy.extend(['https://twitter.com/Paokhons/status/1522013639900868614','https://twitter.com/DaveMcCormickPA/status/1523770947840331776'])
    elif obj.name == 'Tim Ryan':
        ryantweetsImmigration.extend(['https://twitter.com/QuynhMontgomery/status/1524082747026788352','https://twitter.com/Tracyyarchi/status/1522928623350599680'])
        ryantweetsClimate.extend(['https://twitter.com/schriAlphi/status/1524158711505240065','https://twitter.com/CbusPaulieD1977/status/1524051948353331200'])
        ryantweetsNational.extend(['https://twitter.com/TaraGat49825571/status/1524191365588045826','https://twitter.com/lovesanimals/status/1524178803760713734'])
        ryantweetsHealthcare.extend(['https://twitter.com/TimRyan/status/1523327912828563459','https://twitter.com/Brasilmagic/status/1523671803352485888'])
        ryantweetsCoronavirus.extend(['https://twitter.com/kojak756/status/1524146267902726144','https://twitter.com/BookNerd73/status/1524021946303881216'])
        ryantweetsEconomy.extend(['https://twitter.com/dgozinia919/status/1524091864978182145','https://twitter.com/NewGuardsRising/status/1523808274453307392'])
    elif obj.name == 'Josh Mandel':
        mandeltweetsImmigration.extend(['https://twitter.com/IChoseAnother1/status/1521179968100728832','https://twitter.com/MCS_BlueVoter/status/1520796850252615680'])
        mandeltweetsClimate.append('https://twitter.com/MajicAnt/status/1520831644327989248')
        mandeltweetsNational.extend(['https://twitter.com/LennyDykstra/status/1522271801551769600','https://twitter.com/news_ntd/status/1522045992702459904'])
        mandeltweetsHealthcare.append('https://twitter.com/Roberti06733390/status/1521280096799268865')
        mandeltweetsCoronavirus.extend(['https://twitter.com/ThatLawyerJeff/status/1521569538889854976', 'https://twitter.com/Roberti06733390/status/1521280096799268865'])
        mandeltweetsEconomy.append('https://twitter.com/HotlineJosh/status/1521846813233401856')

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
