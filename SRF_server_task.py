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
		self.gui_queue = gui_queue
		#sqlite init
		self.sqlite_records = FinancialDataRecord()
		#tcpip init
		self.tcpip_server = TCPIP_server(ip_addr = '127.0.0.1', ip_port = 9999, ip_max_num = 100)
		self.tcpip_server.start()
		
		
	def run(self):
		self.gui_queue.put('hello')
		print(self.gui_queue.get())

	def server_task_exit(self):
		self.tcpip_server.server_close()
		self.sqlite_records.close_sqlite()
