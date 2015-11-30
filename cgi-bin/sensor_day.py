#!/usr/bin/env python
from Adafruit_BME280 import *
import datetime
from bokeh.plotting import figure
from bokeh.io import vplot
from bokeh.embed import components
sensor = BME280(mode=BME280_OSAMPLE_8)
from data import SQL
sql=SQL()

today=str(datetime.datetime.today())[:10]
yesterday=str(datetime.datetime.today()-datetime.timedelta(minutes=1440))[:10]
hours={'00':0,'01':1,'02':2,'03':3,'04':4,'05':5,'06':6,'07':7,'08':8,'09':9,
'10':10,'11':11,'12':12,'13':13,'14':14,'15':15,'16':16,'17':17,'18':18,'19':19,
'20':20,'21':21,'22':22,'23':23}

p1 = figure(toolbar_location=None,tools="crosshair",y_axis_label='Temperature C',plot_width=1000,plot_height=240)
p2 = figure(toolbar_location=None,tools="crosshair",y_axis_label='Humidity %',plot_width=1000,plot_height=240)
p3 = figure(toolbar_location=None,tools="crosshair",x_axis_label='Time (Hours)',y_axis_label='Pressure mmHg',plot_width=1000,plot_height=240)

degrees = sensor.read_temperature()
humidity = sensor.read_humidity()
mmHg=((sensor.read_pressure()/100)*0.7600616827)-6.2

#----------------------------------------------Temperature-------------------------------------------------------
y_temp_today=[];y_temp_yesterday=[];x_temp_today=[];x_temp_yesterday=[]

temp=sql.raw_request('SELECT sensor_data , time FROM stats WHERE sensor_name="temperature" AND time LIKE "'+today+'%"')
for h in temp:
	y_temp_today.append(h[0])
	if int(h[1][14:16])<30:
		x_temp_today.append(hours[str(h[1][11:13])])
	else:
		x_temp_today.append(hours[str(h[1][11:13])]+0.5)
		
	
temp=sql.raw_request('SELECT sensor_data , time FROM stats WHERE sensor_name="temperature" AND time LIKE "'+yesterday+'%"')
for h in temp:
	y_temp_yesterday.append(h[0])
	if int(h[1][14:16])<30:
		x_temp_yesterday.append(hours[str(h[1][11:13])])
	else:
		x_temp_yesterday.append(hours[str(h[1][11:13])]+0.5)


p1.line(x_temp_yesterday, y_temp_yesterday, color='grey',line_width=1)
p1.circle(x_temp_yesterday, y_temp_yesterday,  fill_color="white", size=4, color='grey')
p1.line(x_temp_today, y_temp_today, color='red',line_width=4)
p1.circle(x_temp_today, y_temp_today,  fill_color="white", size=8, color='red')
p1.xaxis[0].ticker.desired_num_ticks=12
p1.yaxis.axis_label_text_color="#FF0000"
#----------------------------------------------Humidity------------------------------------------------
x_humidity_today=[];x_humidity_yesterday=[];y_humidity_today=[];y_humidity_yesterday=[]
temp=sql.raw_request('SELECT sensor_data, time FROM stats WHERE sensor_name="humidity" AND time LIKE "'+today+'%"')
for h in temp:
	y_humidity_today.append(h[0])
	if int(h[1][14:16])<30:
		x_humidity_today.append(hours[str(h[1][11:13])])
	else:
		x_humidity_today.append(hours[str(h[1][11:13])]+0.5)
temp=sql.raw_request('SELECT sensor_data, time FROM stats WHERE sensor_name="humidity" AND time LIKE "'+yesterday+'%"')
for h in temp:
	y_humidity_yesterday.append(h[0])
	if int(h[1][14:16])<30:
		x_humidity_yesterday.append(hours[str(h[1][11:13])])
	else:
		x_humidity_yesterday.append(hours[str(h[1][11:13])]+0.5)
p2.line(x_humidity_yesterday, y_humidity_yesterday, color='gray',line_width=1)
p2.circle(x_humidity_yesterday, y_humidity_yesterday, fill_color="white", size=4, color="gray")
p2.line(x_humidity_today, y_humidity_today, color='blue',line_width=4)
p2.circle(x_humidity_today, y_humidity_today, fill_color="white", size=8, color="blue")
p2.xaxis[0].ticker.desired_num_ticks=12
p2.yaxis.axis_label_text_color="#0000FF"
#-------------------------------------------Pressure-------------------------------------------------
x_pressure_today=[];x_pressure_yesterday=[];y_pressure_today=[];y_pressure_yesterday=[]
temp=sql.raw_request('SELECT sensor_data, time FROM stats WHERE sensor_name="pressure" AND time LIKE "'+today+'%"')
for h in temp:
	y_pressure_today.append(h[0]-6.2)
	if int(h[1][14:16])<30:
		x_pressure_today.append(hours[str(h[1][11:13])])
	else:
		x_pressure_today.append(hours[str(h[1][11:13])]+0.5)
temp=sql.raw_request('SELECT sensor_data, time FROM stats WHERE sensor_name="pressure" AND time LIKE "'+yesterday+'%"')
for h in temp:
	y_pressure_yesterday.append(h[0]-6.2)
	if int(h[1][14:16])<30:
		x_pressure_yesterday.append(hours[str(h[1][11:13])])
	else:
		x_pressure_yesterday.append(hours[str(h[1][11:13])]+0.5)
p3.line(x_pressure_yesterday, y_pressure_yesterday, color='grey',line_width=1)
p3.circle(x_pressure_yesterday, y_pressure_yesterday,  fill_color="white", size=4, color="grey")
p3.line(x_pressure_today, y_pressure_today, color='green',line_width=4)
p3.circle(x_pressure_today, y_pressure_today,  fill_color="white", size=8, color="green")
p3.xaxis[0].ticker.desired_num_ticks=12
p3.yaxis.axis_label_text_color="#00FF00"
#-----------------------------------------------------------------------------------------------------------
m=vplot(p1,p2,p3)
script, div = components(m)

top='''Content-type: text/html\n
	<html>
	<head>
	<title>BME280 - data</title>
	<link rel="stylesheet" href="http://cdn.pydata.org/bokeh/release/bokeh-0.9.0.min.css" type="text/css" />
	<script type="text/javascript" src="http://cdn.pydata.org/bokeh/release/bokeh-0.9.0.min.js"></script>	
	'''
print top
print script
print '</head>'
print '<body>'
print '<table width="100%">'
print '<tr>'
print '<th rowspan="3" style="width: 1000px;">'
print div
print '</th>'
print '<th height="270">'
print '<center><h1>Temperature<br>'
print '<font color="#FF0000">'
print '{0:0.2f}'.format(degrees)+ ' C'
print '</font></h1></center>'
print '</th>'
print '</tr>'
print '<tr>'
print '<td>'
print '<center><h1>Humidity<br><font color="#0000FF">'
print '{0:0.2f}'.format(humidity)+' %'
print '</font></h1></center>'
print '</td>'
print '</tr>'
print '<tr>'
print '<td height="270">'
print '<center><h1>Pressure<br><font color="#418746">'
print str(mmHg)[0:6]
print '</font></h1></center></td>'
print '</tr>'
print '</table>'
print '</body></html>'


