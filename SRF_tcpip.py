#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' TCP/IP socket communication '

__author__ = 'Lanbu'

import socket
import time, threading
from SRF_tcpip_protocol import *
from SRF_sqlite import *


############################################# tcpip server ####################################################
class TCPIP_server(threading.Thread):
	def __init__(self, ip_addr, ip_port, ip_max_num, sqlite_oper):
		threading.Thread.__init__(self, daemon = True)
		#bind
		self.is_loop_ok	= True
		self.s_ip_addr = ip_addr
		self.s_ip_port = ip_port
		self.s_max_num = ip_max_num
		self.sqlite_oper = sqlite_oper
		
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
			new_conn_thread = Server_connect_client(s_client, addr_client, self.sqlite_oper)
			new_conn_thread.start()
		self.s_server.close()
		
	#close server
	def server_close(self):
		self.is_loop_ok = False

		
class Server_connect_client(threading.Thread):
	def __init__(self, sock_client, addr_client, sqlite_oper):
		threading.Thread.__init__(self, daemon = True)
		self.sock = sock_client
		self.addr = addr_client
		self.is_disconnected = True
		self.pack_data = None
		self.sqlite_oper = sqlite_oper
		
	def run(self):		
		while self.is_disconnected:
			try:
				data = self.sock.recv(1024)
				if len(data) != 0:
					#process the data
					self.data_pack_process(data)
			except:
				self.sock.close()
				self.is_disconnected = False
				print('client disconnected')
				
	def data_pack_process(self, recv_data):
		data_extract = TcpipProtocol()
		res_info = data_extract.pack_decode(recv_data)
		
		if res_info != False:
			print(res_info)
		else:
			print('pack error')
		
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