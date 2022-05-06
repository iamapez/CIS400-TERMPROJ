import twitterapi
import json
from Candidate import Candidate
from backend import twitterAPIcredents
from Constants import *

# authenticate one our api
apez_Authenticated = twitterapi.oauth_login(twitterAPIcredents.apez_consumerKey,
                                            twitterAPIcredents.apez_consumerSecret,
                                            twitterAPIcredents.apez_oauthtoken,
                                            twitterAPIcredents.apez_oauthsecret)  # authenticate apez api key and store it here

# call our custom function, pass in a key word
for Candidate in range(0,3):
response = twitterapi.getTweetsJSONByKeyword(apez_Authenticated,'Biden')
for tweetData in response:
    if any(ext in tweetData['text'] for ext in Constants.ECONOMY_KEYWORDS):
        print(tweetData['text'])
