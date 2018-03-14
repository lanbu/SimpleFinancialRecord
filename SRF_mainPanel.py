#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' main panel '

__author__ = 'Lanbu'

from tkinter import *
from tkinter import ttk
import pickle
import tkinter.messagebox
import sqlite3
from SRF_sqlite import *



class MainPanel():
	#init
	def __init__(self, master = None, user_role = 0, user_name = None):		
		#panel init
		if user_role == 1:	#server main panel
			self.server_panel = MainPanelServer(master, user_name)
		else:	#client main panel
			self.client_panel = MainPanelClient(master, user_name)
		#connect sqlite
		#self.finiancial_record = FinancialDataRecord()
		
		#tcpip server
	
	
#server main panel
class MainPanelServer(Toplevel):
	#init
	def __init__(self, master = None, user_name = None):
		Toplevel.__init__(self, master)
		self.user_name = user_name
		#gui init
		self.server_gui_init()
		
		
		
	#gui init
	def server_gui_init(self):
		self.title('Server Main Panel')
		self.gui_frame = ttk.Frame(self)
		#row 0
		self.usr_name_lbl = ttk.Label(self.gui_frame, text = '用户名: %s'%(self.user_name))
		#row 1		
		self.record_no_lbl = ttk.Label(self.gui_frame, text = '订单编号:')
		self.record_no = ttk.Entry(self.gui_frame)
		self.date_lbl = ttk.Label(self.gui_frame, text = '日期(可选):')
		self.date = ttk.Entry(self.gui_frame)
		self.income_lbl = ttk.Label(self.gui_frame, text = '收入:')
		self.income = ttk.Entry(self.gui_frame)
		self.expense_lbl = ttk.Label(self.gui_frame, text = '支出:')
		self.expense = ttk.Entry(self.gui_frame)
		#row 2
		self.income_relate_lbl = ttk.Label(self.gui_frame, text = '收入关联:')
		self.income_relate = ttk.Entry(self.gui_frame)
		self.income_relate['width'] = self.income_relate['width'] * 2
		self.expense_relate_lbl = ttk.Label(self.gui_frame, text = '支出关联:')
		self.expense_relate = ttk.Entry(self.gui_frame)
		self.expense_relate['width'] = self.expense_relate['width'] * 2
		#row 3
		self.comment_lbl = ttk.Label(self.gui_frame, text = '备注:')
		self.comment = ttk.Entry(self.gui_frame)
		self.comment['width'] = self.comment['width'] * 5
		#row 4
		self.create_record_bnt = ttk.Button(self.gui_frame, text = '创建订单')
		#row 5
		self.record_no_search_lbl = ttk.Label(self.gui_frame, text = '订单编号:')
		self.record_no_search = ttk.Entry(self.gui_frame)
		self.date_search_lbl = ttk.Label(self.gui_frame, text = '日期(可选):')
		self.date_search = ttk.Entry(self.gui_frame)
		self.search_bnt = ttk.Button(self.gui_frame, text = '查询')
		#row 6
		self.gross_profit_lbl = ttk.Label(self.gui_frame, text = '毛利:')
		self.gross_profit = ttk.Label(self.gui_frame, text = '0')
		self.gross_update_bnt = ttk.Button(self.gui_frame, text = '更新')
		
		#grid widgets
		self.gui_frame.grid(column = 0, row = 0, padx = 10)
		#row 0
		gui_row = 0
		self.usr_name_lbl.grid(column = 0, row = gui_row, columnspan = 2, sticky = W, pady = 10)
		#row 1
		gui_row = 1
		self.record_no_lbl.grid(column = 0, row = gui_row, sticky = W, pady = 5)
		self.record_no.grid(column = 1, row = gui_row)
		self.date_lbl.grid(column = 2, row = gui_row)
		self.date.grid(column = 3, row = gui_row)
		self.income_lbl.grid(column = 4, row = gui_row)
		self.income.grid(column = 5, row = gui_row)
		self.expense_lbl.grid(column = 6, row = gui_row)
		self.expense.grid(column = 7, row = gui_row)
		#row 2
		gui_row = 2
		self.income_relate_lbl.grid(column = 0, row = gui_row, pady = 5)
		self.income_relate.grid(column = 1, row = gui_row, columnspan = 3, sticky = W)
		self.expense_relate_lbl.grid(column = 4, row = gui_row)
		self.expense_relate.grid(column = 5, row = gui_row, columnspan = 3, sticky = W)		
		#row 3
		gui_row = 3
		self.comment_lbl.grid(column = 0, row = gui_row, sticky = W, pady = 5)
		self.comment.grid(column = 1, row = gui_row, columnspan = 7, sticky = W)
		#row 4
		gui_row = 4
		self.create_record_bnt.grid(column = 3, row = gui_row, columnspan = 2)
		#row 5
		gui_row = 5
		self.record_no_search_lbl.grid(column = 0, row = gui_row, sticky = W, pady = 10)
		self.record_no_search.grid(column = 1, row = gui_row)
		self.date_search_lbl.grid(column = 2, row = gui_row, sticky = E)
		self.date_search.grid(column = 3, row = gui_row, sticky = W)
		self.search_bnt.grid(column = 4, row = gui_row, sticky = E)
		#row 6
		gui_row = 6
		self.gross_profit_lbl.grid(column = 0, row = gui_row, sticky = W, pady = 10)
		self.gross_profit.grid(column = 1, row = gui_row, sticky = W)
		self.gross_update_bnt.grid(column = 2, row = gui_row, sticky = E)

#client main panel
class MainPanelClient(Toplevel):
	#init
	def __init__(self, master = None, user_name = None):
		Toplevel.__init__(self, master)
		#gui init
		self.user_name = user_name
		self.client_gui_init()
	#gui init
	def client_gui_init(self):
		self.title('Client Main Panel')
		self.gui_frame = ttk.Frame(self)
		#row 0
		self.usr_name_lbl = ttk.Label(self.gui_frame, text = '用户名: %s'%(self.user_name))
		#row 1		
		self.record_no_lbl = ttk.Label(self.gui_frame, text = '订单编号:')
		self.record_no = ttk.Entry(self.gui_frame)
		self.date_lbl = ttk.Label(self.gui_frame, text = '日期(可选):')
		self.date = ttk.Entry(self.gui_frame)
		self.income_lbl = ttk.Label(self.gui_frame, text = '收入:')
		self.income = ttk.Entry(self.gui_frame)
		self.expense_lbl = ttk.Label(self.gui_frame, text = '支出:')
		self.expense = ttk.Entry(self.gui_frame)
		#row 2
		self.income_relate_lbl = ttk.Label(self.gui_frame, text = '收入关联:')
		self.income_relate = ttk.Entry(self.gui_frame)
		self.income_relate['width'] = self.income_relate['width'] * 2
		self.expense_relate_lbl = ttk.Label(self.gui_frame, text = '支出关联:')
		self.expense_relate = ttk.Entry(self.gui_frame)
		self.expense_relate['width'] = self.expense_relate['width'] * 2
		#row 3
		self.comment_lbl = ttk.Label(self.gui_frame, text = '备注:')
		self.comment = ttk.Entry(self.gui_frame)
		self.comment['width'] = self.comment['width'] * 5
		#row 4
		self.create_record_bnt = ttk.Button(self.gui_frame, text = '创建订单')
		#row 5
		self.record_no_search_lbl = ttk.Label(self.gui_frame, text = '订单编号:')
		self.record_no_search = ttk.Entry(self.gui_frame)
		self.date_search_lbl = ttk.Label(self.gui_frame, text = '日期(可选):')
		self.date_search = ttk.Entry(self.gui_frame)
		self.search_bnt = ttk.Button(self.gui_frame, text = '查询')
		
		#grid widgets
		self.gui_frame.grid(column = 0, row = 0, padx = 10)
		#row 0
		gui_row = 0
		self.usr_name_lbl.grid(column = 0, row = gui_row, columnspan = 2, sticky = W, pady = 10)
		#row 1
		gui_row = 1
		self.record_no_lbl.grid(column = 0, row = gui_row, sticky = W, pady = 5)
		self.record_no.grid(column = 1, row = gui_row)
		self.date_lbl.grid(column = 2, row = gui_row)
		self.date.grid(column = 3, row = gui_row)
		self.income_lbl.grid(column = 4, row = gui_row)
		self.income.grid(column = 5, row = gui_row)
		self.expense_lbl.grid(column = 6, row = gui_row)
		self.expense.grid(column = 7, row = gui_row)
		#row 2
		gui_row = 2
		self.income_relate_lbl.grid(column = 0, row = gui_row, pady = 5)
		self.income_relate.grid(column = 1, row = gui_row, columnspan = 3, sticky = W)
		self.expense_relate_lbl.grid(column = 4, row = gui_row)
		self.expense_relate.grid(column = 5, row = gui_row, columnspan = 3, sticky = W)		
		#row 3
		gui_row = 3
		self.comment_lbl.grid(column = 0, row = gui_row, sticky = W, pady = 5)
		self.comment.grid(column = 1, row = gui_row, columnspan = 7, sticky = W)
		#row 4
		gui_row = 4
		self.create_record_bnt.grid(column = 3, row = gui_row, columnspan = 2)
		#row 5
		gui_row = 5
		self.record_no_search_lbl.grid(column = 0, row = gui_row, sticky = W, pady = 10)
		self.record_no_search.grid(column = 1, row = gui_row)
		self.date_search_lbl.grid(column = 2, row = gui_row, sticky = E)
		self.date_search.grid(column = 3, row = gui_row, sticky = W)
		self.search_bnt.grid(column = 4, row = gui_row, sticky = E)
