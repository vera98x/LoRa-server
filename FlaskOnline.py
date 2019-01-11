from flask import Flask
from flask import request
import json
import requests

app = Flask(__name__)


def getWeather(la, lo):
    lat = str(la)
    lon = str(lo)

    app_key = '0b0daf2f59f49d1b7d050208c7abb95f'
    api_url_weather = (
    'https://api.openweathermap.org/data/2.5/weather?lat=' + lat + '&lon=' + lon + '&appid=' + app_key)

    response = requests.get(api_url_weather)

    raining = json.loads(response.text)  # set string to dictionary

    print(raining['weather'][0]['main'])
    return (raining['weather'][0]['main'])


@app.route('/', methods=['POST'])
def index():
    '''Receive post information and get weather'''
    try:
        dictPartText = request.get_data()
        dictPart = json.loads(dictPartText)
    except:
        result = "{'Error': 'Can't parse data'}'"
        result = str.encode(result)
        return (result)
    try:
        print(dictPart)
        metadata = dictPart["metadata"]
        print(metadata)
        metadata = metadata["gateways"][0]
    except:
        result = "{'Error': 'Can't find gateway-data'}'"
        result = str.encode(result)
        return (result)

    try:
        lat = metadata["latitude"]
        lon = metadata["longitude"]
    except:
        result = "{'Error': 'Can't find lon-lat data'}'"
        result = str.encode(result)
        return (result)

    try:
        result = str(getWeather(lat, lon))
        result = "{'raintype': '" + str(result) + "'}'"
        result = str.encode(result)
    except:
        result = "{'Error': 'Can't acces the WeatherAPI'}'"
        result = str.encode(result)
        return (result)

    try:
        downlink = dictPart["downlink_url"]
        dev_id = dictPart['dev_id']
        print("post data:", downlink, dev_id)
        result_weather = "{'raintype': '" + str(result) + "'}'"
        data1 = {"dev_id":dev_id,"payload_raw":"AQE="}
        print(result)
        print("Lets post:")
        r = requests.post(downlink, json=data1)
        print("postdone")
        print(r.status_code)
        print(r.content)
        print("postdone complete")
    except:
        result = "{'Error': 'Error, cant post result'}'"
        result = str.encode(result)
        return (result)

    return (result)

@app.route('/', methods=['GET'])
def index1():
    '''Just a test for connecting, returns hello world'''
    if(request.method == 'GET'):
        return 'Hello UserGET'
