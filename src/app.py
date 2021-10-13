#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "provide a user interface for the main module."#information describing the purpose of this module
__status__ = "Development"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "3.0.2"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
__date__ = "2017"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = []#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



### import the required modules

import os # use for exit status and path

### for output messages to logs systems
from commonz import logger
from commonz.fs import pathnames,checks,actions
from commonz.io import tty

### 
import main



### The same log message can be used in many cases with different variables
### here can be displayed a larger part of the complete lines.
LOG1='Not Existing: {}'
LOG2='Working On: {} {}'
LOG3='New Name: {}'
LOG4='Output Mode: {}'
LOG5='A file or directory with the same name already exists : {}'
LOG6='Mode unknow: {}'
LOG7='Not a file Not a directory: {}'

MODE_CHECK='check'
MODE_RETURN='return'
MODE_WRITE='write'

CMD_PIPE_ARG='-'# use for a specifie input or output args by pipe

### conversion string format :
### things betwins CONV_OR are remplaced by the thing next to CONV_PUT
### and the delimiter CONV_SEP are the separator between inline conversion requests
CONV_OR='|'
CONV_SEP="'"
CONV_PUT='/'



class Application():
	"""main software application as object"""
	def __init__(self,user_name,prog_name,cfg,dirs,env):
		"""initialization of the application"""
		self.exit_stat=os.EX_OK
		
		### setup names
		self.prog_name=prog_name
		self.user_name=user_name
		
		### setup path
		self.working_dir=dirs['cwd']
		self.home_dir=dirs['home']
		self.cache_dir=dirs['cache']
		self.data_dir= dirs['data']
		
		### store configuration settings parameters
		#print(cfg)
		#self.cfg= cfg
		self.pathname= cfg['ARG']['pathname']
		self.mode= cfg['APPLICATION']['mode']
		self.sp_conv= cfg['APPLICATION']['sp_conv']
		self.type= cfg['APPLICATION']['type']
		self.cfg= {}
		self.cfg[checks.TYPE_DIRECTORY]=cfg['DIRECTORIES']
		self.cfg[checks.TYPE_FILE]=cfg['FILES']
		for tip_index in self.cfg :
			for conv_index in ("conv","conv_ext") :
					conv={}
					code=self.cfg[tip_index][conv_index]
					if code :
						for seq in code.split(CONV_SEP) :
							#print("seq: ",seq)
							combo=seq.split(CONV_PUT)
							#print("combo: ",combo)
							olds=combo[0].split(CONV_OR)
							new=combo[1]
							#print("for: {} set: {}".format(olds,new))
							if new in conv :
								conv[new]+=olds
							else :
								conv[new]=olds
					self.cfg[tip_index][conv_index]=conv
					#print(self.cfg[tip_index][conv_index])
	
	
	def set_exit_stat(self,new_exit_stat):
		if self.exit_stat==os.EX_OK :
			self.exit_stat=new_exit_stat
	
	
	def run(self):
		"""operates the software object"""		
		if self.pathname==CMD_PIPE_ARG :
			while True :
				pathname = tty.read_pipe_input()
				if pathname :
					self.proceed(pathname)
				else :
					break
		else :
			self.proceed(self.pathname)
		return self.exit_stat
	
	
	def proceed(self,pathname):
		"""operate on one pathname"""
		if not checks.pathname(pathname) and self.type=="auto" :
			logger.log_error(LOG1.format(pathname))
			self.set_exit_stat(os.EX_NOINPUT) # input file did not exist or was not readable.
		else :
			
			path=pathnames.get_path(pathname)
			if self.type=="file" :
				tip=checks.TYPE_FILE
			elif self.type=="folder" :
				tip=checks.TYPE_DIRECTORY
			else :
				### self.type=="auto"
				tip=checks.get_type(pathname)
				
			if not tip in (checks.TYPE_FILE,checks.TYPE_DIRECTORY) :
				logger.log_error(LOG7.format(pathname))
				self.set_exit_stat(os.EX_DATAERR) # the input data was incorrect.
			else :
				
				full_name=pathnames.get_name(pathname)
				#print(full_name)
				exts_names=[ext for ext in pathnames.get_name_ext(pathname) if ext ]
				#print(exts_names)
				base_name=pathnames.get_base_name(pathname)
				#print(base_name)
				logger.log_info(LOG2.format(tip,full_name))
				cfg_tip=self.cfg[tip]
				renamer=main.Main()
				new_names=renamer.get_correct_name(base_name,exts_names,cfg_tip,self.sp_conv)
				new_name=pathnames.join_base_name_ext(new_names[0],new_names[1:])
				logger.log_info(LOG3.format(new_name))
				logger.log_info(LOG4.format(self.mode))
				if self.mode==MODE_CHECK :
					if not new_name==full_name :
						tty.print_info(pathname)
				elif self.mode==MODE_RETURN :
					tty.print_info(new_name)
				elif self.mode==MODE_WRITE :
					if not new_name==full_name :
						try :
							### must start by changing the name of the files, otherwise problem with new folders names
							actions.rename(path,full_name,new_name)
						except FileExistsError :
							logger.log_error( LOG5.format(pathnames.join_pathname(path,new_name)) )
							self.set_exit_stat(os.EX_CANTCREAT) # a user specified output file could not be created.
				else :
					logger.log_error( LOG6.format(self.mode) )
					self.set_exit_stat(os.EX_USAGE) # the command was used incorrectly, such as when the wrong number of arguments are given.
