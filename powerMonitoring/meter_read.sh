#!/bin/bash

/usr/local/bin/rtl_tcp &

sleep 3

PID=$!
#path="/home/pi/powerMonitoring"
#logpath="/home/pi/powerMonitoring/reading"
#meterid=4410055

/home/pi/powerMonitoring/rtlamr -filterid=4410055 -logfile="/home/pi/powerMonitoring/reading" -quiet -single=true -format="json"

python /home/pi/powerMonitoring/energy_parse.py
kill -9 $PID

