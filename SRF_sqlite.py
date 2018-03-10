#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' sqlite data base interface '

__author__ = 'Lanbu'

import sqlite3

class FinancialDataRecord():
	#init
	def __init__(self):
		#record table contents
		self.usr_name = None
		self.record_date = None
		self.record_num = None
		self.record_income = None
		self.record_income_s = None
		self.record_expense = None
		self.record_expense_s = None
		self.record_remark = None
		#create a connection\
		self.conn = sqlite3.connect('SRF_RecordsDB.db')
		pass
		
	#create main table
	def create_record_table(self):
		self.cursor = self.conn.cursor()
		self.cursor.execute('''CREATE TABLE UserFinanRecords (usr_name TEXT, date TEXT, recordNum TEXT, income REAL, income_s TEXT, expense REAL, expense_s TEXT, remark TEXT)''')
				
	#insert one record
	def insert_one_record(self):
		self.cursor.execute("INSERT INTO UserFinanRecords VALUES ('%s','%s','%s',%f, '%s', %f, '%s' '%s')" 
							%(self.usr_name, self.record_date, self.record_num, self.record_income, self.record_income_s, self.record_expense, self.record_expense_s))
		
		
	#delete one record
	def delete_one_record(self):
		pass
		
	def close_sqlite(self):
		pass
		
