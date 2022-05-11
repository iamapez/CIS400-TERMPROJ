# Kyle Maiorana
# Alexander Perez, acperez@syr.edu
# Streamlit Frontend
import os

from cgi import test
from email import header
import streamlit as st
from PIL import Image
import json
import random
from pathlib import Path
import pickle
import Candidate
import os

# Loading from JSON to file function from cookbook
def load_json(filename):
    with open('{0}.json'.format(filename),
              'r', encoding='utf-8') as f:
        return json.load(f)

#style loading
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#pickle function to retrieve from data to py object
def getObjectsFromPickleDir():
    listOfCandidateObjects = list()
    tmp = os.getcwd()
    os.chdir('../assets/CandidateData')
    for filename in os.listdir(os.getcwd()):
        infile = open(filename, 'rb')
        z = pickle.load(infile)
        listOfCandidateObjects.append(z)

    return listOfCandidateObjects

#title creation
headerImage = Image.open(r'assets\electionwiz.png')
st.image(headerImage)

frontendBase = Path('../frontend')

# objects are stored in the following list
testListObjs = getObjectsFromPickleDir()

#need to switch directory
os.chdir('../../frontend/')

st.markdown("<h3 style='text-align: center; color: white;text-decoration-line: underline;'>Make your Data Selections</h3>", unsafe_allow_html=True)    #Radio selector for issue
issueOptions = ['Economy', 'Coronavirus', 'Healthcare', 'National Security', 'Climate Change', 'Immigration']
issue = st.selectbox("Please select a divisive issue from the dropdown list:", issueOptions)
#st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}text-align: center;</style>', unsafe_allow_html=True)
# print("This is cwd " , os.getcwd())

#Image column array for images of issues
col1, col2, col3= st.columns(3)
with col1:
    if issue == "Economy":
        image = Image.open(r'assets\issues\economy.jpeg')
    else:
        image = Image.open(r'assets\issues\economyblur.jpeg')
    st.image(image)
    if issue == "National Security":
        image = Image.open(r'assets\issues\national-security.jpg')
    else:
        image = Image.open(r'assets\issues\national-securityblur.jpg')
    st.image(image)
with col2:
    if issue == "Coronavirus":
        image = Image.open(r'assets\issues\covid.jpg')
    else:
        image = Image.open(r'assets\issues\covidblur.jpg')
    st.image(image)
    if issue == "Climate Change":
        image = Image.open(r'assets\issues\climate-change.jpg')
    else:
        image = Image.open(r'assets\issues\climate-changeblur.jpg')
    st.image(image)
with col3:
    if issue == "Healthcare":
        image = Image.open(r'assets\issues\healthcare.jpg')
    else:
        image = Image.open(r'assets\issues\healthcareblur.jpg')
    st.image(image)
    if issue == "Immigration":
        image = Image.open(r'assets\issues\immigration.jpg')
    else:
        image = Image.open(r'assets\issues\immigrationblur.jpg')
    st.image(image)


#Radio selector for state/race
candidateInfo = load_json("CLEANED_DATA")
listOfStateNames = []
for state in candidateInfo['states']:
    listOfStateNames.append(state.get('state_name'))

state = st.selectbox("Please select a Senate race to investigate:", listOfStateNames)
markdownString = "<h4 style='text-align: center; color: white;'>You are comparing the issue of " + str(issue).lower() + " between candidates in the " + str(state) + " Senate race.</h4>"
st.markdown(markdownString, unsafe_allow_html=True)

# it is neccessary to clean up the names of the issues
# because the dropdown names don't match the database
issueCleaned = ""
if issue == 'Economy':
    issueCleaned = "ECONOMY"
elif issue == 'Coronavirus':
    issueCleaned = "CORONA"
elif issue == 'Healthcare':
    issueCleaned = "HEALTHCARE"
elif issue == 'National Security':
    issueCleaned = "NATSECURITY"
elif issue == 'Climate Change':
    issueCleaned = "CLIMATE"
elif issue == 'Immigration':
    issueCleaned = "IMMIGRATION"

#Candidate Profiles
#Image column array
candidateCol1, candidateCol2, candidateCol3 ,candidateCol4 = st.columns(4)
stateIndex = listOfStateNames.index(state)
list1 = [10.2, 12.0, 53.7, 74.1, 25.7, 46.4, 10.8, 20.9, 34.5, 82.1, 39.4, 18.0]
valueNumber = round(random.choice(list1),1)
secondVal = round((100-valueNumber), 1)

#Cleaning candidate names for comparison and resource locating
demName = candidateInfo['states'][stateIndex]['democrat']
demNameCleaned = demName.replace(" ", "").lower()
repName = candidateInfo['states'][stateIndex]['republican']
repNameCleaned = repName.replace(" ", "").lower()

#capturing the percentages and tweets of the selected races
repPercent = 0.0
demPercent = 0.0
repTweet = ""
demTweet = ""
tweetCall = issueCleaned + "tweets"
avgCall = issueCleaned + "avg"
for candidate in testListObjs:
    if(candidate.name == repName):
        try:
            repTweet = getattr(candidate, tweetCall)
        except:
            repTweet = "No Tweet Found"
        repPercent = round(getattr(candidate, avgCall), 1)
    if(candidate.name == demName):
        try:
            demTweet = getattr(candidate, tweetCall)
        except:
            demTweet = "No Tweet Found"
        demPercent = round(getattr(candidate, avgCall), 1)

#If there isn't data for one candidate, and the other does, make equal
if(repPercent == 0 and demPercent != 0):
    repPercent = 1-demPercent
elif(repPercent != 0 and demPercent == 0):
    demPercent = 1-repPercent

#display columns for candidate information
with candidateCol1:
    st.markdown("\n\n")
    valString = str(100*round(demPercent,1))+ "%"
    st.metric(label="Twitter Opinion", value=valString)
assetsCandidates = Path('assets/candidates')
with candidateCol2:
    demPathString = 'assets\\candidates\\' + demNameCleaned + '.jpg'
    st.markdown("<h4 style='text-align: center; color: white;text-decoration-line: underline;'>Democrat</h4>", unsafe_allow_html=True)
    image = Image.open(demPathString)
    st.image(image, caption=demName)

with candidateCol3:
    st.markdown("<h4 style='text-align: center; color: white;text-decoration-line: underline;'>Republican</h4>", unsafe_allow_html=True)
    repPathString = 'assets\\candidates\\' + repNameCleaned + '.jpg'
    image = Image.open(repPathString)
    st.image(image, caption=repName)
with candidateCol4:
    st.markdown("\n\n")
    valString2 = str(100*round(repPercent,1))+ "%"
    st.metric(label="Twitter Opinion", value=valString2)

#displaying tweet information
st.markdown("<h4 style='text-align: center; color: white;'>Sample tweet examples from the mined Twitter dataset:</h4>", unsafe_allow_html=True)
with st.expander("Democrats"):
    if len(demTweet) != 0:
        for tweet in demTweet:
            st.text(tweet)
    else:
        st.text("\nNo Tweets at this time.")
        
with st.expander("Republicans"):
    if len(repTweet) != 0:
        for tweet in repTweet:
            st.text(tweet)
    else:
        st.text("\nNo Tweets at this time.")