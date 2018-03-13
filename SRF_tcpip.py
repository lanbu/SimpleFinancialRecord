#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' TCP/IP socket communication '

__author__ = 'Lanbu'

import socket
import time, threading


class tcpip_server():
	def __init__(self, ip_addr, ip_port, ip_max_num):
		#bind
		self.is_loop_ok	= True
		self.s_ip_addr = ip_addr
		self.s_ip_port = ip_port
		self.s_max_num = ip_max_num
	
	#init server
	def server_init(self):
		t_server = threading.Thread(target = self.server_loop, name = 'serverLoop')
		t_server.start()
		t_server.join()
		
	#server loop
	def server_loop(self):
		#init server
		#create socket
		self.s_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s_server.bind((self.s_ip_addr, self.s_ip_port))
		self.s_server.listen(self.s_max_num)
		#loop
		while self.is_loop_ok:
			self.s_client, self.addr_client = self.s_server.accept()
			t = threading.Thread(target = self.sc_linked_loop, args = (self.s_client, self.addr_client))
			t.start()		
		self.s_server.close()
	
	#loop function for server linked with client
	def	sc_linked_loop(self, sock, addr):
		try:
			data = sock.recv()
			#process the data
		finally:
			sock.close()
	
	#close server
	def server_close(self):
		self.is_loop_ok = False
		
		
class tcpip_client():
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
			#send failed