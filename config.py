
# config.py - configuration defaults and phraser
#
# Contents
# --------
#
# DEFAULT_CONFIG
#		Empty configuration that is used to create a blank configuration file if
#		there is none.
#
# ac_config
#		Class that phrases the configuration file.


							 ### Import section ###

import os
from ConfigParser import ConfigParser


							   ### Constants ###

DEFAULT_CONFIG = """\
[list]
refresh_autorefresh = True
refresh_autorefreshdelay = 5
refresh_autorefreshevery = False

[connection]
mallogin_username = 
mallogin_password = 
mallogin_autologin = False

[ui]
tray_onclose = True
window_maximiseonstartup = False
tray_onstartup = False

[options]
ui_bars = list,edit
ui_barsvisible = list
other_runbefore = True
debug_verbosity = 0

[search_dirs]   # Directories where played files are searched for
dir1 = /home
dir2 = /home/foo
"""

ac_config_path = os.path.join(os.path.expanduser("~"), ".animecollector.cfg")


						   ### Class declarations ###

class ac_config(ConfigParser):
	""" Configuration phraser and data class.
	
	Properties
		mal = {'username':str, 'password':str, 'autologin':boolean}
	"""

	option_groups = None

	def __init__(self):
		""" Loads and reads the configuration file.  """

		ConfigParser.__init__(self)

		# Create default configuration if it is missing:
		if not os.path.isfile(ac_config_path):
			x = open(ac_config_path, 'w')
			x.write(DEFAULT_CONFIG)
			x.close()

		# Read configuration file:
		self.read(ac_config_path)

		##
		self.cfgdict = ConfigParser()
		self.cfgdict.read(ac_config_path)
		##

		self.mal = dict()
		self.mal['username'] = self.get('mal', 'username')
		self.mal['password'] = self.get('mal', 'password')
		self.mal['autologin'] = self.getboolean('mal', 'autologin')


		self.connection = { "mallogin": { 
				"username": None, "password": None, "autologin": None }}
		
		self.list = { "refresh" : {
				"autorefresh": None,
				"autorefreshevery": None, 
				"autorefreshdelay": None }}
		
		self.ui = { "tray": { "onStartup": None, "onClose": None },
					"window": { "maximiseOnStartup": None }}
		
		self.options = { "ui": { "bars": None, "barsVisible": None },
						 "debug": {"verbosity": None },
						 "other": {"runBefore": None }}

		self.option_groups = [[self.connection, "connection", True], 
							 [self.list, "list", True], 
							 [self.ui, "ui", True], 
							 [self.options, "options", False]]

		for opts in self.option_groups:
			for (name, group) in opts[0].iteritems():
				for (item, value) in group.iteritems():
					opts[0][name][item] = self.cfgdict.get(opts[1], name +
														"_" + item)

	def update(self):
		for opts in self.option_groups:
			for (name, group) in opts[0].iteritems():
				for (item, value) in group.iteritems():
					self.cfgdict.set(opts[1], name + "_" + item, opts[0][name][item])

	def write(self):
		configpath = open(ac_config_path, "w")
		self.cfgdict.write(configpath)