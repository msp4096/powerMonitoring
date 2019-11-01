#!/usr/bin/python
# Script to read energy meter last reading
# 2016-09-27
import os.path
import linecache
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
filename = path + '/logs/energy_' + filetimestamp + '.log'
FMT = "%Y-%m-%d %H:%M:%S"

####### Read the first line to get starting point for the month...or make a first line for the month in the else statment

if os.path.isfile(filename): #if the file exists it will do advanced calculations and add more info to the log file, first of month is limited data

	a = open(filename, "r")
	first_line = linecache.getline(filename, 1)
        print (first_line) 
	num_lines = sum(1 for line in a) 
	print(num_lines)
	last_line=linecache.getline(filename, num_lines-1)  #subtracted one from the total lines to fix an error...
	print (last_line + " this is the last line")
	a.close()

	first_line = first_line.split(',')
	first_line_time = first_line[0]
	first_line_meter = first_line[1]

	last_line = last_line.split(',')
	print (last_line)
	last_line_time = last_line[0]  #date and time
	print (last_line_time)
	last_line_meter = last_line[1]
	print (last_line_meter)

	current_time = datetime.now().strftime(FMT) #current time without microseconds

	last = datetime.strptime(last_line_time, FMT)
	current = datetime.strptime(current_time, FMT)
	tdelta = current - last
	tdelta = tdelta.total_seconds()

	####### Open and file and add a new line
	datafile = open(filename, "a", 1)
	timestamp = time.strftime(FMT)

	####### Get the latest meter reading and turn into kWh
	tfile = open ( path + 'reading')
	print (tfile)
	text = tfile.read()
	tfile.close()
	data = json.loads(text)
	kWh = float(data['Message']['Consumption']) / 100

	kWh_month_net = kWh - float(first_line_meter)
	if kWh_month_net > 2000 or kWh_month_net < -2000:
		kWh_month_net = kWh - float(first_line_meter) - 99999
	print (kWh_month_net)
	print (kWh)
	current_power_net = ((float(kWh) - float(last_line_meter)) / tdelta) * 3600.0 * 1000 # Power in Watts
	print (current_power_net)

	timestamp, _ = string.split(string.replace(data['Time'],'T',' '),'.')

	stamp = str(timestamp) + ',' + str('%.2f' % kWh) + ',' + str('%.2f' % current_power_net) + ',' + str(kWh_month_net) + '\n'

	datafile.write(stamp)
	datafile.close()
else: #if the file doesn't exist, it will create it and add only the starting kWh reading 
	####### Open and file and add a new line
	datafile = open(filename, "a", 1)
	timestamp = time.strftime(FMT)

	####### Get the latest meter reading and turn into kWh
	tfile = open ( path + 'reading')
	text = tfile.read()
	tfile.close()
	data = json.loads(text)
	kWh = float(data['Message']['Consumption']) / 100
	timestamp, _ = string.split(string.replace(data['Time'],'T',' '),'.')

	stamp = str(timestamp) + ',' + str('%.2f' % kWh) + '\n'

	datafile.write(stamp)
	datafile.close()
