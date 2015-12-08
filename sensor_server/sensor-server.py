import http.server
from urllib.parse import urlparse
from sensor_sql import SQL
import datetime
from bokeh.plotting import figure
from bokeh.io import vplot
from bokeh.embed import components

PORT_NUMBER=4164
HOST_NAME=''
hours={'00':0,'01':1,'02':2,'03':3,'04':4,'05':5,'06':6,'07':7,'08':8,'09':9,
        '10':10,'11':11,'12':12,'13':13,'14':14,'15':15,'16':16,'17':17,'18':18,'19':19,
        '20':20,'21':21,'22':22,'23':23}

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
        today=str(datetime.datetime.today())[:10]
        yesterday=str(datetime.datetime.today()-datetime.timedelta(minutes=1440))[:10]

        p1 = figure(toolbar_location=None,tools="crosshair",y_axis_label='Temperature C',plot_width=1000,plot_height=240)
        p2 = figure(toolbar_location=None,tools="crosshair",y_axis_label='Humidity %',plot_width=1000,plot_height=240)
        p3 = figure(toolbar_location=None,tools="crosshair",x_axis_label='Time (Hours)',y_axis_label='Pressure mmHg',plot_width=1000,plot_height=240)
        #degrees = sensor.read_temperature()
        #humidity = sensor.read_humidity()
        #mmHg=((sensor.read_pressure()/100)*0.7600616827)-6.2

        #----------------------------------------------Temperature-------------------------------------------------------
        y_today=[];y_yesterday=[];x_today=[];x_yesterday=[]
        today_data=sql.raw_request('SELECT sensor_data , time FROM stats WHERE sensor_name="temperature" AND time LIKE "'+today+'%"')
        for h in today_data:
            y_today.append(h[0])
            if int(h[1][14:16])<30:
                x_today.append(hours[str(h[1][11:13])])
            else:
                x_today.append(hours[str(h[1][11:13])]+0.5)
        yesterday_data=sql.raw_request('SELECT sensor_data , time FROM stats WHERE sensor_name="temperature" AND time LIKE "'+yesterday+'%"')
        for h in yesterday_data:
            y_yesterday.append(h[0])
            if int(h[1][14:16])<30:
                x_yesterday.append(hours[str(h[1][11:13])])
            else:
                x_yesterday.append(hours[str(h[1][11:13])]+0.5)
        p1.line(x_yesterday, y_yesterday, color='grey',line_width=1)
        p1.circle(x_yesterday, y_yesterday,  fill_color="white", size=4, color='grey')
        p1.line(x_today, y_today, color='red',line_width=4)
        p1.circle(x_today, y_today,  fill_color="white", size=8, color='red')
        p1.xaxis[0].ticker.desired_num_ticks=12
        p1.yaxis.axis_label_text_color="#FF0000"
        #----------------------------------------------Humidity------------------------------------------------
        x_today=[];x_yesterday=[];y_today=[];y_yesterday=[]
        temp=sql.raw_request('SELECT sensor_data, time FROM stats WHERE sensor_name="humidity" AND time LIKE "'+today+'%"')
        for h in temp:
            y_today.append(h[0])
            if int(h[1][14:16])<30:
                x_today.append(hours[str(h[1][11:13])])
            else:
                x_today.append(hours[str(h[1][11:13])]+0.5)
        temp=sql.raw_request('SELECT sensor_data, time FROM stats WHERE sensor_name="humidity" AND time LIKE "'+yesterday+'%"')
        for h in temp:
            y_yesterday.append(h[0])
            if int(h[1][14:16])<30:
                x_yesterday.append(hours[str(h[1][11:13])])
            else:
                x_yesterday.append(hours[str(h[1][11:13])]+0.5)
        p2.line(x_yesterday, y_yesterday, color='gray',line_width=1)
        p2.circle(x_yesterday, y_yesterday, fill_color="white", size=4, color="gray")
        p2.line(x_today, y_today, color='blue',line_width=4)
        p2.circle(x_today, y_today, fill_color="white", size=8, color="blue")
        p2.xaxis[0].ticker.desired_num_ticks=12
        p2.yaxis.axis_label_text_color="#0000FF"
        #-------------------------------------------Pressure-------------------------------------------------
        x_today=[];x_yesterday=[];y_today=[];y_yesterday=[]
        temp=sql.raw_request('SELECT sensor_data, time FROM stats WHERE sensor_name="pressure" AND time LIKE "'+today+'%"')
        for h in temp:
            y_today.append(h[0]-6.2)
            if int(h[1][14:16])<30:
                x_today.append(hours[str(h[1][11:13])])
            else:
                x_today.append(hours[str(h[1][11:13])]+0.5)
        temp=sql.raw_request('SELECT sensor_data, time FROM stats WHERE sensor_name="pressure" AND time LIKE "'+yesterday+'%"')
        for h in temp:
            y_yesterday.append(h[0]-6.2)
            if int(h[1][14:16])<30:
                x_yesterday.append(hours[str(h[1][11:13])])
            else:
                x_yesterday.append(hours[str(h[1][11:13])]+0.5)
        p3.line(x_yesterday, y_yesterday, color='grey',line_width=1)
        p3.circle(x_yesterday, y_yesterday,  fill_color="white", size=4, color="grey")
        p3.line(x_today, y_today, color='green',line_width=4)
        p3.circle(x_today, y_today,  fill_color="white", size=8, color="green")
        p3.xaxis[0].ticker.desired_num_ticks=12
        p3.yaxis.axis_label_text_color="#00FF00"
        #-----------------------------------------------------------------------------------------------------------
        m=vplot(p1,p2,p3)
        script, div = components(m)

        self.render('bokeh should be here...', script,div)


    def render(self, body='',script='',div=''):
        self.send_response(200);self.send_header("Content-type", "text/html");self.end_headers()
        self.wfile.write(b'<html>')
        self.wfile.write(b'<head>')
        self.wfile.write(b'<link rel="stylesheet" href="http://cdn.pydata.org/bokeh/release/bokeh-0.9.0.min.css" type="text/css" />')
        self.wfile.write(b'<script type="text/javascript" src="http://cdn.pydata.org/bokeh/release/bokeh-0.9.0.min.js"></script>')
        self.wfile.write(bytes(script,'utf-8'))
        self.wfile.write(b'</head>')
        self.wfile.write(b'<body>')
        self.wfile.write(bytes(body,'utf-8'))
        self.wfile.write(bytes(div,'utf-8'))
        self.wfile.write(b'</body></html>')

if __name__ == '__main__':
        server_class = http.server.HTTPServer
        httpd = server_class(('0.0.0.0', PORT_NUMBER), MyHandler)
        httpd.serve_forever()
        httpd.server_close()
