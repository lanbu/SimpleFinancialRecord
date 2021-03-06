#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' main panel '

__author__ = 'Lanbu'

from tkinter import *
from tkinter import ttk
import pickle
import tkinter.messagebox
import sqlite3
import SRF_sqlite
import SFR_login
import time
from SRF_server_task import *
import queue
import time
import re
from SRF_tcpip_protocol import *
import SRF_CommonDefine as commonDefine
import socket


class MainPanel():
	#init
	def __init__(self, master = None, user_role = 0, user_name = None):		
		#panel init
		if user_role == 1:	#server main panel
			self.server_panel = MainPanelServer(master, user_name)
		else:	#client main panel
			self.client_panel = MainPanelClient(master, user_name)
				

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
		#queue
		self.gui2server_queue = queue.Queue()
		self.server2gui_queue = queue.Queue()
		#gui init
		self.server_gui_init()
		#server logic task init
		self.server_task = ServerLogic(self.gui2server_queue, self.server2gui_queue)
		self.server_task.start()
		#message loop, process the message comes from server task
		self.process_message()
			
	def destroy(self):
		is_quit = tkinter.messagebox.askyesno(message = '确认退出？', icon = 'question', title = 'quit')
		if is_quit == True:
			self.quit()
			self.server_task.server_task_exit()
	#gui init
	def server_gui_init(self):
		#get ip address
		myname = socket.getfqdn(socket.gethostname())
		#获取本机ip
		ipAddr = socket.gethostbyname(myname)
		
		self.title('Server Main Panel')
		self.gui_frame = ttk.Frame(self)
		#row 0
		self.usr_name_lbl = ttk.Label(self.gui_frame, text = '用户名: %s'%(self.user_name))
		self.usr_ip_addr = ttk.Label(self.gui_frame, text = 'ip地址：%s'%(ipAddr))
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
		self.gross_profit_var = StringVar()
		self.gross_profit_var.set('0')
		self.gross_profit = ttk.Label(self.gui_frame, textvariable = self.gross_profit_var)
		self.gross_update_bnt = ttk.Button(self.gui_frame, text = '更新', command = self.bnt_update_gross_profit)
		self.reg_user_manage_bnt = ttk.Button(self.gui_frame, text = '用户管理', command = self.bnt_manage_users)
		
		#grid widgets
		self.gui_frame.grid(column = 0, row = 0, padx = 10)
		#row 0
		gui_row = 0
		self.usr_name_lbl.grid(column = 0, row = gui_row, columnspan = 2, sticky = W, pady = 10)
		self.usr_ip_addr.grid(column = 3, row = gui_row, sticky = W)
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
		
	def process_message(self):
		self.after(100, self.process_message)
		
		while not self.server2gui_queue.empty():
			queue_item = self.server2gui_queue.get()
			if queue_item['cmd'] == 'insert' and queue_item['res'] == 'ok':
				tkinter.messagebox.showinfo('Tips', '创建订单成功！')
			elif queue_item['cmd'] == 'query':
				if queue_item['res'] == 'error':
					tkinter.messagebox.showinfo('Search Result', '无订单记录')
				else:
					queue_item.pop('cmd')
					queue_item.pop('res')
					self.search_win = ChildPanelSearch(master = self, search_res = queue_item['records'], gui2server_queue = self.gui2server_queue)				
			elif queue_item['cmd'] == 'g_profit':
				self.gross_profit_var.set(str(queue_item['g_profit']))
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

		self.one_record['cmd'] = 'insert'
		self.gui2server_queue.put(self.one_record)
			
				
	#search a history record_no
	def bnt_search_record(self):
		record_number = self.record_no_search_var.get()
		if record_number == '':
			tkinter.messagebox.showinfo('Search', '搜索订单编号不能为空！')
		else:
			query_no = {}
			query_no['record_no'] = record_number
			query_no['cmd'] = 'query'
			self.gui2server_queue.put(query_no)
			
	#update the gross profit
	def bnt_update_gross_profit(self):
		profit = {}
		profit['cmd'] = 'profit_update'
		self.gui2server_queue.put(profit)
		
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
		self.conn_res = False
		#gui init
		self.user_name = user_name
		win_width = 890
		win_height = 215
		win_pos_x = self.winfo_screenwidth() // 2 - win_width // 2
		win_pos_y = (self.winfo_screenheight() - 100) // 2 - win_height // 2
		self.geometry('%sx%s+%s+%s' % (win_width, win_height, win_pos_x, win_pos_y))
		self.client_gui_init()
		#ip connecting parameters
		self.ip_addr = commonDefine.SOCKET_SERVER_IP
		self.ip_port = commonDefine.SOCKET_SERVER_PORT
		#message queue for communication between panel and client socket
		self.to_sock_queue = queue.Queue()
		self.from_sock_queue = queue.Queue()
		#tcpip init for record store or search
		self.tcpip_api = TCPIP_client(self.ip_addr, self.ip_port, from_server_queue = self.to_sock_queue, to_server_queue = self.from_sock_queue)
		self.tcpip_api.start()
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
		self.server_connect_bnt_var = StringVar()
		self.server_connect_bnt_var.set('连接')
		self.server_connect_bnt = ttk.Button(self.gui_frame, textvariable = self.server_connect_bnt_var, command = self.bnt_connect)
		self.server_conn_config_bnt = ttk.Button(self.gui_frame, text = '配置', command = self.bnt_config)
		
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
		self.server_connect_bnt.grid(column = 6, row = gui_row, sticky = W)
		self.server_conn_config_bnt.grid(column = 7, row = gui_row, sticky = W)
	
	#create a new record
	def bnt_create_new_record(self):
		if self.conn_res == False:
			tkinter.messagebox.showinfo('tips', '请先连接主机！')
		else:				
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
			self.one_record['head'] = 'client2server'
			self.one_record['pack_type'] = 'store'
			tcpip_protocol = TcpipProtocol()
			record_info_b = tcpip_protocol.encode_dict_bytes(self.one_record)
			send_res = self.tcpip_api.client_send(record_info_b)
			if send_res:
				
				s_recv = self.tcpip_api.client_recv()
				if s_recv: 
					dic_recv = tcpip_protocol.decode_bytes_dict(s_recv)
					if dic_recv['pack_type'] == 'error_ack':
						tkinter.messagebox.showinfo('tips', '创建订单失败！')
					else:					
						if dic_recv['res'] == 'ok':
							tkinter.messagebox.showinfo('tips', '创建订单成功！')
						else:
							tkinter.messagebox.showinfo('tips', '创建订单失败！')
				else:
					tkinter.messagebox.showinfo('tips', '创建订单失败！')
			else:
				tkinter.messagebox.showinfo('tips', '创建订单失败！')
	#search a history record_no
	def bnt_search_record(self):
		if self.conn_res:
			record_number = self.record_no_search_var.get()
			if record_number == '':
				tkinter.messagebox.showinfo('Search', '搜索订单编号不能为空！')
			else:			
				#send the quest for record to master and wait for the record returned
				tcpip_protocol = TcpipProtocol()
				search_record = {}
				search_record['head'] = 'client2server'
				search_record['pack_type'] = 'query'
				search_record['name'] = self.user_name
				search_record['record_no'] = self.record_no_search_var.get()
				
				search_record_b = tcpip_protocol.encode_dict_bytes(search_record)
				send_res = self.tcpip_api.client_send(search_record_b)
				if send_res:
					search_res = self.tcpip_api.client_recv()
					
					if search_res == False:
						tkinter.messagebox.showinfo('Search Result', '无订单记录')
					else:
						dic_search = tcpip_protocol.decode_bytes_dict(search_res)
						if dic_search['pack_type'] == 'error_ack':
							tkinter.messagebox.showinfo('Warning', '查询失败pack_type！')
						else:
							if dic_search['res'] == 'ok':
								dic_search.pop('res')
								dic_search.pop('head')
								dic_search.pop('pack_type')
								self.search_win = ChildPanelSearch(self, dic_search['record'], self.tcpip_api)
							else:
								tkinter.messagebox.showinfo('Warning', '无记录！')
				else:
					tkinter.messagebox.showinfo('Warning', '请求失败！')
		else:
			tkinter.messagebox.showinfo('tips', '请先连接主机！')
	#connect with server by socket
	def bnt_connect(self):
		self.server_connect_bnt['state'] = 'disabled'
		
		conncet_cmd = {'cmd':'connect'}
		self.to_sock_queue.put(conncet_cmd)		
		'''if self.conn_res:
			self.server_connect_bnt_var.set('已连接')
		else:
			tkinter.messagebox.showinfo('Warning', '连接失败！')
			self.server_connect_bnt['state'] = 'enabled'
			self.server_connect_bnt_var.set('连接')'''
	#save the ip configure
	def save_ip_configure(self, ip_addr):
		self.ip_addr = ip_addr
		
	#configure the connecting parameters
	def bnt_config(self):
		ip_config_win = IPConfigurePanel(self)
		
############################################## panel for search result #################################
#search panel
class ChildPanelSearch(Toplevel):
	#init
	def __init__(self, master = None, search_res = None, tcpip_api = None, gui2server_queue = None):
		Toplevel.__init__(self, master)
		self.search_result = search_res
		self.back_record = {'name':self.search_result[0][0], 'record_no':self.search_result[0][2]}
		self.is_modify = True
		self.tcpip_api = tcpip_api
		self.server2gui_queue = gui2server_queue
		self.sel_item = None
		win_width = 790
		win_height = 370
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
		self.search_delete_bnt = ttk.Button(self.gui_frame, text = '删除', command = self.btn_search_delete)
		#row 4
		self.search_tree = ttk.Treeview(self.gui_frame, columns = ('1', '2', '3', '4', '5', '6'))
		#number
		self.search_tree.heading("#0", text="订单号")
		self.search_tree.column("#0", anchor='center', minwidth=0,width=50, stretch=NO)
		#date
		self.search_tree.heading("1", text="日期")   
		self.search_tree.column("1", anchor='center', minwidth=0,width=100, stretch=NO) 
		#income
		self.search_tree.heading("2", text="收入")   
		self.search_tree.column("2", anchor='center', minwidth=0,width=70, stretch=NO)
		#income related
		self.search_tree.heading('3', text = '收入关联')
		self.search_tree.column('3', anchor='center', minwidth=0,width=60, stretch=NO)
		#expense
		self.search_tree.heading("4", text="支出")   
		self.search_tree.column("4", anchor='center', minwidth=0,width=70, stretch=NO)
		#expense related
		self.search_tree.heading("5", text="支出关联")   
		self.search_tree.column("5", anchor='center', minwidth=0,width=60, stretch=NO)
		#comment
		self.search_tree.heading("6", text = '备注')
		self.search_tree.column("6", anchor='center')
		#bind click select
		self.search_tree.bind('<ButtonRelease-1>', self.select_tree_item) 

		self.tree_scro_v = ttk.Scrollbar(self.gui_frame, orient = VERTICAL, command = self.search_tree.yview)
		
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
		self.search_delete_bnt.grid(column = 5, row = gui_row, sticky = E, padx = 3)
		#row 4
		self.search_tree.grid(column = 0, row = 4, columnspan = 8, pady = 10, sticky = (N, W, E, S))
		self.tree_scro_v.grid(column = 9, row = 4, sticky = (N, S))
		self.search_tree['yscrollcommand'] = self.tree_scro_v.set
		
	#init search result
	def search_dispaly_init(self):
		self.date_var.set(self.search_result[0][1])	#date	
		self.record_no_var.set(self.search_result[0][2])	#record nunber			
		self.income_var.set(self.search_result[0][3])	#income
		self.income_relate_var.set(self.search_result[0][4])	#income related
		self.expense_var.set(self.search_result[0][5])	#expense
		self.expense_relate_var.set(self.search_result[0][6])	#expense related
		self.comment_var.set(self.search_result[0][7])	#comment
		
		self.intsert_record_2_tree(self.search_result)
		
	#display update
	def search_display_update(self, update_record = None):
		if update_record != None:
			self.record_no_var.set(update_record['record_no'])
			self.date_var.set(update_record['date'])
			self.income_var.set(update_record['income'])
			self.income_relate_var.set(update_record['income_s'])
			self.expense_var.set(update_record['expense'])
			self.expense_relate_var.set(update_record['expense_s'])
			self.comment_var.set(update_record['comment'])
			
	#insert one record into the displaying tree_scro_h
	def intsert_record_2_tree(self, records = None):
		if records != None:
			for one_record in records:
				self.search_tree.insert('', 'end', text = one_record[2], values = (one_record[1], one_record[3], one_record[4], one_record[5],one_record[6], one_record[7]))
		
	#response for tree item selected
	def select_tree_item(self, e):
		if not self.is_modify:
			is_quit = tkinter.messagebox.askyesno(message = '是否保存修改？', icon = 'question', title = 'ask')
			if is_quit == True:
				self.btn_search_saveOrmodify()					
			else:
				self.is_modify = False		
				self.en_disable_records_modify('disabled')
				
		self.sel_item = self.search_tree.selection()[0]
		selected_item = self.search_tree.item(self.search_tree.selection())
		selected_record = {}
		selected_record['record_no'] = selected_item['text']
		selected_record['date'] = selected_item['values'][0]
		selected_record['income'] = selected_item['values'][1]
		selected_record['income_s'] = selected_item['values'][2]
		selected_record['expense'] = selected_item['values'][3]
		selected_record['expense_s'] = selected_item['values'][4]
		selected_record['comment'] = selected_item['values'][5]
		
		#backup the selected record
		self.back_record['record_no'] = selected_record['record_no']
		self.back_record['date'] = selected_record['date']
		self.back_record['income'] = selected_record['income']
		self.back_record['income_s'] = selected_record['income_s']
		self.back_record['expense'] = selected_record['expense']
		self.back_record['expense_s'] = selected_record['expense_s']
		self.back_record['comment'] = selected_record['comment']
		
	#sure for searching result
	def btn_search_sure(self):
		if not self.is_modify:
			is_quit = tkinter.messagebox.askyesno(message = '是否保存修改？', icon = 'question', title = 'ask')
			if is_quit == True:
				self.btn_search_saveOrmodify()
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
			if self.tcpip_api != None:
				self.save_modify_client()
			else:
				self.save_modify_master()	#master call
				
			self.bnt_modify_text.set('修改')
			self.en_disable_records_modify('disabled')
			
	#delete the record
	def btn_search_delete(self):
		is_delete = tkinter.messagebox.askyesno(message = '确认删除该记录？删除后不可恢复！', icon = 'question', title = 'ask')
		if is_delete:
			if self.tcpip_api != None:	#client call
				self.delete_record_client()
			else:
				delete_record = {}
				delete_record['cmd'] = 'delete'
				delete_record['record'] = self.back_record
				self.server2gui_queue.put(delete_record)
				
			#disable the modify button
			self.search_modify_bnt['state'] = 'disabled'
			#clean the dipaly
			self.record_no_var.set('')
			self.date_var.set('')
			self.income_var.set('')
			self.income_relate_var.set('')
			self.expense_var.set('')
			self.expense_relate_var.set('')
			self.comment_var.set('')
			
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
		modifed_records['name'] = self.search_result[0][0]	#name
		modifed_records['record_no'] = self.record_no_var.get()
		modifed_records['date'] = self.date_var.get()
		modifed_records['income'] = self.income_var.get()
		modifed_records['income_s'] = self.income_relate_var.get()
		modifed_records['expense'] = self.expense_var.get()
		modifed_records['expense_s'] = self.expense_relate_var.get()
		modifed_records['comment'] = self.comment_var.get()
		
		modifed_records['cmd'] = 'update'
		modifed_records['old_no'] = self.back_record	#old record	
		self.server2gui_queue.put(modifed_records)
			
	#save/modify action for client
	def save_modify_client(self):
		modifed_records = {}
		modifed_records['name'] = self.search_result[0][0]	#name
		modifed_records['record_no'] = self.record_no_var.get()
		modifed_records['date'] = self.date_var.get()
		modifed_records['income'] = self.income_var.get()
		modifed_records['income_s'] = self.income_relate_var.get()
		modifed_records['expense'] = self.expense_var.get()
		modifed_records['expense_s'] = self.expense_relate_var.get()
		modifed_records['comment'] = self.comment_var.get()
		
		modifed_records['pack_type'] = 'update'
		modifed_records['record_no_old'] = self.search_result[0][2]	#record number
		modifed_records['head'] = 'client2server'

		tcpip_protocol = TcpipProtocol()
		record_info_b = tcpip_protocol.encode_dict_bytes(modifed_records)
		send_res = self.tcpip_api.client_send(record_info_b)
		
		modify_res = False
		if send_res:
			s_recv = self.tcpip_api.client_recv()
			if s_recv: 
				dic_recv = tcpip_protocol.decode_bytes_dict(s_recv)

				if dic_recv['pack_type'] == 'error_ack':
					tkinter.messagebox.showinfo('tips', '修改订单失败！')
				else:
					if dic_recv['res'] != 'ok':
						tkinter.messagebox.showinfo('tips', '修改订单失败！')
					else:
						modify_res = True
			else:
				tkinter.messagebox.showinfo('tips', '修改订单失败！')
		else:
			tkinter.messagebox.showinfo('tips', '修改订单失败！')
		
		return modify_res
	#delete action for client
	def delete_record_client(self):
		delete_record = {}
		delete_record['pack_type'] = 'delete'
		delete_record['record_no'] = self.record_no_var.get()
		delete_record['name'] = self.search_result[0][0]	#name
		delete_record['head'] = 'client2server'
		
		tcpip_protocol = TcpipProtocol()
		record_info_b = tcpip_protocol.encode_dict_bytes(delete_record)
		send_res = self.tcpip_api.client_send(record_info_b)
		
		delete_res = False
		if send_res:
			s_recv = self.tcpip_api.client_recv()
			if s_recv: 
				dic_recv = tcpip_protocol.decode_bytes_dict(s_recv)
				
				if dic_recv['pack_type'] == 'error_ack':
					tkinter.messagebox.showinfo('tips', '删除订单失败！')
				else:
					if dic_recv['res'] != 'ok':
						tkinter.messagebox.showinfo('tips', '删除订单失败！')
					else:
						delete_res = True
			else:
				tkinter.messagebox.showinfo('tips', '删除订单失败！')
		else:
			tkinter.messagebox.showinfo('tips', '删除订单失败！')
		return delete_res
############################################## panel for ip configure ###############################
class IPConfigurePanel(Toplevel):
	#init
	def __init__(self, master = None):
		Toplevel.__init__(self, master)
		win_width = 245
		win_height = 90
		win_pos_x = self.winfo_screenwidth() // 2 - win_width // 2
		win_pos_y = (self.winfo_screenheight() - 100) // 2 - win_height // 2
		self.geometry('%sx%s+%s+%s' % (win_width, win_height, win_pos_x, win_pos_y))
		#mange gui init
		self.manage_win_init()
		
	def manage_win_init(self):
		self.title('ip设置')
		self.gui_frame = ttk.Frame(self)
		
		#row 0
		self.ip_addr_lbl = ttk.Label(self.gui_frame, text = 'ip地址：')
		self.ip_addr_var = StringVar()
		self.ip_addr_entry = ttk.Entry(self.gui_frame, textvariable = self.ip_addr_var)
		#row 1
		self.ip_eg_lbl = ttk.Label(self.gui_frame, text = '示例:192.168.1.1')
		#row 2
		self.ip_sure = ttk.Button(self.gui_frame, text = '确认', command = self.bnt_ip_sure)
		self.ip_cancle = ttk.Button(self.gui_frame, text = '取消', command = self.bnt_ip_cancle)
		
		#grid
		self.gui_frame.grid(column = 0, row = 0, padx = 10)
		#row 0 
		self.ip_addr_lbl.grid(column = 0, row = 0, sticky = W, pady = 5)
		self.ip_addr_entry.grid(column = 1, row = 0, columnspan = 2, sticky = E)
		#row 1
		self.ip_eg_lbl.grid(column = 1, row = 1, columnspan = 2, sticky = W)
		#row 2
		self.ip_sure.grid(column = 1, row = 2)
		self.ip_cancle.grid(column = 2, row = 2)
		
	def bnt_ip_sure(self):
		ip_addr = self.ip_addr_var.get()
		
		match_res = re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip_addr)
		if match_res != None:	
			self.master.save_ip_configure(ip_addr)
			self.destroy()
		else:
			tkinter.messagebox.showinfo('警告', 'ip地址格式错误')
		
	def bnt_ip_cancle(self):
		self.destroy()
		
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
		self.list_users = StringVar()
		self.user_list_box = Listbox(self.gui_frame, listvariable = self.list_users, height = 10)
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
		
		#init list box of users registered
		try:
			with open(self.master.master.login_userinfo_path, 'rb') as usr_file:
				self.usrs_info = pickle.load(usr_file)
		except FileNotFoundError:
			with open(self.master.master.login_userinfo_path, 'wb') as usr_file:
				self.usrs_info = {self.master.master.administor_name:selfmastr.master.administor_pwd}	#null dictionary			
				pickle.dump(self.usrs_info, usr_file)		
		
		users_list = []
		for user in self.usrs_info:
			users_list.append(user)
		self.list_users.set(users_list)
		
		# Colorize alternating lines of the listbox
		for i in range(0,len(users_list),2):
			self.user_list_box.itemconfigure(i, background='#f0f0ff')
		#select the first one as default
		self.user_list_box.selection_set(0)
		
	#sure
	def bnt_user_manage_sure(self):
		self.destroy()
	
	#delete
	def bnt_user_manage_del(self):
		idxs = self.user_list_box.curselection()
		if len(idxs) == 1:
			selected_user = self.user_list_box.get(int(idxs[0]))
		
			if selected_user == 'admin':
				tkinter.messagebox.showinfo('警告', '不能删除该用户！')
			else:
				is_delete = tkinter.messagebox.askyesno(message = '确认删除该用户？', icon = 'question', title = 'ask')
				if is_delete == True:
					self.usrs_info.pop(selected_user)
					#rewrite the users file
					with open(self.master.master.login_userinfo_path, 'wb') as usr_file:
						pickle.dump(self.usrs_info, usr_file)
						#succeed delete
						tkinter.messagebox.showinfo('确认', '删除成功！')	
						self.user_list_box.delete(int(idxs[0]))
			
	#modify
	def bnt_user_modify(self):
		idxs = self.user_list_box.curselection()
		if len(idxs) == 1:
			selected_user = self.user_list_box.get(int(idxs[0]))
		
			if selected_user == 'admin':
				tkinter.messagebox.showinfo('警告', '不能修改该用户！')
			else:
				self.modify_win = NewPasswordPanel(self)						
					
	#set new pwd
	def bnt_set_new_pwd(self, new_pwd):
		idxs = self.user_list_box.curselection()
		if len(idxs) == 1:
			selected_user = self.user_list_box.get(int(idxs[0]))
			
			self.usrs_info[selected_user] = new_pwd
			#rewrite the users file
			with open(self.master.master.login_userinfo_path, 'wb') as usr_file:
				pickle.dump(self.usrs_info, usr_file)
				
############################################## panel for new password #################################
class NewPasswordPanel(Toplevel):
	def __init__(self, master = None):
		Toplevel.__init__(self, master)
		win_width = 307
		win_height = 120
		win_pos_x = self.winfo_screenwidth() // 2 - win_width // 2
		win_pos_y = (self.winfo_screenheight() - 100) // 2 - win_height // 2
		self.geometry('%sx%s+%s+%s' % (win_width, win_height, win_pos_x, win_pos_y))
		#mange gui init
		self.newpwd_win_int()	
		
	#gui init
	def newpwd_win_int(self):
		self.title('修改密码')
		self.gui_frame = ttk.Frame(self)		
		#row 0
		self.pwd_lbl = ttk.Label(self.gui_frame, text = '密码:')
		self.pwd_var = StringVar()
		self.pwd = ttk.Entry(self.gui_frame, textvariable = self.pwd_var)
		#row 1
		self.pwd_config_lbl = ttk.Label(self.gui_frame, text = '确认密码:')
		self.pwd_config_var = StringVar()
		self.pwd_config = ttk.Entry(self.gui_frame, textvariable = self.pwd_config_var)
		#row 2
		self.pwd_sure = ttk.Button(self.gui_frame, text = '确认', command = self.bnt_pwd_sure)
		self.pwd_cancel = ttk.Button(self.gui_frame, text = '取消', command = self.bnt_pwd_cancle)
		
		#grid widgets
		self.gui_frame.grid(column = 0, row = 0, padx = 10)
		#row 0
		self.pwd_lbl.grid(column = 0, row = 0, padx = 5, pady = 10)
		self.pwd.grid(column = 1, row = 0)
		#row 1
		self.pwd_config_lbl.grid(column = 0, row = 1, padx = 5)
		self.pwd_config.grid(column = 1, row = 1)
		#row 2
		self.pwd_sure.grid(column = 0, row = 2, padx = 15, pady = 10)
		self.pwd_cancel.grid(column = 1, row = 2)

	def bnt_pwd_sure(self):
		if self.pwd_var.get() == self.pwd_config_var.get():
			is_modify_pwd = tkinter.messagebox.askyesno(message = '确认修改密码？', icon = 'question', title = 'ask')
			if is_modify_pwd:
				self.master.bnt_set_new_pwd(self.pwd_var.get())
				self.destroy()
		else:
			tkinter.messagebox.showinfo("Warning", '两次密码不一致！')

	def bnt_pwd_cancle(self):
		self.destroy()	