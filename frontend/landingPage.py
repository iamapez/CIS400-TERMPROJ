# Kyle Maiorana
# Streamlit Frontend

from email import header
import streamlit as st
from PIL import Image
import json
import random

#Loading from JSON to file function from cookbook
def load_json(filename):
    with open('{0}.json'.format(filename), 
              'r', encoding='utf-8') as f:
        return json.load(f)

#title creation
#st.markdown("<h1 style='text-align: center; color: white;'>2022 Midterm Election\nTwitter Opinion Visualizer</h1>", unsafe_allow_html=True)
#st.markdown("<h5 style='text-align: center; color: white;'>Alex Perez, Fiona Powers, Kyle Maiorana, Liz Melo, Kayla Nieto, Kyle Betten</h5>", unsafe_allow_html=True)
headerImage = Image.open(r'assets\electionwiz.png')
st.image(headerImage)

#style loading
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: white;text-decoration-line: underline;'>Make your Data Selections</h3>", unsafe_allow_html=True)    #Radio selector for issue
issueOptions = ['Economy', 'Coronavirus', 'Healthcare', 'National Security', 'Climate Change']
issue = st.selectbox("Please select a divisive issue from the dropdown list:", issueOptions)
#st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}text-align: center;</style>', unsafe_allow_html=True)

#Image column array
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if issue == "Economy":
        image = Image.open(r'assets\issues\economy.jpeg')
    else:
        image = Image.open(r'assets\issues\economyblur.jpeg')
    st.image(image)
with col2:
    if issue == "Coronavirus":
        image = Image.open(r'assets\issues\covid.jpg')
    else:
        image = Image.open(r'assets\issues\covidblur.jpg')
    st.image(image)
with col3:
    if issue == "Healthcare":
        image = Image.open(r'assets\issues\healthcare.jpg')
    else:
        image = Image.open(r'assets\issues\healthcareblur.jpg')
    st.image(image)
with col4:
    if issue == "National Security":
        image = Image.open(r'assets\issues\national-security.jpg')
    else:
        image = Image.open(r'assets\issues\national-securityblur.jpg')
    st.image(image)
with col5:
    if issue == "Climate Change":
        image = Image.open(r'assets\issues\climate-change.jpg')
    else:
        image = Image.open(r'assets\issues\climate-changeblur.jpg')
    st.image(image)

#Radio selector for state/race
candidateInfo = load_json("CLEANED_DATA")
listOfStateNames = []
for state in candidateInfo['states']:
    listOfStateNames.append(state.get('state_name'))

state = st.selectbox("Please select a Senate race to investigate:", listOfStateNames)
markdownString = "<h4 style='text-align: center; color: white;'>You are comparing the issue of " + str(issue).lower() + " between candidates in the " + str(state) + " Senate race.</h4>"
st.markdown(markdownString, unsafe_allow_html=True)

#Candidate Profiles
#Image column array
candidateCol1, candidateCol2, candidateCol3 ,candidateCol4 = st.columns(4)
stateIndex = listOfStateNames.index(state)
list1 = [10.2, 12.0, 53.7, 74.1, 25.7, 46.4, 10.8, 20.9, 34.5, 82.1, 39.4, 18.0]
valueNumber = round(random.choice(list1),1)
secondVal = round((100-valueNumber), 1)
with candidateCol1:
    st.markdown("\n\n")
    valString = str(valueNumber)+ "%"
    st.metric(label="Twitter Opinion", value=valString)
with candidateCol2:
    demName = candidateInfo['states'][stateIndex]['democrat']
    demNameCleaned = demName.replace(" ", "").lower()
    demPathString = 'assets\\candidates\\' + demNameCleaned + '.jpg'
    st.markdown("<h4 style='text-align: center; color: white;text-decoration-line: underline;'>Democrat</h4>", unsafe_allow_html=True)
    image = Image.open(demPathString)
    st.image(image, caption=demName)

with candidateCol3:
    st.markdown("<h4 style='text-align: center; color: white;text-decoration-line: underline;'>Republican</h4>", unsafe_allow_html=True)
    repName = candidateInfo['states'][stateIndex]['republican']
    repNameCleaned = repName.replace(" ", "").lower()
    repPathString = 'assets\\candidates\\' + repNameCleaned + '.jpg'
    image = Image.open(repPathString)
    st.image(image, caption=repName)
with candidateCol4:
    st.markdown("\n\n")
    valString2 = str(secondVal)+ "%"
    st.metric(label="Twitter Opinion", value=valString2)



