#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "this modul is in charge of collecting config options and settings for starting program."#information describing the purpose of this prog
__status__ = "Development"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "4.0.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
__date__ = "2017"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = []#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



### use for exit()
### and can get prog_dir from it
import sys 

### specific modules
from commonz import platform
from commonz import logger
from commonz import config
from commonz.fs import checks
from commonz.fs import pathnames
from commonz.fs import actions

import app



### These variables needs to be hard coded
CFG_DIRECTORY="cfg"
LOGS_DIRECTORY="logs"
CACHE_DIRECTORY="cache"
DATA_DIRECTORY="data"

MSGS_FILE="msgs.txt"
CFG_FORMAT_FILE="format.yml"
CFG_SYSTEM_FILE="system.ini"
CFG_USER_FILE="user.ini"
LOG_FILE="logs.tsv"

PLATFORMS = ('linux','darwin','netbsd','freebsd','openbsd') # are the current supported OS platforms

### for the setup of sub directories additional identity can be used
### especially for windows os, because currently not working on linux
PROG_PUBLISHER= None # if set at None this feature will be ignored



### parsing files should not be integrated in this module
### because the prog have to decide later which mode to use for opening or writing files, 
### or which size of the memory buffer and prioritizing access, etc ...



def check_platform():
	"""verify that the current platform support the program"""
	### development focusing on specific os platforms may not work on others
	os_name=platform.get_os_name()
	if not os_name in PLATFORMS :
		logger.log_warning(1,(os_name))


def get_prog_dir():
	"""get path of the program directory"""
	start_file=__file__
	#start_file=sys.argv[0]
	#print(__file__,sys.argv[0])
	real_path=pathnames.get_real_path(start_file)
	src_path=pathnames.get_path(real_path)
	prog_path= pathnames.get_path(src_path)
	#print(start_file,real_path,src_path,prog_path)
	return prog_path

def get_log_dirs(parent_path,prog_name):
	"""get logs paths"""
	### high priority at the begin of the list
	### low  priority at the end of the list
	pathnames_list=[]
	pathnames_list.append( pathnames.get_log_dir(prog_name,PROG_PUBLISHER) )
	pathnames_list.append( pathnames.join_pathname(parent_path,LOGS_DIRECTORY) )
	#print(pathnames_list)
	return pathnames_list

def get_cache_dirs(parent_path,prog_name):
	"""get cache path"""
	### high priority at the begin of the list
	### low  priority at the end of the list
	pathnames_list=[]
	pathnames_list.append( pathnames.get_cache_dir(prog_name,PROG_PUBLISHER) )
	pathnames_list.append( pathnames.join_pathname(parent_path,CACHE_DIRECTORY) )
	#print(pathnames_list)
	return pathnames_list

def get_data_dirs(parent_path,prog_name):
	"""get data path"""
	### high priority at the begin of the list
	### low  priority at the end of the list
	### this directories contain unalterable program data
	pathnames_list=[]
	pathnames_list.extend( pathnames.get_data_dirs(prog_name,PROG_PUBLISHER) )
	pathnames_list.append( pathnames.join_pathname(parent_path,DATA_DIRECTORY) )
	#print(pathnames_list)
	return pathnames_list

def get_cfg_dirs(parent_dir,prog_name):
	"""get the cfg paths"""
	### high priority at the begin of the list
	### low  priority at the end of the list
	pathnames_list=[]
	pathnames_list.extend( pathnames.get_cfg_dirs(prog_name,PROG_PUBLISHER) )
	pathnames_list.append( pathnames.join_pathname(parent_dir,CFG_DIRECTORY) )
	#print(pathnames_list)
	return pathnames_list


def find_file(directories,file_name):
	"""get the log file path"""
	for directory in directories :
		fullpath= pathnames.join_pathname(directory,file_name)
		if checks.pathname(fullpath) :
			#print(fullpath)
			return fullpath


def set_logger(prog_name,msgsfile,syslog_verbosity,terminal_verbosity,logfile_verbosity,logfile):
	"""set the logs system"""
	#print(logfile)
	actions.create_directory(pathnames.get_path(logfile))
	logger.setup(prog_name,logfile,syslog_verbosity,terminal_verbosity,logfile_verbosity)
	logger.load_messages(msgsfile)
	logger.log_debug(2)


def get_prog_name():
	"""return the program name"""
	name = pathnames.get_base_name( pathnames.get_name(__file__) )
	#print(name)
	return name


def start(user_name,prog_name,cfg,dirs,env):
	"""start main activity"""
	logger.log_debug(3)
	a = app.Application(user_name,prog_name,cfg,dirs,env)
	exit_stat = a.run()
	return exit_stat

def finsih(exit_stat):
	"""finish the prog"""
	logger.log_debug(4)
	logger.shutdown()
	sys.exit(exit_stat)# 0 is the default exit code in case everything was ok, any nonzero value is considered “abnormal termination” by shells.



### This module should not be imported,
### otherwise the following important part will not be executed.
if __name__ == '__main__':
	"""start procedure"""
	
	env= platform.get_shell_env()

	user_name=platform.get_user_name()
	
	### prog_name used by: XDG directories; the set of name process; messages for syslogs;translate domain
	prog_name=get_prog_name()
	### the set of process name should be done by shell script
	### platform os may need to choose a special name for the process
	# set_name(prog_name)
	
	working_dir=pathnames.get_working_dir()
	home_dir=pathnames.get_home_dir()
	### get path of the program directory
	parent_dir=get_prog_dir()

	log_dirs=get_log_dirs(parent_dir,prog_name)
	cache_dirs=get_cache_dirs(parent_dir,prog_name)
	data_dirs=get_data_dirs(parent_dir,prog_name)
	cfg_dirs=get_cfg_dirs(parent_dir,prog_name)
	
	default_cfg_file=find_file(cfg_dirs,CFG_FORMAT_FILE)
	cfg_parser=config.Config()
	cfg_parser.read_format(default_cfg_file)
	cfg=cfg_parser.get()
	local=cfg['SYSTEM']['local']
	### if local True, will not use files outside program directory
	if local :
		log_dirs= [log_dirs[-1]]
		cache_dirs= [cache_dirs[-1]]
		data_dirs= [data_dirs[-1]]
	else :
		system_cfg_file=find_file(cfg_dirs,CFG_SYSTEM_FILE)
		user_cfg_file=find_file(cfg_dirs,CFG_USER_FILE)
		cfg_file_list=list(filter(None,[system_cfg_file,user_cfg_file]))# remove None from the list
		if cfg_file_list :# if list not empty
			#print(cfg_file_list)
			cfg_parser.read_configfiles(cfg_file_list)
			cfg=cfg_parser.get()
	dirs={'cwd':working_dir,'home':home_dir,'cache':cache_dirs[0],'data':data_dirs}
	
	msgsfile= find_file(data_dirs,MSGS_FILE)
	logfile= pathnames.join_pathname(log_dirs[0],LOG_FILE)
	cfg_logs= cfg['VERBOSITY']
	set_logger(prog_name,msgsfile,cfg_logs['syslog'],cfg_logs['terminal'],cfg_logs['logfile'],logfile)
	
	check_platform() # here because want setup the logs system first
	
	exit_stat=start(user_name,prog_name,cfg,dirs,env)
	
	finsih(exit_stat)

