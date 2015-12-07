import http.server
from urllib.parse import urlparse
from sensor_sql import SQL

PORT_NUMBER=4164
server_name=PORT_NUMBER
HOST_NAME=''
sql=SQL()

class MyHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        query = urlparse(self.path).query
        if query:
            query_components = dict(qc.split("=") for qc in query.split("&"))
            if 'action' in query_components.keys() and query_components['action']:
                if query_components['action']=='add':
                    self.add(query_components)   #add_sensor_data
            else:
                self.render('unknown action<br>')       #no action
        else:
            self.bokeh_viz()        #show index page

    def add(self,data):
        s=''
        for key in data:
            s=s+'<br>'+key+'='+data[key]
        self.render(s)
        sql.add_record(data['location'],data['sensor'],data['sensor_value'],data['sensor_time'].replace('%20',' '))

    def bokeh_viz(self):
        self.render('bokeh should be here...')


    def render(self, body):
        self.send_response(200);self.send_header("Content-type", "text/html");self.end_headers()
        self.wfile.write(b'<html><body>')
        self.wfile.write(bytes(body,'utf-8'))
        self.wfile.write(b'</body></html>')

if __name__ == '__main__':
        server_class = http.server.HTTPServer
        httpd = server_class(('0.0.0.0', PORT_NUMBER), MyHandler)
        httpd.serve_forever()
        httpd.server_close()
