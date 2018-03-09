#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' main panel '

__author__ = 'Lanbu'

from tkinter import *
import pickle
import tkinter.messagebox
import sqlite3
from SRF_sqlite import *



class MainPanel(Toplevel):
	#init
	def __init__(self, master = None):
		Toplevel.__init__(self, master)
		#connect sqlite
		self.finiancial_record = FinancialDataRecord()

	 