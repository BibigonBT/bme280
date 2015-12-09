import http.server
from urllib.parse import urlparse
from service import SQL
from Adafruit_BME280 import *
import json

PORT_NUMBER=4164
HOST_NAME=''
sql=SQL()
sensor = BME280(mode=BME280_OSAMPLE_8)

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        query = urlparse(self.path).query
        if query:
            query_components = dict(qc.split("=") for qc in query.split("&"))
            if 'action' in query_components.keys() and query_components['action']:
                if query_components['action']=='get':
                    self.render(json.dump(self.get_sensor_data()))  #get_sensor_data

                self.render('Unknown action<br>')
            else:
                self.render('Unknown request<br>')
        else:
            self.render('Clean index page<br>')

    def get_sensor_data(self):
        sensor_data={}
        sensor_data['degrees'] = sensor.read_temperature()
        pascals = sensor.read_pressure()
        sensor_data['hectopascals'] = pascals / 100
        sensor_data['humidity'] = sensor.read_humidity()
        sensor_data['mmHg'] =(pascals/100)*0.7600616827
        return sensor_data


    def render(self, body=''):
        self.send_response(200);self.send_header("Content-type", "text/html");self.end_headers()
        self.wfile.write(b'<html>')
        self.wfile.write(b'<head>')
        self.wfile.write(b'</head>')
        self.wfile.write(b'<body>')
        self.wfile.write(body)
        self.wfile.write(b'</body></html>')

if __name__ == '__main__':
        server_class = http.server.HTTPServer
        httpd = server_class(('0.0.0.0', PORT_NUMBER), MyHandler)
        httpd.serve_forever()
        httpd.server_close()
