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
import SRF_sqlite
import SFR_login



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
	

################################ main panel for server ########################################	
#server main panel
class MainPanelServer(Toplevel):
	#init
	def __init__(self, master = None, user_name = None):
		Toplevel.__init__(self, master)
		self.master = master
		master.withdraw()
		self.user_name = user_name
		win_width = 860
		win_height = 245
		win_pos_x = self.winfo_screenwidth() // 2 - win_width // 2
		win_pos_y = (self.winfo_screenheight() - 100) // 2 - win_height // 2
		self.geometry('%sx%s+%s+%s' % (win_width, win_height, win_pos_x, win_pos_y))
		#gui init
		self.server_gui_init()
		#sqlite init
		self.sqlite_records = FinancialDataRecord()
		
	def destroy(self):
		is_quit = tkinter.messagebox.askyesno(message = '确认退出？', icon = 'question', title = 'quit')
		if is_quit == True:
			self.sqlite_records.close_sqlite()
			self.quit()
		
	#gui init
	def server_gui_init(self):
		self.title('Server Main Panel')
		self.gui_frame = ttk.Frame(self)
		#row 0
		self.usr_name_lbl = ttk.Label(self.gui_frame, text = '用户名: %s'%(self.user_name))
		#row 1		
		self.record_no_lbl = ttk.Label(self.gui_frame, text = '订单编号:')
		self.record_no_var = StringVar()
		self.record_no = ttk.Entry(self.gui_frame, textvariable = self.record_no_var)
		self.date_lbl = ttk.Label(self.gui_frame, text = '日期(可选):')
		self.date_var = StringVar()
		self.date = ttk.Entry(self.gui_frame, textvariable = self.date_var)
		self.income_lbl = ttk.Label(self.gui_frame, text = '收入:')
		self.income_var = StringVar()
		self.income = ttk.Entry(self.gui_frame, textvariable = self.income_var)
		self.expense_lbl = ttk.Label(self.gui_frame, text = '支出:')
		self.expense_var = StringVar()
		self.expense = ttk.Entry(self.gui_frame, textvariable = self.expense_var)
		#row 2
		self.income_relate_lbl = ttk.Label(self.gui_frame, text = '收入关联:')
		self.income_relate_var = StringVar()
		self.income_relate = ttk.Entry(self.gui_frame, textvariable = self.income_relate_var)
		self.income_relate['width'] = self.income_relate['width'] * 2
		self.expense_relate_lbl = ttk.Label(self.gui_frame, text = '支出关联:')
		self.expense_relate_var = StringVar()
		self.expense_relate = ttk.Entry(self.gui_frame, textvariable = self.expense_relate_var)
		self.expense_relate['width'] = self.expense_relate['width'] * 2
		#row 3
		self.comment_lbl = ttk.Label(self.gui_frame, text = '备注:')
		self.comment_var = StringVar()
		self.comment = ttk.Entry(self.gui_frame, textvariable = self.comment_var)
		self.comment['width'] = self.comment['width'] * 5
		#row 4
		self.create_record_bnt = ttk.Button(self.gui_frame, text = '创建订单', command = self.bnt_create_new_record)
		#row 5
		self.record_no_search_lbl = ttk.Label(self.gui_frame, text = '订单编号:')
		self.record_no_search_var = StringVar()
		self.record_no_search = ttk.Entry(self.gui_frame, textvariable = self.record_no_search_var)
		self.date_search_lbl = ttk.Label(self.gui_frame, text = '日期(可选):')
		self.date_search_var = StringVar()
		self.date_search = ttk.Entry(self.gui_frame, textvariable = self.date_search_var)
		self.search_bnt = ttk.Button(self.gui_frame, text = '查询', command = self.bnt_search_record)
		#row 6
		self.gross_profit_lbl = ttk.Label(self.gui_frame, text = '毛利:')
		self.gross_profit = ttk.Label(self.gui_frame, text = '0')
		self.gross_update_bnt = ttk.Button(self.gui_frame, text = '更新', command = self.bnt_update_gross_profit)
		self.reg_user_manage_bnt = ttk.Button(self.gui_frame, text = '用户管理', command = self.bnt_manage_users)
		
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
		self.reg_user_manage_bnt.grid(column = 7, row = gui_row, sticky = E)
	
	#create a new record
	def bnt_create_new_record(self):
		self.one_record = {}
		self.one_record['name'] = self.user_name
		self.one_record['record_no'] = self.record_no_var.get()
		self.one_record['date'] = self.date_var.get()
		self.one_record['income'] = self.income_var.get()
		self.one_record['income_s'] = self.income_relate_var.get()
		self.one_record['expense'] = self.expense_var.get()
		self.one_record['expense_s'] = self.expense_relate_var.get()
		self.one_record['comment'] = self.comment_var.get()
		
		if self.one_record['record_no'] == '':
			tkinter.messagebox.showinfo('Warning', '请输入订单编号')
			return
			
		if self.one_record['income'] == '' or self.one_record['expense'] == '':
			is_create = tkinter.messagebox.askyesno('ask', '支出或收入为空，确认保存？')
			if not is_create:
				return
			else:
				if self.one_record['income'] == '':
					self.one_record['income'] = 0.0
				if self.one_record['expense'] == '':
					self.one_record['expense'] = 0.0
					
		#need acquire thread lock	
		self.sqlite_records.sql_insert_one_record(self.one_record)
		#need release thread lock
		
	#search a history record_no
	def bnt_search_record(self):
		record_number = self.record_no_search_var.get()
		if record_number == '':
			tkinter.messagebox.showinfo('Search', '搜索订单编号不能为空！')
		else:
			#need acquire thread lock
			search_res = self.sqlite_records.sql_query_one_record(record_number)
			#need release thread lock
		
			if search_res == False:
				tkinter.messagebox.showinfo('Search Result', '无订单记录')
			else:
				self.search_win = ChildPanelSearch(self, search_res, sql_api = self.sqlite_records)				
				
	#update the gross profit
	def bnt_update_gross_profit(self):
		pass
		
	#manage the registered user
	def bnt_manage_users(self):
		UserPanelManage(self)
		
######################################## main panel for client ###################################		
#client main panel
class MainPanelClient(Toplevel):
	#init
	def __init__(self, master = None, user_name = None):
		Toplevel.__init__(self, master)
		self.master = master
		master.withdraw()
		#gui init
		self.user_name = user_name
		win_width = 860
		win_height = 215
		win_pos_x = self.winfo_screenwidth() // 2 - win_width // 2
		win_pos_y = (self.winfo_screenheight() - 100) // 2 - win_height // 2
		self.geometry('%sx%s+%s+%s' % (win_width, win_height, win_pos_x, win_pos_y))
		self.client_gui_init()
		#tcpip init for record store or search
		
		
	#destroy the window
	def destroy(self):
		is_quit = tkinter.messagebox.askyesno(message = '确认退出？', icon = 'question', title = 'quit')
		if is_quit == True:
			self.quit()
		
	#gui init
	def client_gui_init(self):
		self.title('Client Main Panel')
		self.gui_frame = ttk.Frame(self)
		#row 0
		self.usr_name_lbl = ttk.Label(self.gui_frame, text = '用户名: %s'%(self.user_name))
		#row 1		
		self.record_no_lbl = ttk.Label(self.gui_frame, text = '订单编号:')
		self.record_no_var = StringVar()
		self.record_no = ttk.Entry(self.gui_frame, textvariable = self.record_no_var)
		self.date_lbl = ttk.Label(self.gui_frame, text = '日期(可选):')
		self.date_var = StringVar()
		self.date = ttk.Entry(self.gui_frame, textvariable = self.date_var)
		self.income_lbl = ttk.Label(self.gui_frame, text = '收入:')
		self.income_var = StringVar()
		self.income = ttk.Entry(self.gui_frame, textvariable = self.income_var)
		self.expense_lbl = ttk.Label(self.gui_frame, text = '支出:')
		self.expense_var = StringVar()
		self.expense = ttk.Entry(self.gui_frame, textvariable = self.expense_var)
		#row 2
		self.income_relate_lbl = ttk.Label(self.gui_frame, text = '收入关联:')
		self.income_relate_var = StringVar()
		self.income_relate = ttk.Entry(self.gui_frame, textvariable = self.income_relate_var)
		self.income_relate['width'] = self.income_relate['width'] * 2
		self.expense_relate_lbl = ttk.Label(self.gui_frame, text = '支出关联:')
		self.expense_relate_var = StringVar()
		self.expense_relate = ttk.Entry(self.gui_frame, textvariable = self.expense_relate_var)
		self.expense_relate['width'] = self.expense_relate['width'] * 2
		#row 3
		self.comment_lbl = ttk.Label(self.gui_frame, text = '备注:')
		self.comment_var = StringVar()
		self.comment = ttk.Entry(self.gui_frame, textvariable = self.comment_var)
		self.comment['width'] = self.comment['width'] * 5
		#row 4
		self.create_record_bnt = ttk.Button(self.gui_frame, text = '创建订单', command = self.bnt_create_new_record)
		#row 5
		self.record_no_search_lbl = ttk.Label(self.gui_frame, text = '订单编号:')
		self.record_no_search_var = StringVar()
		self.record_no_search = ttk.Entry(self.gui_frame, textvariable = self.record_no_search_var)
		self.date_search_lbl = ttk.Label(self.gui_frame, text = '日期(可选):')
		self.date_search_var = StringVar()
		self.date_search = ttk.Entry(self.gui_frame, textvariable = self.date_search_var)
		self.search_bnt = ttk.Button(self.gui_frame, text = '查询', command = self.bnt_search_record)
		
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
	
	#create a new record
	def bnt_create_new_record(self):
		self.one_record = {}
		self.one_record['name'] = self.user_name
		self.one_record['record_no'] = self.record_no_var.get()
		self.one_record['date'] = self.date_var.get()
		self.one_record['income'] = self.income_var.get()
		self.one_record['income_s'] = self.income_relate_var.get()
		self.one_record['expense'] = self.expense_var.get()
		self.one_record['expense_s'] = self.expense_relate_var.get()
		self.one_record['comment'] = self.comment_var.get()
		
		if self.one_record['record_no'] == '':
			tkinter.messagebox.showinfo('Warning', '请输入订单编号')
			return
			
		if self.one_record['income'] == '' or self.one_record['expense'] == '':
			is_create = tkinter.messagebox.askyesno('ask', '支出或收入为空，确认保存？')
			if not is_create:
				return
			else:
				if self.one_record['income'] == '':
					self.one_record['income'] = 0.0
				if self.one_record['expense'] == '':
					self.one_record['expense'] = 0.0
					
		#transfer record to master through tcpip
		pass
		
	#search a history record_no
	def bnt_search_record(self):
		record_number = self.record_no_search_var.get()
		if record_number == '':
			tkinter.messagebox.showinfo('Search', '搜索订单编号不能为空！')
		else:			
			#send the quest for record to master and wait for the record returned
			search_res = False
		
			if search_res == False:
				tkinter.messagebox.showinfo('Search Result', '无订单记录')
			else:
				if search_res['name'] == self.user_name:
					self.search_win = ChildPanelSearch(self, search_res)
				else:
					tkinter.messagebox.showinfo('Warning', '无权查看该订单！请联系管理员')
############################################## panel for search result #################################
#search panel
class ChildPanelSearch(Toplevel):
	#init
	def __init__(self, master = None, search_res = None, sql_api = None, tcpip_api = None):
		Toplevel.__init__(self, master)
		self.search_result = search_res
		self.is_modify = True
		self.sql_api = sql_api
		self.tcpip_api = tcpip_api
		win_width = 860
		win_height = 130
		win_pos_x = self.winfo_screenwidth() // 2 - win_width // 2
		win_pos_y = (self.winfo_screenheight() - 100) // 2 - win_height // 2
		self.geometry('%sx%s+%s+%s' % (win_width, win_height, win_pos_x, win_pos_y))
		#search gui init
		self.search_win_init()
		self.search_dispaly_init()
		
	#init
	def search_win_init(self):
		self.title('Search Result')
		self.gui_frame = ttk.Frame(self)
		#row 0		
		self.record_no_lbl = ttk.Label(self.gui_frame, text = '订单编号:')
		self.record_no_var = StringVar()
		self.record_no = ttk.Entry(self.gui_frame, textvariable = self.record_no_var, state = 'disabled', font = 'Helvetica 8 bold')
		self.date_lbl = ttk.Label(self.gui_frame, text = '日期(可选):')
		self.date_var = StringVar()
		self.date = ttk.Entry(self.gui_frame, textvariable = self.date_var, state = 'disabled', font = 'Helvetica 8 bold')
		self.income_lbl = ttk.Label(self.gui_frame, text = '收入:')
		self.income_var = StringVar()
		self.income = ttk.Entry(self.gui_frame, textvariable = self.income_var, state = 'disabled', font = 'Helvetica 8 bold')
		self.expense_lbl = ttk.Label(self.gui_frame, text = '支出:')
		self.expense_var = StringVar()
		self.expense = ttk.Entry(self.gui_frame, textvariable = self.expense_var, state = 'disabled', font = 'Helvetica 8 bold')
		#row 1
		self.income_relate_lbl = ttk.Label(self.gui_frame, text = '收入关联:')
		self.income_relate_var = StringVar()
		self.income_relate = ttk.Entry(self.gui_frame, textvariable = self.income_relate_var, state = 'disabled', font = 'Helvetica 8 bold')
		self.income_relate['width'] = self.income_relate['width'] * 2
		self.expense_relate_lbl = ttk.Label(self.gui_frame, text = '支出关联:')
		self.expense_relate_var = StringVar()
		self.expense_relate = ttk.Entry(self.gui_frame, textvariable = self.expense_relate_var, state = 'disabled', font = 'Helvetica 8 bold')
		self.expense_relate['width'] = self.expense_relate['width'] * 2
		#row 2
		self.comment_lbl = ttk.Label(self.gui_frame, text = '备注:')
		self.comment_var = StringVar()
		self.comment = ttk.Entry(self.gui_frame, textvariable = self.comment_var, state = 'disabled', font = 'Helvetica 8 bold')
		self.comment['width'] = self.comment['width'] * 5
		#row 3
		self.search_sure_bnt = ttk.Button(self.gui_frame, text = '确认', command = self.btn_search_sure)
		self.bnt_modify_text = StringVar()
		self.bnt_modify_text.set('修改')
		self.search_modify_bnt = ttk.Button(self.gui_frame, textvariable = self.bnt_modify_text, command = self.btn_search_saveOrmodify)
		
		#grid widgets
		self.gui_frame.grid(column = 0, row = 0, padx = 10)
		#row 0
		gui_row = 0
		self.record_no_lbl.grid(column = 0, row = gui_row, sticky = W, pady = 5)
		self.record_no.grid(column = 1, row = gui_row)
		self.date_lbl.grid(column = 2, row = gui_row)
		self.date.grid(column = 3, row = gui_row)
		self.income_lbl.grid(column = 4, row = gui_row)
		self.income.grid(column = 5, row = gui_row)
		self.expense_lbl.grid(column = 6, row = gui_row)
		self.expense.grid(column = 7, row = gui_row)
		#row 1
		gui_row = 1
		self.income_relate_lbl.grid(column = 0, row = gui_row, pady = 5)
		self.income_relate.grid(column = 1, row = gui_row, columnspan = 3, sticky = W)
		self.expense_relate_lbl.grid(column = 4, row = gui_row)
		self.expense_relate.grid(column = 5, row = gui_row, columnspan = 3, sticky = W)		
		#row 2
		gui_row = 2
		self.comment_lbl.grid(column = 0, row = gui_row, sticky = W, pady = 5)
		self.comment.grid(column = 1, row = gui_row, columnspan = 7, sticky = W)
		#row 3
		gui_row = 3
		self.search_sure_bnt.grid(column = 3, row = gui_row, sticky = W, padx = 3)
		self.search_modify_bnt.grid(column = 4, row = gui_row, sticky = E, padx = 3)
		
	#init search result
	def search_dispaly_init(self):
		self.record_no_var.set(self.search_result['record_no'])
		self.date_var.set(self.search_result['date'])
		self.income_var.set(self.search_result['income'])
		self.income_relate_var.set(self.search_result['income_s'])
		self.expense_var.set(self.search_result['expense'])
		self.expense_relate_var.set(self.search_result['expense_s'])
		self.comment_var.set(self.search_result['comment'])
	#sure for searching result
	def btn_search_sure(self):
		if not self.is_modify:
			is_quit = tkinter.messagebox.askyesno(message = '是否保存修改？', icon = 'question', title = 'ask')
			if is_quit == True:
				self.bnt_modify_text.set('保存')
				self.is_modify = True
			else:
				self.is_modify = False
		self.destroy()
	
	#save/modify for searching result
	def btn_search_saveOrmodify(self):
		if self.is_modify:
			self.bnt_modify_text.set('保存')
			self.is_modify = False
			self.en_disable_records_modify('enabled')
		else:
			self.is_modify = True
			#save the change
			if self.sql_api != None:	#master call
				self.save_modify_master()
			elif self.tcpip_api != None:
				self.save_modify_client()
			else:
				pass
			self.bnt_modify_text.set('修改')
			self.en_disable_records_modify('disabled')
	
	#enable or disable the widgets
	def en_disable_records_modify(self, is_en_disable):
		if is_en_disable in ('disabled', 'enabled'):
			self.record_no['state'] = is_en_disable
			self.date['state'] = is_en_disable
			self.income['state'] = is_en_disable
			self.income_relate['state'] = is_en_disable
			self.expense['state'] = is_en_disable
			self.expense_relate['state'] = is_en_disable
			self.comment['state'] = is_en_disable

	#save/modify action for master
	def save_modify_master(self):
		modifed_records = {}
		modifed_records['name'] = self.search_result['name']
		modifed_records['record_no'] = self.record_no_var.get()
		modifed_records['date'] = self.date_var.get()
		modifed_records['income'] = self.income_var.get()
		modifed_records['income_s'] = self.income_relate_var.get()
		modifed_records['expense'] = self.expense_var.get()
		modifed_records['expense_s'] = self.expense_relate_var.get()
		modifed_records['comment'] = self.comment_var.get()
		
		self.sql_api.sql_update_one_record(self.search_result['record_no'], modifed_records)
	
	#save/modify action for client
	def save_modify_client(self):
		pass
############################################## panel for user manage#################################	
class UserPanelManage(Toplevel):
	#init
	def __init__(self, master = None):
		Toplevel.__init__(self, master)
		self.is_modify = True
		win_width = 307
		win_height = 260
		win_pos_x = self.winfo_screenwidth() // 2 - win_width // 2
		win_pos_y = (self.winfo_screenheight() - 100) // 2 - win_height // 2
		self.geometry('%sx%s+%s+%s' % (win_width, win_height, win_pos_x, win_pos_y))
		#mange gui init
		self.manage_win_init()	
		
	#gui init
	def manage_win_init(self):
		self.title('User Manage')
		self.gui_frame = ttk.Frame(self)		
		#row 0
		self.user_list_lbl = ttk.Label(self.gui_frame, text = '已注册用户列表')
		#row 1
		self.user_list_box = Listbox(self.gui_frame, height = 10)
		self.list_scro = ttk.Scrollbar(self.gui_frame, orient = VERTICAL, command = self.user_list_box.yview) 
		#row 2
		self.bnt_sure = ttk.Button(self.gui_frame, text = '确认', command = self.bnt_user_manage_sure)
		self.bnt_delete = ttk.Button(self.gui_frame, text = '删除', command = self.bnt_user_manage_del)
		self.bnt_modify = ttk.Button(self.gui_frame, text = '修改密码', command = self.bnt_user_modify)
		
		#grid widgets
		self.gui_frame.grid(column = 0, row = 0, padx = 10)
		#row 0
		self.user_list_lbl.grid(column = 0, row = 0, columnspan = 3, pady = 5)
		#row 1
		self.user_list_box.grid(column = 0, row = 1, columnspan = 3, sticky = (N, W, E, S))
		self.list_scro.grid(column = 3, row = 1, sticky = (N, S))
		self.user_list_box['yscrollcommand'] = self.list_scro.set
		#row 2
		self.bnt_sure.grid(column = 0, row = 2, padx = 5, pady = 10)
		self.bnt_delete.grid(column = 1, row = 2)
		self.bnt_modify.grid(column = 2, row = 2)
		
	#sure
	def bnt_user_manage_sure(self):
		self.destroy()
	
	#delete
	def bnt_user_manage_del(self):
		is_delete = tkinter.messagebox.askyesno(message = '确认删除该用户？', icon = 'question', title = 'ask')
		if is_delete == True:
			pass
			
	#modify
	def bnt_user_modify(self):
		pass