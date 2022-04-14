# Alexander C. Perez, acperez@syr.edu
# Backend class to convert election data from assets/ and convert it to python objects
# we serialize the python objects then store them in a json file in assets/

from Canidate import *
import csv
import os
import os.path
import shutil
import json


def getInfoandUpdateJSON():
    try:
        # move our working directory to access the csv very soon
        d = os.getcwd()
        os.chdir('..')
        d = os.getcwd()

        pathToCSV = 'assets/Candidate_Listing_2022.csv'  # path of CSV
        listOfCandidateObjects = []  # empty list that will temporarily store each object of canidate
        with open(pathToCSV) as f:
            csv_reader = csv.reader(f, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    # print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    # print(f'\t{row[0]} email, {row[1]} canodacydate, party contest {row[2]}.')
                    tmpCandidate = Candidate(row)
                    listOfCandidateObjects.append(tmpCandidate)
                    line_count += 1

        # output to json file
        d = os.getcwd()
        pathToWritingCSV = 'assets/CandidateDataCLEANED.json'
        with open(pathToWritingCSV, 'w') as outfile:
            for item in listOfCandidateObjects:
                outfile.write(item.toJSON())

        return 400

    except Exception as e:
        return e
