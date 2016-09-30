#!/usr/bin/python
# Script to read energy meter last reading
# 2016-09-27

import sys
import json
import time
import string
import datetime as dt
from datetime import datetime

####### User Variables
path = '/home/pi/projects/powerMonitoring/'
logfilepath = '/home/pi/project/powerMonitoring/logs/'		# log file directory
textfilepath = '/home/pi/projects/powerMonitoring/sample'	# text file to read from

####### End User Variables
filetimestamp = time.strftime("%Y-%m")
filename = logfilepath + 'logs/energy_' + filetimestamp + '.log'
FMT = "%Y-%m-%d %H:%M:%S"

####### Read the first line to get starting point for the month...only works if the file exists and there is data already in there
## Need to have a Try: thing I think...

try:
	a = open(filename, "r")
	first_line = a.readline().rstrip()
except OSerror as err:
	print "there is no fuckin file"
