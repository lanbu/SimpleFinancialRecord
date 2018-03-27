#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' server logic task'

__author__ = 'Lanbu'

import time, threading
from SRF_sqlite import *
from SRF_tcpip import *

class ServerLogic(threading.Thread):
	def __init__(self, gui_queue):
		threading.Thread.__init__(self, daemon = True)
		self.task_exit = False
		self.task_event = threading.Event()
		#for communication to main panel
		self.gui_queue = gui_queue
		self.gui_oper_res = False
		#sqlite init
		self.sqlite_records = FinancialDataRecord()
		#tcpip init
		self.tcpip_server = TCPIP_server(ip_addr = '127.0.0.1', ip_port = 9999, ip_max_num = 100)
		self.tcpip_server.start()
		
	def run(self):
		while not self.task_exit:
			if  not self.task_event.is_set():
				self.task_event.wait(0.01)
			#check if there are messages needed to be process in the queue
			#message from main panel
			self.gui_oper_res = False
			if not self.gui_queue.empty():				
				queue_message = self.gui_queue.get()
				
				#resolve the message
				if queue_message['cmd'] == 'insert':	
					queue_message.pop('cmd')
					self.sqlite_records.sql_insert_one_record(queue_message)
					self.gui_oper_res = True
				elif queue_message['cmd'] == 'query':
					queue_message.pop('cmd')
					pass
				elif queue_message['cmd'] == 'update':
					queue_message.pop('cmd')	
					pass
					
	def gui_oper_res_get(self):
		return self.gui_oper_res
		
	def server_task_exit(self):
		self.task_exit = True
		self.tcpip_server.server_close()
		self.sqlite_records.close_sqlite()
