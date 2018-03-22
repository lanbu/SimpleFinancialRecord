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
		if len(data_stream) > (self.packHead_len + 2):
			#packet head
			pack_head_b = data_stream[0:self.packHead_len]
			if pack_head_b == self.packHead_client2server:	#pack head check
				#packet length
				pack_data_len = 0
				pack_data_len = data_stream[self.packHead_len]
				pack_data_len <<= 8
				pack_data_len += data_stream[self.packHead_len + 1]
				
				if pack_data_len > 0:		
					#packet type	
					pack_data_start = self.packHead_len + 2
					pack_type = data_stream[pack_data_start]			
					if pack_type == self.packType_query:		#pack type check -- ask for query
						#name
						pack_name_pos_start = pack_data_start + 1
						pack_name_pos_end = pack_data_start + data_stream[pack_data_start + 1] + 1
						self.pack_name = data_stream[pack_name_pos_start : pack_name_pos_end].decode()
						#record number
						pack_record_pos_start = pack_name_pos_end + 1
						pack_record_pos_end = data_stream[pack_name_pos_end] + pack_record_pos_start + 1
						self pack_recordno = data_stream[pack_record_pos_start : pack_record_pos_end].decode()
					elif pack_type == self.packType_store:	#pack type check -- ask for store
						self.pack_data = data_stream[self.packData_start_pos :].decode()
						print('store')
					else:
						print('error')
