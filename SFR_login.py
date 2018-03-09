#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' login dialog '

__author__ = 'Lanbu'

from tkinter import *
import pickle
import tkinter.messagebox
from SRF_mainPanel import *

#login window class
class Login(Tk):
	def __init__(self):
		Tk.__init__(self)
		self.login_pic_path = './pictures/login.gif'
		self.login_userinfo_path = 'usrs_info.pickle'
		self.login_usrinfo_default_path = 'usrs_info_defaul.pickle'
		self.administor_name = 'admin'
		self.administor_pwd = 'ImAdmin'
		#window parameters init
		self.title('Login')
		#central display
		win_width = 450
		win_height = 300
		win_pos_x = self.winfo_screenwidth() // 2 - win_width // 2
		win_pos_y = (self.winfo_screenheight() - 100) // 2 - win_height // 2
		self.geometry('%sx%s+%s+%s' % (win_width, win_height, win_pos_x, win_pos_y))
		self.login_init()
		self.login_default_info()
			
	def login_init(self):
		#welcome image
		self.canvas = Canvas(self, height = 200, width = 500)
		self.image_file = PhotoImage(file = self.login_pic_path)
		image = self.canvas.create_image(0, 0, anchor = 'nw', image = self.image_file)
		self.canvas.pack(side = 'top')
		#user information
		#set label
		Label(self, text = 'User name:').place(x = 50, y = 150)
		Label(self, text = 'Password:').place(x = 50, y = 190)		
		#login user name input
		self.var_usr_name = StringVar()
		entry_usr_name = Entry(self, textvariable = self.var_usr_name)
		entry_usr_name.place(x = 160, y = 150)
		#login user password input
		self.var_usr_pwd = StringVar()
		entry_usr_pwd = Entry(self, textvariable = self.var_usr_pwd, show = '*')
		entry_usr_pwd.place(x = 160, y = 190)
		#login and sign up button
		bnt_login = Button(self, text = 'Login', comman = self.usr_login)
		bnt_login.place(x = 170, y = 230)
		bnt_sign_up = Button(self, text = 'Add New', command = self.usr_sign_up)
		bnt_sign_up.place(x = 270, y = 230)	
		#create a new user information file
		try:
			open(self.login_userinfo_path, 'rb')
		except FileNotFoundError:
			with open(self.login_userinfo_path, 'wb') as usr_file:
				usrs_info = {self.administor_name:self.administor_pwd}	#default dictionary			
				pickle.dump(usrs_info, usr_file)
		
	#reset the login information after sign up
	def reset_login_info(self, new_user_name):
		self.var_usr_name.set(new_user_name)
		self.var_usr_pwd.set('')
		
	#default login information displayed in the entry
	def login_default_info(self, default_info = None):
		if not default_info:
			try:
				with open(self.login_usrinfo_default_path, 'rb') as usr_file:
					usr_info = pickle.load(usr_file)
					if usr_info:
						self.var_usr_name.set(usr_info[0])
						self.var_usr_pwd.set(usr_info[1])
			except FileNotFoundError:
				with open(self.login_usrinfo_default_path, 'wb') as usr_file:
					usr_info = []
					pickle.dump(usr_info, usr_file)	
		else:
			with open(self.login_usrinfo_default_path, 'wb') as usr_file:
				pickle.dump(default_info, usr_file)
				
	#user login
	def usr_login(self):
		self.usr_name = self.var_usr_name.get()
		self.usr_pwd = self.var_usr_pwd.get()
		
		try:
			with open(self.login_userinfo_path, 'rb') as usr_file:
				usrs_info = pickle.load(usr_file)
		except FileNotFoundError:
			with open(self.login_userinfo_path, 'wb') as usr_file:
				usrs_info = {self.administor_name:self.administor_pwd}	#null dictionary			
				pickle.dump(usrs_info, usr_file)
				
		if self.usr_name != '' and self.usr_name in usrs_info:			
			if self.usr_pwd == usrs_info[self.usr_name]:
				default_info = []
				default_info.append(self.usr_name)
				default_info.append(self.usr_pwd)
				
				self.login_default_info(default_info)
				#tkinter.messagebox.showinfo(title = 'Welcome', message = 'how are you?' + self.usr_name)
				self.mainPanel = MainPanel(self)
			else:
				tkinter.messagebox.showerror(message = 'Error, your password is wrong!')
		
	#user sign up
	def usr_sign_up(self):
		self.usr_name = self.var_usr_name.get()
		self.usr_pwd = self.var_usr_pwd.get()
		if self.usr_name == self.administor_name and self.usr_pwd == self.administor_pwd:
			self.signin_win = SignIn(self, self.login_userinfo_path)
		else:
			tkinter.messagebox.showinfo(title = 'Notice', message = 'Sorry! You are not Administrator.')
	
#sign in window class
class SignIn(Toplevel):
	def __init__(self, master = None, login_userInfo_path = None):
		Toplevel.__init__(self, master)
		self.login_userInfo_path = login_userInfo_path
		self.title('Sign In')
		#sign in window geometry
		win_width = 350
		win_height = 200
		win_pos_x = self.winfo_screenwidth() // 2 - win_width // 2
		win_pos_y = (self.winfo_screenheight() - 100) // 2 - win_height // 2		
		self.geometry('%sx%s+%s+%s' % (win_width, win_height, win_pos_x, win_pos_y))
		self.sign_in_win()
		
	def sign_in_win(self):
		#sign in name
		Label(self, text = 'User name').place(x = 10, y = 10)
		self.sign_name_var = StringVar()
		sign_name_entry = Entry(self, textvariable = self.sign_name_var)
		sign_name_entry.place(x = 150, y = 10)
		#sign in password
		Label(self, text = 'Password').place(x = 10, y = 50)
		self.sign_pwd_var = StringVar()
		sign_pwd_entry = Entry(self, textvariable = self.sign_pwd_var)
		sign_pwd_entry.place(x = 150, y = 50)
		#sign in password confirm
		Label(self, text = 'Confirm Password').place(x = 10, y = 90)
		self.sign_pwd_confi_var = StringVar()
		sign_pwd_confi_entry = Entry(self, textvariable = self.sign_pwd_confi_var)
		sign_pwd_confi_entry.place(x = 150, y = 90)
		#sign in button
		sign_confirm_bnt = Button(self, text = 'Sign Up', command = self.sign_up_callback)
		sign_confirm_bnt.place(x = 150, y = 130)
		#sign in cancel button
		sign_cancel_bnt = Button(self, text = 'Cancel', command = self.sign_cancel_callback)
		sign_cancel_bnt.place(x = 250, y = 130)
		
	def sign_up_callback(self):
		new_pwd = self.sign_pwd_var.get()
		new_pwd_confirm = self.sign_pwd_confi_var.get()
		new_name = self.sign_name_var.get()
		
		if new_name != '' and new_pwd != '' and new_pwd_confirm != '':		
			with open(self.login_userInfo_path, 'rb') as usr_file:
				exist_usr_info = pickle.load(usr_file)
			if 	new_pwd != new_pwd_confirm:
				tkinter.messagebox.showerror('Error', 'Password and confirm password must be the same')
				#lift the sign up window to the top
				self.lift(self.master)
			elif new_name in exist_usr_info:
				tkinter.messagebox.showerror('Error', 'The user has already signed up')
				#lift the sign up window to the top
				self.lift(self.master)
			else:
				exist_usr_info[new_name] = new_pwd
				with open(self.login_userInfo_path, 'wb') as usr_file:
					pickle.dump(exist_usr_info, usr_file)
				tkinter.messagebox.showinfo('welcome', 'Succeed Signed Up')
				self.master.reset_login_info(self.sign_name_var.get())
				self.destroy()
		else:	
			tkinter.messagebox.showinfo('Warning', 'Illegal Input')
			#lift the sign up window to the top
			self.lift(self.master)	
	def sign_cancel_callback(self):		
		self.destroy()
		
# main		
if __name__ == '__main__':
	app_login = Login()		
	
	app_login.mainloop()