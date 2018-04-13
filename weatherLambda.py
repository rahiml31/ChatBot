try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import json
global intent
global smallImage
global largeImage

def lambda_handler(event, context):
    global intent
    global smallImage
    global largeImage
    
    if event["request"]["type"] =="LaunchRequest":
        output="Welcome to the Weather API."
        session_end_status=False
    elif event["request"]["type"] =="IntentRequest":
        if event["request"]["intent"]["name"] =="getQueryData":
            query=event["request"]["intent"]["slots"]["Query"]["value"]
            splitQuery=query.split()
            if (len(splitQuery)==2):
                city=splitQuery[0]
                state=splitQuery[1]
            elif (len(splitQuery)==3):
                city=str(splitQuery[0])+"%20"+str(splitQuery[1])
                state=splitQuery[2]
            else:
                city=str(splitQuery[0])+"%20"+str(splitQuery[1])
                state=str(splitQuery[2])+"%20"+str(splitQuery[3])
            baseurl="https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22"+str(city)+"%2C"+str(state)+"%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
            finalurl=Request(baseurl,headers={'User-Agent':'Mozilla/5.0'})
            
            queryResult=urlopen(finalurl)
            json_output=json.load(queryResult)
            cityy=json_output["query"]["results"]["channel"]["location"]["city"]
            statee=json_output["query"]["results"]["channel"]["location"]["region"]
            forecast=json_output["query"]["results"]["channel"]["item"]["forecast"][0]
            text=forecast["text"]
            
            textFormat=text.lower()
            smallImage=""
            largeImage=""
            if (textFormat=="mostly cloudy"):
                smallImage="https://www.wpclipart.com/weather/weather_icons/weather_icons_2/partly_cloudy.png"
                largeImage="https://cdn.pixabay.com/photo/2012/04/18/13/21/clouds-37009_960_720.png"
            else:
                smallImage="https://vignette.wikia.nocookie.net/fantendo/images/4/40/Tornado_Wind.png/revision/latest?cb=20151022165830"
                largeImage="https://banner.kisspng.com/20180130/joe/kisspng-tornado-storm-tornado-5a70bceb4be609.9880442315173378353109.jpg"
                        
            output="The weather today in "+str(cityy)+","+str(statee)+" is "+str(forecast)
            
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
                    "type": "Standard",
                    "title": "Weather Information",
                    "text": output,
                    "image": {
                        "smallImageUrl": smallImage,
                        "largeImageUrl": largeImage
                    }
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
