#!/bin/bash

/usr/local/bin/rtl_tcp &

sleep 3

PID=$!
#path="/home/pi/projects/powerMonitoring"
#logpath="/home/pi/projects/powerMonitoring/reading"
#meterid=4410055

/home/pi/projects/powerMonitoring/rtlamr -filterid=4410055 -logfile="/home/pi/projects/powerMonitoring/reading" -quiet -single=true -format="json"

python /home/pi/projects/powerMonitoring/energy_parse.py
kill -9 $PID

