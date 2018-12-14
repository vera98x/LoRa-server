
# A very simple Flask Hello World app for you to get started with...

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
        print(dictPart)
        metadata = dictPart["gateways"][0]
        print(metadata)
        lat = metadata["latitude"]
        lon = metadata["longitude"]
        print(json.dumps(request.get_json()))

        result = str(getWeather(lat, lon))
        result = "{'raintype': '" + str(result) + "'}'"
        result = str.encode(result)


    except:
        result = "{'raintype': 'Error'}'"
        result = str.encode(result)

    return (result)
@app.route('/', methods=['GET'])
def index1():
    '''Just a test for connecting, returns hello world'''
    if(request.method == 'GET'):
        return 'Hello VeraGET'

if __name__ == '__main__':
    #run webserver
    app.run(debug=True, use_reloader=False)