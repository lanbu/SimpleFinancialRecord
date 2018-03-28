#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' tcpip communication protocol '

__author__ = 'Lanbu'

import json

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
		self.packHead_server2client = 'server2client'
		self.packType_query_ack = 'query_ack'
		self.packType_store_ack = 'store_ack'
		
		#client to server
		self.packHead_client2server = 'client2server'		
		self.packType_query = 'query'
		self.packType_store = 'store'
		
	#pack decode
	def pack_decode(self, data_stream):
		usr_info_literal = UserRecordInfoLiteral()
		decoded_pack = self.decode_bytes_dict(data_stream)
		
		pack_head = decoded_pack.get('head')
		pack_type = decoded_pack.get('pack_type')
		if pack_head != None and pack_type != None:
			if pack_head == self.packHead_client2server:
				if pack_type == self.packType_query:
					usr_name = decoded_pack.get(usr_info_literal.usr_name_liter)
					usr_record_no = decoded_pack.get(usr_info_literal.record_num_liter)
					if usr_name == None or usr_record_no == None:
						decoded_pack = None
				elif pack_type == self.packType_store:
					pass
		else:
			decoded_pack = None

			#return decoded packet
		return decoded_pack
		
	#pack encode
	def pack_encode(self, pack_data):
		inf_literal = UserRecordInfoLiteral()
		encoded_data = self.packHead_server2client.encode()
		
		if pack_data != False:
			
			#name
			pack_data[inf_literal.usr_name_liter]
		else:
			pass 
			
		return encoded_data	
			

	#encode: dictionary --> bytes
	def encode_dict_bytes(self, dat_dict):
		#dict --> json
		dat_json = json.JSONEncoder().encode(dat_dict)
		#json --> string
		dat_str = json.dumps(dat_json)
		#string --> bytes
		dat_bytes = dat_str.encode()
	
		return dat_bytes
			
	#decode: bytes --> dictionary
	def decode_bytes_dict(self, dat_bytes):
		#bytes --> string
		dat_str = dat_bytes.decode()
		#string --> json
		dat_json = json.loads(dat_str)
		#json --> dictionary
		dat_dict = json.JSONDecoder().decode(dat_json)

		return dat_dict