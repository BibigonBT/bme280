import sqlite3
import os

class SQL():
    def __init__(self,debug=1):
        self.debug=debug
        if not os.path.isfile('sensor_data.sqlite'):
            self.connection=sqlite3.connect('sensor_data.sqlite')
            self.curs = self.connection.cursor()
            cmd=('CREATE TABLE stats ( "sensor_location" char(50) NOT NULL, "sensor_name" char(50) NOT NULL, "sensor_data" float(30) NOT NULL,  "time" DATETIME NOT NULL)')
            self.curs.execute(cmd)
            self.connection.commit()
            self.connection.close()

    def connect(self):
        self.connection=sqlite3.connect('sensor_data.sqlite')
        self.curs = self.connection.cursor()

    def flush_table(self):
        self.connect()
        self.curs.execute('DELETE FROM stats ')
        self.connection.commit()
        self.connection.close()

    def add_record(self,location,sensor,sensor_value,sensor_time):
        self.connect()
        self.curs.execute('INSERT INTO stats VALUES ("'+location+'" , "'+sensor+'", "' + str(sensor_value) +'", "' + sensor_time + '")')
        self.connection.commit()
        self.connection.close()

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



