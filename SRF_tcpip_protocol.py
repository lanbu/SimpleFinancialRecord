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
		self.record_num_old_liter = 'record_no_old'

class TcpipProtocol():
	def __init__(self):
		#server to client
		self.packHead_server2client = 'server2client'
		self.packType_query_ack = 'query_ack'
		self.packType_store_ack = 'store_ack'
		self.packType_update_ack = 'update_ack'
		self.packType_del_ack = 'delete_ack'
		self.packType_error_ack = 'error_ack'
		
		#client to server
		self.packHead_client2server = 'client2server'		
		self.packType_query = 'query'
		self.packType_store = 'store'
		self.packType_update = 'update'
		self.packType_delete = 'delete'
				
	#pack decode
	def pack_decode(self, data_stream):
		usr_info_literal = UserRecordInfoLiteral()
		decoded_pack = self.decode_bytes_dict(data_stream)
		
		pack_head = decoded_pack.get('head')
		pack_type = decoded_pack.get('pack_type')
		if pack_head != None and pack_type != None:
			if pack_head == self.packHead_client2server:
				if pack_type == self.packType_query or pack_type == self.packType_delete:
					usr_name = decoded_pack.get(usr_info_literal.usr_name_liter)
					usr_record_no = decoded_pack.get(usr_info_literal.record_num_liter)
					if usr_name == None or usr_record_no == None:
						decoded_pack = None
				elif pack_type == self.packType_store or pack_type == self.packType_update:
					usr_name = decoded_pack.get(usr_info_literal.usr_name_liter)
					usr_record_no = decoded_pack.get(usr_info_literal.record_num_liter)
					usr_date = decoded_pack.get(usr_info_literal.record_date_liter)
					usr_income = decoded_pack.get(usr_info_literal.record_income_liter)
					usr_income_s = decoded_pack.get(usr_info_literal.record_income_s_liter)
					usr_expense = decoded_pack.get(usr_info_literal.record_expense_liter)
					usr_expense_s = decoded_pack.get(usr_info_literal.record_expense_s_liter)
					usr_remark = decoded_pack.get(usr_info_literal.record_remark_liter)
					if usr_name == None or usr_record_no == None or usr_date or usr_income or usr_income_s \
						or usr_expense or usr_expense_s or usr_remark:
						if pack_type == self.packType_update:
							usr_old_record_no = decoded_pack.get(usr_info_literal.record_num_old_liter)
							if usr_old_record_no == None:
								decoded_pack = None
				else:
					decoded_pack = None
		else:
			decoded_pack = None

			#return decoded packet
		return decoded_pack
		
	#pack encode
	def pack_encode(self, pack_data):
		encoded_data = self.encode_dict_bytes(pack_data)	
		
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