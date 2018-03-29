#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' TCP/IP socket communication '

__author__ = 'Lanbu'

import socket
import time, threading
from SRF_tcpip_protocol import *
from SRF_sqlite import *
import queue

############################################# tcpip server ####################################################
class TCPIP_server(threading.Thread):
	def __init__(self, ip_addr = None, ip_port = None, ip_max_num = None, from_server_queues = None, to_server_queue = None):
		threading.Thread.__init__(self, daemon = True)
		#bind
		self.is_loop_ok	= True
		self.s_ip_addr = ip_addr
		self.s_ip_port = ip_port
		self.s_max_num = ip_max_num
		self.from_server_queues = from_server_queues
		self.to_server_queue = to_server_queue
		
	#server loop
	def run(self):
		#init server
		#create socket
		self.s_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s_server.bind((self.s_ip_addr, self.s_ip_port))
		self.s_server.listen(self.s_max_num)
		#loop
		while self.is_loop_ok:
			s_client, addr_client = self.s_server.accept()
			new_conn_thread = Server_connect_client(s_client, addr_client, self.from_server_queues, self.to_server_queue)
			new_conn_thread.start()
		self.s_server.close()
		
	#close server
	def server_close(self):
		self.is_loop_ok = False

		
class Server_connect_client(threading.Thread):
	def __init__(self, sock_client = None, addr_client = None, from_server_queues = None, to_server_queue = None):
		threading.Thread.__init__(self, daemon = True)
		self.sock = sock_client
		self.addr = addr_client
		self.from_server_queues = from_server_queues
		self.to_server_queue = to_server_queue
		self.is_disconnected = True
		self.pack_data = None
		#get threading id
		self.thread_id = threading.get_ident()
		self.from_server_queues[self.thread_id] = queue.Queue()
		
	def run(self):				
		while self.is_disconnected:
			try:
				data = self.sock.recv(1024)
				if len(data) != 0:
					#process the data
					self.client_pack_process(data)
					#wait for the message from server task
					while self.from_server_queues[self.thread_id].empty():
						time.sleep(0.1)
					server_pack = self.from_server_queues[self.thread_id].get()	
					self.server_pack_process(server_pack)
			except:
				self.sock.close()
				self.is_disconnected = False
				print('client disconnected')
				
	def client_pack_process(self, recv_data):
		data_extract = TcpipProtocol()
		res_info = data_extract.pack_decode(recv_data)

		if res_info != None:
			info_literal = UserRecordInfoLiteral()
			if res_info['pack_type'] == data_extract.packType_query or res_info['pack_type'] == data_extract.packType_delete:
				query_queue = {}
				
				if res_info['pack_type'] == data_extract.packType_query:	#query	
					query_queue['cmd'] = 'query'
				else:	#delete
					query_queue['cmd'] = 'delete'
					
				query_queue['thread_id'] = self.thread_id
				query_queue['name'] = res_info[info_literal.usr_name_liter]
				query_queue['record_no'] = res_info[info_literal.record_num_liter]				
				self.to_server_queue.put(query_queue)		
			elif res_info['pack_type'] == data_extract.packType_store or res_info['pack_type'] == data_extract.packType_update:
				res_info.pop('head')
				res_info.pop('pack_type')
				
				store_queue = {}
				if res_info['pack_type'] == data_extract.packType_store:	#store
					store_queue['cmd'] = 'store'
				else:	#update
					store_queue['cmd'] = 'update'
					store_queue['record_no_old'] = res_info['record_no_old']
					res_info.pop('record_no_old')
				
				store_queue['thread_id'] = self.thread_id
				store_queue['record'] = res_info
				self.to_server_queue.put(store_queue)
			else:
				pass
		else:
			print('pack error')
			
	def server_pack_process(self, ser_pack):
		data_extract = TcpipProtocol()
		if ser_pack['cmd'] == 'query':
			ser_pack.pop('cmd')
			ser_pack['pack_type'] = data_extract.packType_query_ack
			ser_pack['head'] = data_extract.packHead_server2client
			ser_pack_encode = data_extract.pack_encode(ser_pack)
			#sock send data
			self.sock.send(ser_pack_encode)
		elif ser_pack['cmd'] == 'store':
			ser_pack.pop('cmd')
			ser_pack['pack_type'] = ata_extract.packType_store_ack
			ser_pack['head'] = data_extract.packHead_server2client
			ser_pack_encode = data_extract.pack_encode(ser_pack)
			#sock send data
			self.sock.send(ser_pack_encode)
		elif ser_pack['cmd'] == 'update':
			ser_pack.pop('cmd')
			ser_pack['pack_type'] = ata_extract.packType_update_ack
			ser_pack['head'] = data_extract.packHead_server2client
			ser_pack_encode = data_extract.pack_encode(ser_pack)
			#sock send data
			self.sock.send(ser_pack_encode)
		elif ser_pack['cmd'] == 'delete':
			ser_pack.pop('cmd')
			ser_pack['pack_type'] = ata_extract.packType_del_ack
			ser_pack['head'] = data_extract.packHead_server2client
			ser_pack_encode = data_extract.pack_encode(ser_pack)
			#sock send data
			self.sock.send(ser_pack_encode)
############################################### tcpip client ################################################		
class TCPIP_client():
	def __init__(self, ip_addr, ip_port):
		self.client_addr = (ip_addr, ip_port)
		c_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
	def client_connect(self):
		try:
			c_sock.connect(self.client_addr)
		except:
			#connect failed
			pass
		finally:
			c_sock.close()
	def client_send(self, send_data):
		try:
			c_sock.send(send_data)
		except:
			pass
			#send failed