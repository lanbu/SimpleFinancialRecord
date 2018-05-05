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
		#create a connection
		self.conn = sqlite3.connect('SRF_RecordsDB.db', check_same_thread = False)
		self.cursor = self.conn.cursor()
		self.sql_create_record_table()
		
	#create main table if not exists
	def sql_create_record_table(self):	
		self.cursor.execute('''CREATE TABLE IF NOT EXISTS UserFinanRecords (usr_name TEXT, date TEXT, recordNum TEXT, income REAL, income_s TEXT, expense REAL, expense_s TEXT, remark TEXT)''')
				
	#insert one record
	def sql_insert_one_record(self, record_info = {}):
		self.cursor.execute("INSERT INTO UserFinanRecords VALUES (?,?,?,?,?,?,?,?)", \
							(record_info['name'], record_info['date'], record_info['record_no'], float(record_info['income']), record_info['income_s'], float(record_info['expense']), record_info['expense_s'], record_info['comment'],))
		
	#update one record
	def sql_update_one_record(self, old_record_no, record_info = {}):
		#at first delete the old record
		self.cursor.execute("DELETE FROM UserFinanRecords WHERE recordNum = ?", (old_record_no,))
		#add the new record
		self.cursor.execute("INSERT INTO UserFinanRecords VALUES (?,?,?,?,?,?,?,?)", \
							(record_info['name'], record_info['date'], record_info['record_no'], float(record_info['income']), record_info['income_s'], float(record_info['expense']), record_info['expense_s'], record_info['comment'],))
	
	#query one record
	def sql_query_one_record(self, record_number, name = None):
		if name == None:
			self.cursor.execute("SELECT * FROM UserFinanRecords WHERE recordNum = ?", (record_number,))
		else:
			self.cursor.execute("SELECT * FROM UserFinanRecords WHERE recordNum = ? AND usr_name = ?", (record_number, name, ))
		
		res = self.cursor.fetchall()
		
		if len(res):
			''' only return one record
			sql_query_res = {}
			sql_query_res['name'] = res[0][0]
			sql_query_res['date'] = res[0][1]
			sql_query_res['record_no'] = res[0][2]
			sql_query_res['income'] = res[0][3]
			sql_query_res['income_s'] = res[0][4]
			sql_query_res['expense'] = res[0][5]
			sql_query_res['expense_s'] = res[0][6]
			sql_query_res['comment'] = res[0][7]
			
			return sql_query_res
			'''
			
			return res
		else:
			return False
	#delete one record
	def delete_one_record(self, record_num = None, name = None):
		if name == None:
			#delete record
			self.cursor.execute("DELETE FROM UserFinanRecords WHERE recordNum = ?", (record_num,))
		else:
			self.cursor.execute("DELETE FROM UserFinanRecords WHERE recordNum = ? AND usr_name = ?", (record_num, name, ))
	
	#profit compute
	def comput_profit(self):
		gross_profit = 0;
		
		self.cursor.execute("SELECT income FROM UserFinanRecords")		
		income_res = self.cursor.fetchall()
		total_income = 0;
		for income in income_res:
			total_income+= income[0]
		
		self.cursor.execute("SELECT expense FROM UserFinanRecords")		
		expense_res = self.cursor.fetchall()
		total_expense = 0
		for expense in expense_res:
			total_expense += expense[0]
			
		gross_profit = total_income - total_expense

		return gross_profit
	
	def close_sqlite(self):
		self.cursor.close()
		self.conn.commit()
		self.conn.close()
		
