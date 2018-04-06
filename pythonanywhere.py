#!/usr/bin/env python2.7

# A very simple Flask Hello World app for you to get started with...
#import urllib
from __future__ import print_function
#from future.standard_library import install_aliases
#install_aliases()
from future import standard_library
standard_library.install_aliases()
import os
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from twilio.rest import TwilioRestClient
#from urllib.parse import urlparse, urlencode
from urllib.request import urlopen
#from urllib.error import HTTPError

import json
from random import randint

from flask import Flask
from flask import request
from flask import make_response
user_otp={}
user_otp_ssid={}

user_list={"ABwppHFHtuY6Ska40VRQ08H8a5loeBXr8RcDCQhKz4mTNwaLHbkDVk9tlMCg89MTqc6q-zjDJqtSSvaCCQ":"peter","ABwppHGMjTDJbeei2LYHHKQG-gmVR1ZhmMHr9kZCtj9roehFYcm6niUb0nFspMJdJgKbUiYPK7T6mKfuYIwA":"manu"}
session_auth_list={}
app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')

def hello_world():
    return 'Welcome to webhook-testagent'

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") == "input.unknown":
        return chat_bot_request(req)
    else:
        return {}

def chat_bot_request(req):
    variable = req.get("result").get("resolvedQuery")
    print(variable)
    queryOutput = chat_bot(variable)
    speech = queryOutput

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "ChatBotRequest_App_Chatbox"
    }

def chat_bot(query):
    baseurl = "https://swapi.co/api/planets/"
    yql_url = baseurl + str(query)
    result = urlopen(yql_url).read()
    

    return str(result)

