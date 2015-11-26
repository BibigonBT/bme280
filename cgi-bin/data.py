#!/usr/bin/env python
import sqlite3



class SQL():
        
        def connect(self):
                self.connection=sqlite3.connect('base.sqlite')
                self.curs = self.connection.cursor()


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


