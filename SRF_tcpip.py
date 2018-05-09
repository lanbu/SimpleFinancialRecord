#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' TCP/IP socket communication '

__author__ = 'Lanbu'

import socket
import pickle
import time, threading
from SRF_tcpip_protocol import *
from SRF_sqlite import *
import queue
import SRF_CommonDefine as commonDefine
import struct

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
				data = self.sock.recv(commonDefine.SOCKET_RECV_LEN)
				if len(data) != 0:
					#process the data
					proce_res = self.client_pack_process(data)
					if proce_res:
						#wait for the message from server task
						while self.from_server_queues[self.thread_id].empty():
							time.sleep(0.1)
						server_pack = self.from_server_queues[self.thread_id].get()	
						self.server_pack_process(server_pack)
					else:
						self.send_error_ack()
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
				store_queue = {}
				if res_info['pack_type'] == data_extract.packType_store:	#store
					store_queue['cmd'] = 'store'
				else:	#update
					store_queue['cmd'] = 'update'
					store_queue['record_no_old'] = res_info['record_no_old']
					res_info.pop('record_no_old')
				
				res_info.pop('head')
				res_info.pop('pack_type')
				
				store_queue['thread_id'] = self.thread_id
				store_queue['record'] = res_info
				self.to_server_queue.put(store_queue)
			elif res_info['pack_type'] == 'login':

				try:
					with open(commonDefine.LOGIN_USERINFO_PATH, 'rb') as usr_file:
						usrs_info = pickle.load(usr_file)
				except FileNotFoundError:
					with open(commonDefine.LOGIN_USERINFO_PATH, 'wb') as usr_file:
						usrs_info = {commonDefine.ADMINISTRATOR:commonDefine.ADMINISTRATOR_PWD}	#null dictionary			
						pickle.dump(usrs_info, usr_file)
					
				login_ack = {}
				login_ack['head'] = 'server2client'
				login_ack['pack_type'] = 'login_ack'
				
				if res_info['name'] in usrs_info:			
					if res_info['pwd'] == usrs_info[res_info['name']]:							
						login_ack['res'] = 'ok'
						
					else:
						login_ack['res'] = 'error'
						
					login_ack_b = data_extract.encode_dict_bytes(login_ack)
					self.sock.send(login_ack_b)
					self.sock.close()
			else:
				pass
				
			return True
		else:
			return False
			
	def server_pack_process(self, ser_pack):
		data_extract = TcpipProtocol()
		if ser_pack['cmd'] == 'query':
			ser_pack.pop('cmd')
			ser_pack['pack_type'] = data_extract.packType_query_ack
			ser_pack['head'] = data_extract.packHead_server2client
			ser_pack_encode = data_extract.pack_encode(ser_pack)
			#sock send data
			ser_pack_len = struct.pack('<L', len(ser_pack_encode))
			print(ser_pack_len + ser_pack_encode)
			self.sock.send(ser_pack_len + ser_pack_encode)
		elif ser_pack['cmd'] == 'store':
			ser_pack.pop('cmd')
			ser_pack['pack_type'] = data_extract.packType_store_ack
			ser_pack['head'] = data_extract.packHead_server2client
			ser_pack_encode = data_extract.pack_encode(ser_pack)
			#sock send data
			self.sock.send(ser_pack_encode)		
		elif ser_pack['cmd'] == 'update':
			ser_pack.pop('cmd')
			ser_pack['pack_type'] = data_extract.packType_update_ack
			ser_pack['head'] = data_extract.packHead_server2client
			ser_pack_encode = data_extract.pack_encode(ser_pack)
			#sock send data
			self.sock.send(ser_pack_encode)
		elif ser_pack['cmd'] == 'delete':
			ser_pack.pop('cmd')
			ser_pack['pack_type'] = data_extract.packType_del_ack
			ser_pack['head'] = data_extract.packHead_server2client
			ser_pack_encode = data_extract.pack_encode(ser_pack)
			#sock send data
			self.sock.send(ser_pack_encode)
			
	def send_error_ack(self):
		data_code = TcpipProtocol()
		error_ack = {}
		error_ack['head'] = data_code.packHead_server2client
		error_ack['pack_type'] = data_code.packType_error_ack
		
		error_ack_b = data_code.pack_encode(error_ack)
		#sock send data
		self.sock.send(error_ack_b)
		
############################################### tcpip client ################################################		
class TCPIP_client(threading.Thread):
	def __init__(self, ip_addr, ip_port, from_server_queue = None, to_server_queue = None):
		threading.Thread.__init__(self, daemon = True)
		self.from_serv_queue = from_server_queue
		self.to_serv_queue = to_server_queue		
		self.client_quit = False
		self.client_addr = (ip_addr, ip_port)
		self.c_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
	def run(self):
		#message loop
		while not self.client_quit:
			while self.from_serv_queue.empty():
				time.sleep(0.1)
			
			serv_pack = self.from_serv_queue.get()
			self.serv_pack_process(serv_pack)
	
	def serv_pack_process(self, server_pack = None):
		if server_pack != None:
			if server_pack['cmd'] == 'connect':
				connect_res = self.client_connect()
				connect_ack = {'cmd':'connect'}
				if connect_res:
					connect_ack['res'] = 'ok'
					tcpip_protocol = TcpipProtocol()
					record_info = {'head':'client2server', 'pack_type':'store', 'name':'admin', 'record_no':'124', 'date':'20180330', 'income':0, 'income_s':'', 'expense':0, 'expense_s':'', 'comment':''}	
					record_info_b = tcpip_protocol.encode_dict_bytes(record_info)
					self.client_send(record_info_b)
					#recv = self.client_recv()
					#print(recv)
				else:
					connect_ack['res'] = 'error'
			elif server_pack['cmd'] == 'store':
				pass
			elif server_pack['cmd'] == 'search':
				pass
			else:
				pass
				
	def client_connect(self):
		try:
			self.c_sock.connect(self.client_addr)
			return True
		except:
			#connect failed
			return False
			
	def client_send(self, send_data):
		try:
			self.c_sock.send(send_data)
			return True
		except:
			return False
			#send failed
	
	def client_recv(self):
		try:
			recv_data = self.c_sock.recv(1024)
		except:
			recv_data = False
		
		return recv_data