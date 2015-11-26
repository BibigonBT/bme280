#!/usr/bin/env python
from Adafruit_BME280 import *
import time
from bokeh.plotting import figure
from bokeh.io import vplot
from bokeh.embed import components
from data import SQL
sensor = BME280(mode=BME280_OSAMPLE_8)
sql=SQL()

#xaxis = DatetimeAxis(formatter=DatetimeTickFormatter(formats={"months": ["%B %Y"], "days": ["%B %Y"]}),**AXIS_FORMATS)


 # create a new plot
p1 = figure(
toolbar_location=None,
tools="crosshair",
y_axis_label='Temperature C',
plot_width=1000,
plot_height=240)

p2 = figure(toolbar_location=None,
tools="crosshair",
y_axis_label='Humidity %',
plot_width=1000,
plot_height=240)
   
p3 = figure(toolbar_location=None,
tools="crosshair",
#y_range=[0,100],
x_axis_label='Time (Hours)',
y_axis_label='Pressure mmHg',
plot_width=1000,
plot_height=240)

degrees = sensor.read_temperature()
pascals = sensor.read_pressure()
hectopascals = pascals / 100
humidity = sensor.read_humidity()
mmHg=(pascals/100)*0.7600616827


y1=[]
temp=sql.raw_request('SELECT sensor_data FROM stats WHERE sensor="temperature"')
for h in temp:
	y1.append(h[0])
x1=[x for x in range(0,len(y1))]

p1.line(x1, y1, color='red',line_width=4)
p1.circle(x1, y1,  fill_color="white", size=8, color='red')
p1.yaxis.axis_label_text_color="#FF0000"

y2=[]
temp=sql.raw_request('SELECT sensor_data FROM stats WHERE sensor="humidity"')
for h in temp:
	y2.append(h[0])
x2=[x for x in range(0,len(y2))]

p2.line(x2, y2, color='blue',line_width=4)
p2.circle(x2, y2, fill_color="white", size=8)
p2.yaxis.axis_label_text_color="#0000FF"

y3=[]
temp=sql.raw_request('SELECT sensor_data FROM stats WHERE sensor="pressure"')
for h in temp:
	y3.append(h[0])
x3=[x for x in range(0,len(y2))]

p3.line(x3, y3, color='green',line_width=4)
p3.circle(x3, y3,  fill_color="white", size=8)
p3.yaxis.axis_label_text_color="#00FF00"
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


