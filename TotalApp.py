import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import json

def getWeather(la, lo):
    lat = str(la)
    lon = str(lo)

    app_key = '0b0daf2f59f49d1b7d050208c7abb95f'
    api_url_weather = (
    'https://samples.openweathermap.org/data/2.5/weather?lat=35' + lat + '&lon=' + lon + '&appid=' + app_key)
    api_url_weather1 = (
    'https://samples.openweathermap.org/data/2.5/weather?q=London,uk&appid=0b0daf2f59f49d1b7d050208c7abb95f')

    response = requests.get(api_url_weather)

    raining = json.loads(response.text)  # set string to dictionary

    print(raining['weather'][0]['main'])
    return (raining['weather'][0]['main'])


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello World!')

    def do_POST(self):
        print(self.headers['Content-Length'])
        content_length = 0
        if (self.headers['Content-Length'] is not None):
            content_length = int(self.headers['Content-Length'])
        #body = self.rfile.read(self.headers.get('Content-Length'))
        body = self.rfile.read(content_length)
        print (body)
        dictPartText = body.decode()
        print(type(dictPartText))
        dictPart = json.loads(dictPartText)
        print(dictPart)
        metadata = dictPart["metadata"]
        print(metadata)
        lat = metadata["latitude"]
        lon = metadata["longitude"]
        print(lat, lon)
        result = getWeather(lat, lon)
        result = "{'raintype': '" + str(result) + "'}'"
        result = str.encode(result)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        response.write(b'   weather: ')
        response.write(result)
        self.wfile.write(response.getvalue())


httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()
