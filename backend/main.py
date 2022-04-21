# Alexander C. Perez, acperez@syr.edu
# this will serve as the main python file for the twitter api

from bs4 import BeautifulSoup
import pandas as pd
import requests
import wikitextparser as wtp
import json
import urllib.request
import os
import pathlib
import sys
import parseCSV
import twitterapi
import json
from Canidate import setFromRow
from googlesearch import search


def updateJSONData():
    """
    Method to write to JSON file based on csv pulled from internet
    :return: true if successful, false if failure
    """

    response = parseCSV.getInfoandUpdateJSON()
    if len(response) == 0:
        return response
    else:
        print('ERROR!')
        print(response)
        exit(-1)


def getUserObjectsFromJSON():
    """
    If the JSON file already exists, return a list of python objects to our main program to work with
    :return: listOfObjects
    """

    pathToDataJSON = 'assets/CLEANconvertcsv.json'
    d = os.getcwd()  # change directories to access the json file containing the data
    os.chdir("..")

    listOfObjects = list()

    # Opening JSON file
    f = open('assets/CLEANconvertcsv.json')
    data = json.load(f)
    for i in data:
        # print(i)
        tempCanidate = setFromRow(dateOfElection=i['election_dt'], county=i['county_name'],
                                  contestName=i['contest_name'],
                                  nameOnBallot=i['name_on_ballot'], firstName=i['first_name'], lastName=i['last_name'],
                                  nickName=i['nick_name'], streetAddress=i['street_address'], city=i['city'],
                                  state=i['state'],
                                  zipCode=i['zip_code'], businessPhone=i['business_phone'], email=i['email'],
                                  candidacyDT=i['candidacy_dt'],
                                  partyContest=i['party_contest'], partyCandidate=i['party_candidate'],
                                  isUnexpired=i['is_unexpired'],
                                  hasPrimary=i['has_primary'], isPartisan=i['is_partisan'], voteFor=i['vote_for'],
                                  term=i['term'])
        listOfObjects.append(tempCanidate)

    # Closing file
    f.close()

    return listOfObjects


def findTwitterUsername(nameOnBallot, state):
    query = '{} {} twitter'.format(nameOnBallot, state)
    for i in search(query, num_results=5):
        if 'twitter.com' in i:
            return i


def main():
    """
    Entry point for our backend code.
    :return: exit code status
    """

    # electionObjects = updateJSONData()            # only run this is we want to re initalize our data from the csv data file

    apez_Authenticated = twitterapi.getAuthenticated()  # authenticate apez api key and store it here
    userObjects = getUserObjectsFromJSON()  # get a list of user objects that we can do work with internally

    for i in userObjects:
        print(findTwitterUsername(i.nameOnBallot, i.state))

    # populate the twitterusername attribute for each python object so we can use the api later

    exit(1)


if __name__ == "__main__":
    main()
