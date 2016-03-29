#!/usr/bin/python
import json

# Open and read the whole info.json file
with open('info.json') as data_file:
     data = json.load(data_file)

# grab specific json items
meter_id  = data['Meter_ID']
solar_key = data['Solar_Key']

print data       #print the whole json file
print meter_id   #print the meter_id value
print solar_key  #print the solar_key value
