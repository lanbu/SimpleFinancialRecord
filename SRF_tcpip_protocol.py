#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' tcpip communication protocol '

__author__ = 'Lanbu'

class selftocol():
	def __init__(self):
		#server to client
		self.packHead_server2client = b'server2client'
		self.packType_query_ack = b'\x00'
		self.packType_store_ack = b'\x01'
		
		#client to server
		self.packHead_client2server = b'client2server'		
		self.packType_query = b'\x00'
		self.packType_store = b'\x01'
		
		#common
		self.packHead_len = len(self.packHead_client2server)
		self.packType_pos = self.packHead_len
		self.packData_start_pos = self.packType_pos + 1
		
	#pack decode
	def pack_decode(self, data_stream):
		pack_head_b = recv_data[0:self.packHead_len]
		pack_type = recv_data[self.packHead_len]	
		
		if pack_head_b == self.packHead_client2server:	#pack head check		
			if pack_type == self.packType_query:		#pack type check -- ask for query
				self.pack_data = recv_data[self.packData_start_pos :].decode()
			
			elif pack_type == self.packType_store:	#pack type check -- ask for store
				self.pack_data = recv_data[self.packData_start_pos :].decode()
				print('store')
			else:
				print('error')
		else:
			print('head error')