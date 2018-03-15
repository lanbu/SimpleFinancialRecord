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
		
	def destroy(self):
		is_quit = tkinter.messagebox.askyesno(message = '确认退出？', icon = 'question', title = 'quit')
		if is_quit == True:
			self.quit()
		
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
		self.create_record_bnt = ttk.Button(self.gui_frame, text = '创建订单', command = self.bnt_create_new_record)
		#row 5
		self.record_no_search_lbl = ttk.Label(self.gui_frame, text = '订单编号:')
		self.record_no_search = ttk.Entry(self.gui_frame)
		self.date_search_lbl = ttk.Label(self.gui_frame, text = '日期(可选):')
		self.date_search = ttk.Entry(self.gui_frame)
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
		pass
		
	#search a history record_no
	def bnt_search_record(self):
		self.search_win = ChildPanelSearch()
		
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
		self.create_record_bnt = ttk.Button(self.gui_frame, text = '创建订单', command = self.bnt_create_new_record)
		#row 5
		self.record_no_search_lbl = ttk.Label(self.gui_frame, text = '订单编号:')
		self.record_no_search = ttk.Entry(self.gui_frame)
		self.date_search_lbl = ttk.Label(self.gui_frame, text = '日期(可选):')
		self.date_search = ttk.Entry(self.gui_frame)
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
		pass
		
	#search a history record_no
	def bnt_search_record(self):
		self.search_win = ChildPanelSearch()
		
############################################## panel for search result #################################
#search panel
class ChildPanelSearch(Toplevel):
	#init
	def __init__(self, master = None):
		Toplevel.__init__(self, master)
		self.is_modify = True
		win_width = 860
		win_height = 130
		win_pos_x = self.winfo_screenwidth() // 2 - win_width // 2
		win_pos_y = (self.winfo_screenheight() - 100) // 2 - win_height // 2
		self.geometry('%sx%s+%s+%s' % (win_width, win_height, win_pos_x, win_pos_y))
		#search gui init
		self.search_win_init()
		
	#init
	def search_win_init(self):
		self.title('Search Result')
		self.gui_frame = ttk.Frame(self)
		#row 0		
		self.record_no_lbl = ttk.Label(self.gui_frame, text = '订单编号:')
		self.record_no = ttk.Entry(self.gui_frame)
		self.date_lbl = ttk.Label(self.gui_frame, text = '日期(可选):')
		self.date = ttk.Entry(self.gui_frame)
		self.income_lbl = ttk.Label(self.gui_frame, text = '收入:')
		self.income = ttk.Entry(self.gui_frame)
		self.expense_lbl = ttk.Label(self.gui_frame, text = '支出:')
		self.expense = ttk.Entry(self.gui_frame)
		#row 1
		self.income_relate_lbl = ttk.Label(self.gui_frame, text = '收入关联:')
		self.income_relate = ttk.Entry(self.gui_frame)
		self.income_relate['width'] = self.income_relate['width'] * 2
		self.expense_relate_lbl = ttk.Label(self.gui_frame, text = '支出关联:')
		self.expense_relate = ttk.Entry(self.gui_frame)
		self.expense_relate['width'] = self.expense_relate['width'] * 2
		#row 2
		self.comment_lbl = ttk.Label(self.gui_frame, text = '备注:')
		self.comment = ttk.Entry(self.gui_frame)
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
		else:
			self.is_modify = True
			self.bnt_modify_text.set('修改')
			
############################################## panel for user manage#################################	
class UserPanelManage(Toplevel):
	#init
	def __init__(self, master = None):
		Toplevel.__init__(self, master)
		self.is_modify = True
		win_width = 220
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
		
		#grid widgets
		self.gui_frame.grid(column = 0, row = 0, padx = 10)
		#row 0
		self.user_list_lbl.grid(column = 0, row = 0, columnspan = 2, pady = 5)
		#row 1
		self.user_list_box.grid(column = 0, row = 1, columnspan = 2, sticky = (N, W, E, S))
		self.list_scro.grid(column = 3, row = 1, sticky = (N, S))
		self.user_list_box['yscrollcommand'] = self.list_scro.set
		#row 2
		self.bnt_sure.grid(column = 0, row = 2, padx = 5, pady = 10)
		self.bnt_delete.grid(column = 1, row = 2)
		
	#sure
	def bnt_user_manage_sure(self):
		self.destroy()
	
	#delete
	def bnt_user_manage_del(self):
		is_delete = tkinter.messagebox.askyesno(message = '确认删除该用户？', icon = 'question', title = 'ask')
		if is_delete == True:
			pass