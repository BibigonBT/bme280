#!/usr/bin/env python
import os
import sqlite3
import datetime
from Adafruit_BME280 import *
import requests
server_ip='10.0.0.2'
server_port='4164'

class SQL():
	def __init__(self,server_ip=server_ip, server_port=server_port):
		self.server_ip=server_ip
		self.server_port=server_port
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

	def add_data(self,location,sensor,sensor_value,sensor_time):
		self.raw_request('INSERT INTO stats VALUES ("'+location+'" , "'+sensor+'", "' + str(sensor_value) +'", "' + str(sensor_time) + '")')
		
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

			
	def main_loop(self):
		while True:
			if datetime.datetime.now().minute==00 or datetime.datetime.now().minute==30: #check sensors every 30 minutes
				degrees = sensor.read_temperature()
				pascals = sensor.read_pressure()
				hectopascals = pascals / 100
				humidity = sensor.read_humidity()
				mmHg=(pascals/100)*0.7600616827
				self.upload_old_data()
				self.send_to_server('Room','temperature',	degrees,	datetime.datetime.now())
				self.send_to_server('Room','pressure',		mmHg,		datetime.datetime.now())
				self.send_to_server('Room','humidity',		humidity,	datetime.datetime.now())
				time.sleep(1500)
			time.sleep(10)

	def upload_old_data(self):
		old_data=sql.raw_request('SELECT * FROM stats')
		for line in old_data:
			try:
				m=requests.get('http://'+self.server_ip+':'+self.server_port+'/?action=add&location='+line[0]+'&sensor='+line[1]+'&sensor_value='+str(line[2])+'&sensor_time='+str(line[3]))
			except:
				return 1
			else:
				self.raw_request('DELETE FROM stats WHERE sensor_location="'+line[0]+'" AND sensor_name="'+line[1]+'" AND sensor_data='+str(line[2])+' AND time="'+line[3]+'"')

	def send_to_server(self,location,sensor,sensor_value,sensor_time):
		try:
			m=requests.get('http://'+self.server_ip+':'+self.server_port+'/?action=add&location='+location+'&sensor='+sensor+'&sensor_value='+str(sensor_value)+'&sensor_time='+str(sensor_time))
		except:
			sql.add_data(location,sensor,sensor_value,sensor_time)
		


sql=SQL()
sensor = BME280(mode=BME280_OSAMPLE_8)
sql.main_loop()


