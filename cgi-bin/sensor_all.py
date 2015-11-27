#!/usr/bin/env python
from Adafruit_BME280 import *
import datetime
from bokeh.plotting import figure
from bokeh.io import vplot
from bokeh.embed import components
sensor = BME280(mode=BME280_OSAMPLE_8)
from data import SQL
sql=SQL()



p1 = figure(toolbar_location=None,tools="crosshair",y_axis_label='Temperature C',plot_width=1000,plot_height=240)
p2 = figure(toolbar_location=None,tools="crosshair",y_axis_label='Humidity %',plot_width=1000,plot_height=240)
p3 = figure(toolbar_location=None,tools="crosshair",x_axis_label='Time (Hours)',y_axis_label='Pressure mmHg',plot_width=1000,plot_height=240)

degrees = sensor.read_temperature()
humidity = sensor.read_humidity()
mmHg=(sensor.read_pressure()/100)*0.7600616827

#----------------------------------------------Temperature-------------------------------------------------------
temp_today=[]

temp=sql.raw_request('SELECT sensor_data FROM stats WHERE sensor_name="temperature"')
for h in temp:
	temp_today.append(h[0])
x=[z for z in range(0,len(temp))]
p1.line(x, temp_today, color='red',line_width=4)
p1.circle(x, temp_today,  fill_color="white", size=8, color='red')
p1.yaxis.axis_label_text_color="#FF0000"
#----------------------------------------------Humidity------------------------------------------------
humidity_today=[]

temp=sql.raw_request('SELECT sensor_data FROM stats WHERE sensor_name="humidity"')
for h in temp:
	humidity_today.append(h[0])

p2.line(x, humidity_today, color='blue',line_width=4)
p2.circle(x, humidity_today, fill_color="white", size=8, color="blue")

p2.yaxis.axis_label_text_color="#0000FF"
#-------------------------------------------Pressure-------------------------------------------------
pressure_today=[]

temp=sql.raw_request('SELECT sensor_data FROM stats WHERE sensor_name="pressure"')
for h in temp:
	pressure_today.append(h[0])

p3.line(x, pressure_today, color='green',line_width=4)
p3.circle(x, pressure_today,  fill_color="white", size=8, color="green")

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


