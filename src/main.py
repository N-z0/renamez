#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "This is the program centerpiece,but need to be imported by other modules to be used"#information describing the purpose of this module
__status__ = "Development"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "3.0.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
__date__ = "2017"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = []#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



### import the required modules
from commonz.convert import text



CONTROL_CHAR= '\x07\x0b\x09\x0a\x0d\x7f\x08\x1b\x0c\x1b'
SYSTEM_CHAR="/\:*<>|.~"
QUOTE_CHAR="'"
DOUBLE_QUOTE_CHAR='"'

SUBSTITUTE_SPACE='_'
SUBSTITUTE_DOT='-'

### Misc
#import random
#import string # chain of char manipulation
#import collections	# provide alternatives specialized datatypes (dict, list, set, and tupl) ex: deque>list-like container with fast appends and pops on either end
#from collections import deque # storage de queue de données
#import urllib # open a URL the same way you open a local file

### asynchron
#import asyncio #provides the basic infrastructure for writing asynchronous programs.
#import threading # constructs higher-level threading interfaces
#import queue  #when information must be exchanged safely between multiple threads.
#import signal #Set handlers for asynchronous events
#import select # is low level module,Users are encouraged to use the selectors module instead
#import selectors # built upon the select module,allows high-level I/O multiplexing
#import asyncio# built upon selectors
#import multiprocessing

class Main():
	"""main software application as object"""
	
	def __init__(self):
		"""initialization of the application"""
		pass
	
	
	def get_correct_name(self,old_name,old_ext_names,cfg,sp_char):
		#print(base_name,ext_names,max_ext)
		uncode=cfg["uncode"]
		ascii_only=cfg["ascii"]
		spaces=cfg["spaces"]
		case=cfg["case"]
		strip_list=cfg["strip"]
		merge_list=cfg["merge"]
		eraze_list=cfg["eraze"]
		convert_tabl=cfg["conv"]
		max_dots=cfg["ext"]
		convert_ext_tabl=cfg["conv_ext"]
		
		names_list= self.undots(old_name,old_ext_names,max_dots)
		#print(names_list)
		names_qantum=len(names_list)
		for name_index in range(names_qantum) :
			name=None
			new_name=names_list[name_index]
			if uncode :
				new_name=self.uncode(new_name)
			while not new_name==name :
				name=new_name
				new_name=self.normalize(new_name,sp_char)
				if ascii_only :
					new_name=self.ascii(new_name)
				if not spaces :
					new_name=self.unspaces(new_name)
				if case!=0 :
					new_name=self.set_case(new_name,case)
				if strip_list!=() :
					new_name=self.strip(new_name,strip_list)
				if merge_list!=() :
					new_name=self.merge(new_name,merge_list)
				if eraze_list!=() :
					new_name=self.eraze(new_name,eraze_list)
				if convert_tabl!={} :
					new_name=self.convert(new_name,convert_tabl)
			names_list[name_index]=new_name

		if convert_ext_tabl and names_qantum>1 :
			for ext_index in range(1,names_qantum-1) :
				ext_name=names_list[ext_index]
				new_ext_name=self.convert(ext_name,convert_ext_tabl)
				names_list[ext_index]=new_ext_name
		
		return names_list


	def undots(self,base_name,ext_names,max_ext):
		"""allow a certain number of .ext and merge the others"""
		#print(base_name,ext_names,max_ext)
		ext_quantum=len(ext_names)
		if ext_quantum==0 :
			return [base_name]
		elif max_ext==-1 :
			return [base_name]+ext_names
		elif max_ext==0 :
			return [SUBSTITUTE_DOT.join([base_name]+ext_names)]
		else :
			if ext_quantum>max_ext :
				base_name=SUBSTITUTE_DOT.join([base_name]+ext_names[:0-max_ext])
				ext_names=ext_names[0-max_ext:]
				return [base_name]+ext_names
			else :
				return [base_name]+ext_names


	def uncode(self,name):
		"""decode URL special characters"""
		return text.decode_url(name)
	
	
	def ascii(self,name):
		"""Replace special accents characters by their closest ASCII equivalents"""
		return text.to_ascii(name)
	
	
	def unspaces(self,name):
		"""replace blank space by _"""
		name=name.replace(' ',SUBSTITUTE_SPACE)
		return name


	def set_case(self,name,change):
		"""switch caracteres case (1=upper,-1=lower,0=no change)"""
		if change>0 :
			new_name=name.upper()
		elif change<0 :
			new_name=name.lower()
		else :
			new_name=name
		return new_name


	def strip(self,name,strip_list):
		"""delete the specified characters if name beginning or ending with"""
		new_name=name
		while True :
			for s in strip_list :
				new_name=new_name.strip(s)
			if name==new_name :
				break
			else :
				name=new_name
		return new_name


	def merge(self,name,merge_list):
		"""merge the specified characters"""
		new_name=name
		while True :
			for s in merge_list:
				new_name=new_name.replace(s+s,s)
			if name==new_name :
				break
			else :
				name=new_name
		return new_name


	def eraze(self,name,eraze_list):
		"""remove the specified characters"""
		new_name=name
		while True :
			for s in eraze_list :
				new_name=new_name.replace(s,'')
			if name==new_name :
				break
			else :
				name=new_name
		return new_name


	def convert(self,name,convert_tabl):
		"""convert the specific characters by other characters"""
		new_name=name
		while True :
			for n in convert_tabl :
				for o in convert_tabl[n] :
					new_name=new_name.replace(o,n)
			if name==new_name :
				break
			else :
				name=new_name
		return new_name

	
	def normalize(self,name,sp_char):
		"""substitute special system characters"""
		bad_chars=CONTROL_CHAR+SYSTEM_CHAR+QUOTE_CHAR+DOUBLE_QUOTE_CHAR
		for c in bad_chars :
			name=name.replace(c,sp_char)
			#print(name)
		return name

