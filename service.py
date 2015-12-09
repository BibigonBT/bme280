#!/usr/bin/env python
import os
import sqlite3
import datetime


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


			
	
if __name__=='__main__':
        sql=SQL()
        sensor = BME280(mode=BME280_OSAMPLE_8)



