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


def updateJSONData():
    # update the local program data
    response = parseCSV.getInfoandUpdateJSON()
    if response == 400:
        exit(1)
    else:
        print('ERROR!')
        print(response)


def main():
    # updateJSONData()
    apez_Authenticated = twitterapi.getAuthenticated()

    firstScreenName = 'edmundyu1001'
    testUser = twitterapi.get_user_profile(apez_Authenticated, firstScreenName)

    print(1)


if __name__ == "__main__":
    main()
