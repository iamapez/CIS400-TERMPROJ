# Alexander C. Perez, acperez@syr.edu
import streamlit as st
from PIL import Image

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#title creation
st.markdown("<h1 style='text-align: center; color: white;'>2022 Midterm Election\nTwitter Opinion Visualizer</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: white;'>Alex Perez, Fiona Powers, Kyle Maiorana, Liz Melo, Kayla Nieto, Kyle Betten</h5>", unsafe_allow_html=True)

#Radio selector for issue
issueOptions = ['Economy', 'Coronavirus', 'Healthcare', 'National Security', 'Climate Change']
issue = st.selectbox("Please select a divisive issue:", issueOptions)
#st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}text-align: center;</style>', unsafe_allow_html=True)

#Image column array
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if issue == "Economy":
        image = Image.open(r'assets\economy.jpeg')
    else:
        image = Image.open(r'assets\economyblur.jpeg')
    st.image(image)
with col2:
    if issue == "Coronavirus":
        image = Image.open(r'assets\covid.jpg')
    else:
        image = Image.open(r'assets\covidblur.jpg')
    st.image(image)
with col3:
    if issue == "Healthcare":
        image = Image.open(r'assets\healthcare.jpg')
    else:
        image = Image.open(r'assets\healthcareblur.jpg')
    st.image(image)
with col4:
    if issue == "National Security":
        image = Image.open(r'assets\national-security.jpg')
    else:
        image = Image.open(r'assets\national-securityblur.jpg')
    st.image(image)
with col5:
    if issue == "Climate Change":
        image = Image.open(r'assets\climate-change.jpg')
    else:
        image = Image.open(r'assets\climate-changeblur.jpg')
    st.image(image)

#Radio selector for state/race
stateOptions = ['Arizona', 'Florida', 'Georgia', 'North Carolina', 'Ohio', 'Pennsylvania', 'Wisconsin']
state = st.selectbox("Please select a Senate race to investigate:", stateOptions)
st.markdown('You are comparing the issue of ' + str(issue).lower() + " between candidates in the " + str(state) + " Senate race.")


