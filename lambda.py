try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import json
global intent

def lambda_handler(event, context):
    global intent
    
    if event["request"]["type"] =="LaunchRequest":
        output="Welcome to the Star Wars Planet API."
        session_end_status=False
    elif event["request"]["type"] =="IntentRequest":
        if event["request"]["intent"]["name"] =="getQueryData":
            query=event["request"]["intent"]["slots"]["Query"]["value"]
            baseurl="https://swapi.co/api/planets/"
            yqlurl=baseurl+str(query)
            finalurl=Request(yqlurl,headers={'User-Agent':'Mozilla/5.0'})
            queryResult=urlopen(finalurl).read()
            output=str(queryResult)
            intent="getQueryData"
            session_end_status=False
        else:
            output="I am exiting from intent "+event["request"]["intent"]["name"]
            session_end_status=True
    
    # TODO implement
    return  {
             "version": "1.0",
             "response": {
             "outputSpeech": {
                "type": "PlainText",
                "text": output
                },
                "card": {
                "content": output,
                    "title": "planet information",
                    "type": "Simple"
                },
                "reprompt": {
                "outputSpeech": {
                "type": "PlainText",
                "text": ""
                 }
            },
            "shouldEndSession": session_end_status
            },
            "sessionAttributes": {}
        }
