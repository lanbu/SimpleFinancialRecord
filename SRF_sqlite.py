#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' sqlite data base interface '

__author__ = 'Lanbu'

import sqlite3

class FinancialDataRecord():
	#init
	def __init__(self):
		#create a connection
		#self.conn = sqlite3.connect('SRF_RecordsDB.db')
		pass
		
	#create main table
	def create_record_table(self):
		#self.cursor = self.conn.cursor()
		#self.cursor.execute('create table UserFinanRecords (usr_name varchar(20) primary key, file_path varchar(100))')
		pass
		
	#insert one record
	def insert_one_record(self):
		pass
		
	#delete one record
	def delete_one_record(self):
		pass
		
	def close_sqlite(self):
		pass