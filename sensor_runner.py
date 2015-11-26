#!/usr/bin/env python
import os
import sqlite3
import datetime
from Adafruit_BME280 import *
import time


class SQL():
        def __init__(self,debug=1):
                if not os.path.isfile('base.sqlite'):
                        self.connection=sqlite3.connect('base.sqlite')
                        self.curs = self.connection.cursor()
                        tblcmd =[]
                        #tblcmd.append('CREATE TABLE tests (test_id char(20) NOT NULL, day char(20) NOT NULL,  PRIMARY KEY (test_id))')
                        tblcmd.append('CREATE TABLE stats ( sensor char(50) NOT NULL, sensor_data float(500) NOT NULL,  day char(20) NOT NULL, time char(20) NOT NULL)')
                        for cmd in tblcmd:
                                self.curs.execute(cmd)
        def connect(self):
                self.connection=sqlite3.connect('base.sqlite')
                self.curs = self.connection.cursor()

        def flush_table(self):
                self.connect()
                self.curs.execute('DELETE FROM stats ')
                #self.curs.execute('DELETE FROM tests ')
                self.connection.commit()
                self.connection.close()

        def add_data(self,temperature,pressure,humidity):
                day=str(datetime.datetime.today())[:10]
                time=datetime.datetime.now().time()
                time=str(time.replace(microsecond=0))

                self.raw_request('INSERT INTO stats VALUES ("temperature", "' +str(temperature) +'", "' + day + '", "' + time + '")')
                self.raw_request('INSERT INTO stats VALUES ("pressure", "' + str(pressure) +'", "' + day + '", "' + time + '")')
                self.raw_request('INSERT INTO stats VALUES ("humidity", "' + str(humidity) +'", "' + day + '", "' + time + '")')


        def raw_request(self,command):
                self.connect()
                data=[]
                try:
                        for row in self.curs.execute(command):
                                data.append(row)
                except:
                        data='None'
                self.connection.commit()
                self.connection.close()
                return data

sql=SQL()
sensor = BME280(mode=BME280_OSAMPLE_8)
print sql.raw_request('SELECT sensor_data FROM stats ')
while True:
	if datetime.datetime.now().minute==0 or datetime.datetime.now().minute==30: #check sensors every 30 minutes
		degrees = sensor.read_temperature()
		pascals = sensor.read_pressure()
		hectopascals = pascals / 100
		humidity = sensor.read_humidity()
		mmHg=(pascals/100)*0.7600616827
		sql.add_data(degrees,mmHg,humidity)
		time.sleep(30)

