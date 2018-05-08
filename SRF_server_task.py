#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' server logic task'

__author__ = 'Lanbu'

import time, threading
from SRF_sqlite import *
from SRF_tcpip import *
import queue

class ServerLogic(threading.Thread):
	def __init__(self, gui_queue, server2gui_queue):
		threading.Thread.__init__(self, daemon = True)
		self.task_exit = False
		self.task_event = threading.Event()
		#for communication to main panel
		self.gui_queue = gui_queue
		self.server2gui_queue = server2gui_queue
		self.gui_oper_res = False
		#for communication to tcpip task
		self.to_sock_queues = {}
		self.from_sock_queue = queue.Queue()
		#sqlite init
		self.sqlite_records = FinancialDataRecord()
		#tcpip init
		self.tcpip_server = TCPIP_server(ip_addr = commonDefine.SOCKET_SERVER_IP, ip_port = commonDefine.SOCKET_SERVER_PORT, ip_max_num = 100, from_server_queues = self.to_sock_queues, to_server_queue = self.from_sock_queue)
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
					self.server2gui_queue.put({'cmd':'insert', 'res':'ok'})
				elif queue_message['cmd'] == 'query':
					queue_message.pop('cmd')
					query_res = self.sqlite_records.sql_query_one_record(queue_message['record_no'])
					
					if query_res == False:
						qres = {'cmd':'query', 'res':'error'}
					else:
						qres = {}
						qres['cmd'] = 'query'
						qres['res'] = 'ok'
						qres['records'] = query_res
					self.server2gui_queue.put(qres)
				elif queue_message['cmd'] == 'update':
					queue_message.pop('cmd')
					old_no = queue_message['old_no']
					queue_message.pop('old_no')
					self.sqlite_records.sql_update_one_record(old_no, queue_message)
				elif queue_message['cmd'] == 'delete':
					self.sqlite_records.delete_one_record(queue_message['record'])
				elif queue_message['cmd'] == 'profit_update':
					g_profit = self.sqlite_records.comput_profit()
					profit = {}
					profit['cmd'] = 'g_profit'
					profit['g_profit'] = g_profit
					self.server2gui_queue.put(profit)
			#message from tcpip socket
			if not self.from_sock_queue.empty():
				queue_message = self.from_sock_queue.get()
				
				#resolve the message
				if queue_message['cmd'] == 'query':
					query_res = self.sqlite_records.sql_query_one_record(queue_message['record_no'], queue_message['name'])
					
					query_queue = {}
					query_queue['cmd'] = 'query'
					if query_res == False:
						query_queue['res'] = 'none'
					else:
						query_queue['res'] = 'ok'
					
					query_queue['record'] = query_res
					self.to_sock_queues[queue_message['thread_id']].put(query_queue)
				elif queue_message['cmd'] == 'store':
					self.sqlite_records.sql_insert_one_record(queue_message['record'])
					store_queue = {}
					store_queue['cmd'] = 'store'
					store_queue['res'] = 'ok'
					self.to_sock_queues[queue_message['thread_id']].put(store_queue)
				elif queue_message['cmd'] == 'update':
					self.sqlite_records.sql_update_one_record(queue_message['record_no_old'], queue_message['record'])
					update_queue = {}
					update_queue['cmd'] = 'update'
					update_queue['res'] = 'ok'
					self.to_sock_queues[queue_message['thread_id']].put(update_queue)
				elif queue_message['cmd'] == 'delete':
					self.sqlite_records.delete_one_record(queue_message['record_no'], queue_message['name'])
					
					del_queue = {}
					del_queue['cmd'] = 'delete'
					del_queue['res'] = 'ok'
					self.to_sock_queues[queue_message['thread_id']].put(del_queue)
	def server_task_exit(self):
		self.task_exit = True
		self.tcpip_server.server_close()
		self.sqlite_records.close_sqlite()
