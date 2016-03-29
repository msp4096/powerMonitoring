#!/usr/bin/python
# Script to read energy meter last reading
# 2014-03-21

import json
import time
import string

####### User Variables
path = '/home/pi/projects/powerMonitoring/'
logfilepath = '/home/pi/project/spowerMonitoring/logs/'		# log file directory
textfilepath = '/home/pi/projects/powerMonitoring/sample'	# text file to read from

####### End User Variables

filetimestamp = time.strftime("%Y-%m")
filename = path +  'logs/energy_' + filetimestamp + '.log'

datafile = open(filename, "a", 1)
timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

tfile = open(path+'reading')
text = tfile.read()
tfile.close()

data = json.loads(text)

kWh = float(data['Message']['Consumption']) / 100
timestamp, _ = string.split(string.replace(data['Time'],'T',' '),'.')
stamp = str(timestamp) + ',' + str('%.2f' % kWh) + '\n'

datafile.write(stamp)
datafile.close()




