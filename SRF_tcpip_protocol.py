#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' tcpip communication protocol '

__author__ = 'Lanbu'


#literal for user's record information
class UserRecordInfoLiteral():
	def __init__(self):
		self.usr_name_liter = 'name'
		self.record_date_liter = 'date'
		self.record_num_liter = 'record_no'
		self.record_income_liter = 'income'
		self.record_income_s_liter = 'income_s'
		self.record_expense_liter = 'expense'
		self.record_expense_s_liter = 'expense_s'
		self.record_remark_liter = 'comment'

class TcpipProtocol():
	def __init__(self):
		#server to client
		self.packHead_server2client = b'server2client'
		self.packType_query_ack = 1
		self.packType_store_ack = 1
		
		#client to server
		self.packHead_client2server = b'client2server'		
		self.packType_query = 0
		self.packType_store = 1
		
		#common
		self.packHead_len = len(self.packHead_client2server)
		self.packType_pos = self.packHead_len
		self.packData_start_pos = self.packType_pos + 1
		
	#pack decode
	def pack_decode(self, data_stream):
		decoded_pack = {}
		inf_literal = UserRecordInfoLiteral()
		
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
						pack_name_pos_start = pack_data_start + 2
						pack_name_pos_end = pack_name_pos_start + data_stream[pack_data_start + 1]
						pack_name = data_stream[pack_name_pos_start : pack_name_pos_end].decode()
						decoded_pack[inf_literal.usr_name_liter] = pack_name
						#record number
						pack_record_pos_start = pack_name_pos_end + 1
						pack_record_pos_end = data_stream[pack_name_pos_end] + pack_record_pos_start
						pack_recordno = data_stream[pack_record_pos_start : pack_record_pos_end].decode()
						decoded_pack[inf_literal.record_num_liter] = pack_recordno
					elif pack_type == self.packType_store:	#pack type check -- ask for store
						self.pack_data = data_stream[self.packData_start_pos :].decode()
						print('store')
					else:
						decoded_pack = False						
				else:
					decoded_pack = False
			else:
				decoded_pack = False
		else:
			decoded_pack = False
		
		#return decoded packet
		return decoded_pack