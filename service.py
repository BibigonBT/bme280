#!/usr/bin/env python
import os
import sqlite3
import datetime
from Adafruit_BME280 import *
import random

class SQL():
        def __init__(self,debug=1):
                if not os.path.isfile('base.sqlite'):
                        self.connection=sqlite3.connect('base.sqlite')
                        self.curs = self.connection.cursor()
                        tblcmd =[]
                        tblcmd.append('CREATE TABLE stats ( "sensor_location" char(50) NOT NULL, "sensor_name" char(50) NOT NULL, "sensor_data" float(30) NOT NULL,  "time" DATETIME NOT NULL)')
                        for cmd in tblcmd:
                                self.curs.execute(cmd)
        def connect(self):
                self.connection=sqlite3.connect('base.sqlite')
                self.curs = self.connection.cursor()

        def flush_table(self):
                self.connect()
                self.curs.execute('DELETE FROM stats ')
                self.connection.commit()
                self.connection.close()

        def add_data(self,temperature,pressure,humidity):
                time=str(datetime.datetime.today())
                self.raw_request('INSERT INTO stats VALUES ("Room" , "temperature", "' + str(temperature) +'", "' + time + '")')
                self.raw_request('INSERT INTO stats VALUES ("Room" , "pressure", "'    + str(pressure)    +'", "' + time + '")')
                self.raw_request('INSERT INTO stats VALUES ("Room" , "humidity", "'    + str(humidity)    +'", "' + time + '")')


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

	def fake_data(self):
		dates_delta=4320 # 3 days
		finish=datetime.datetime.today()
		start=finish-datetime.timedelta(minutes=dates_delta)
		delta=0
		for i in range(0,144):
			
			time=start+datetime.timedelta(minutes=delta)
			self.raw_request('INSERT INTO stats VALUES ("Room" , "temperature", "' + str(random.randrange(0,35)) +'", "' + str(time) + '")')
                	self.raw_request('INSERT INTO stats VALUES ("Room" , "pressure", "'    + str(random.randrange(750,770))    +'", "' + str(time) + '")')
                	self.raw_request('INSERT INTO stats VALUES ("Room" , "humidity", "'    + str(random.randrange(30,80))    +'", "' + str(time) + '")')
			delta=delta+30
			
	

sql=SQL()
sensor = BME280(mode=BME280_OSAMPLE_8)

#sql.fake_data()

print sql.raw_request('Select time FROM stats WHERE  time LIKE "2015-11-26 10%"')
sql.raw_request('DELETE FROM stats WHERE  time LIKE "2015-11-26 22%"')
#sql.main_loop()


