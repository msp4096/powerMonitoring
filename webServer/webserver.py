#!/usr/bin/python3

from wsgiref.simple_server import make_server
import time
import json
import urllib.request as urllib2, json
import sys
from sense_hat import SenseHat
import pingNet
import os
import os.path
import keys
#import picamera

# ------ User settings -------
portNumber = 81

print('User settings imported')

#Get time
def get_current_time():
    print('time...')
    current_time = time.strftime('%H:%M:%S')
    print(current_time)
    return current_time

#Get solar power data from the SolarEdge API
def get_solar():
    print('solar...')
    try:
        with urllib2.urlopen(keys.api_solar_url) as urla:
            a = json.loads(urla.read().decode())
            print(a)
        with urllib2.urlopen(keys.api_solar_nana_url) as urlb:
            b = json.loads(urlb.read().decode())
            print(b)
    except:
        print("Failed to get solar")
        return False
    return (a,b)

#Get the current weather conditions
def get_conditions():
    print('weather...')
    try:
        with urllib2.urlopen(keys.api_conditions_url) as url:
            f = json.loads(url.read().decode())
    except:
        print("Failed to get conditions")
        return False
    outside_conditions = f
    temp_k = outside_conditions['main']['temp']
    wind_speed = outside_conditions['wind']['speed']
    temp_F = round((temp_k-273.0) * 9.0 /5.0 +32.0, 2)
    print(temp_F)
    print(wind_speed)
    return f

#Get current information from the log file
def get_kWh():
    print('kWh meter...')
    path = '/home/pi/projects/powerMonitoring/logs/'
    fileTS = time.strftime("%Y-%m")
    tfile = path + 'energy_' + fileTS + '.log'
    if os.path.isfile(tfile):
        tfile = open(tfile)
        lines = tfile.readlines()
        if lines:
            first_line = str(lines[0].rstrip())
            last_line = str(lines[-1].rstrip())
        tfile.close()
        first_line = first_line.split(',')
        last_line  = last_line.split(',')
        print(first_line)
        print(last_line)
        kWh = last_line[1]
        netuse = last_line[3]
        pwr = last_line[2]
        print(kWh, netuse, pwr)
    else:
        kWh = 0
        netuse = 0
        pwr = 0
    return (kWh, netuse, pwr)

#start the server and get values when page is refreshed
def application(environ, start_response):

    print('Application started')
    print(environ['PATH_INFO'])

    #solar stuff
    solara, solarb = get_solar()
    try:
        currentPowera = solara['sitesOverviews']['siteEnergyList'][0]['siteOverview']['currentPower']['power']
        DayProductiona = solara['sitesOverviews']['siteEnergyList'][0]['siteOverview']['lastDayData']['energy']
        MonthProductiona = solara['sitesOverviews']['siteEnergyList'][0]['siteOverview']['lastMonthData']['energy']
        currentPowerb = solarb['sitesOverviews']['siteEnergyList'][0]['siteOverview']['currentPower']['power']
        DayProductionb = solarb['sitesOverviews']['siteEnergyList'][0]['siteOverview']['lastDayData']['energy']
        MonthProductionb = solarb['sitesOverviews']['siteEnergyList'][0]['siteOverview']['lastMonthData']['energy']
    except:
        currentPowera = 0
        currentPowerb = 0
    print("Current power at 12 Tim = " + str(currentPowera) + " Watts \n")
    print("Current power at 18 Tim = " + str(currentPowerb) + " Watts \n")

    #get time
    current_time = get_current_time()

    #meter stuff
    kWh, netuse, pwr = get_kWh()
    netuse = round(float(netuse),2)
    print("meter now = " + str(kWh) + " kwh")
    print("usage = " + str(netuse) + " kwr")
    print(pwr)
    pwr = float(pwr) + float(currentPowera)

    #network stuff
    Intra_pings = pingNet.pingNet()
    #print Intra_pings

    #sense hat stuff
    sense=SenseHat()

    temp_c = sense.get_temperature()
    humidity = sense.get_humidity()
    pressure_mb = sense.get_pressure()
    temp_f = temp_c * 9.0 / 5.0 + 32.0
    temp_f = float("{0:.2f}".format(temp_f))
    humidity = float("{0:.2f}".format(humidity)) + 20
    pressure_in = 0.0295301*(pressure_mb)
    pressure_in = float("{0:.2f}".format(pressure_in))

    # attempt to get weather values, print 'n/a' if unable
    try:
        outside_conditions = get_conditions()
        #outside_temp_f = outside_conditions['current_observation']['temp_f']
        #outside_humidity_pct = outside_conditions['current_observation']['relative_humidity']
        outside_temp_k = outside_conditions['main']['temp']
        outside_humidity_pct = outside_conditions['main']['humidity']
        outside_wind = outside_conditions['wind']['speed']
        outside_temp_f = round((outside_temp_k-273.0) * 9.0 /5.0 +32.0, 2)
        outside_wind = round(outside_wind * 2.23694,2)
        print(outside_temp_f)
        print(outside_humidity_pct)
        print(temp_f)
        print(humidity)
        print(pressure_in)
    except Exception as e:
        print(e)
        outside_temp_f = 'n/a'
        outside_humidity_pct = 'n/a'

#   html1 = '<html><header><h1>Pi Monitoring System</h1><h2>Power Monitoring</h2><title>Pi in the Basement</title></header><body>'
    htmla = '<html><header><title>Erics Pi</title></hearder><body><center><h1>Pi Monitoring System</h1><h2>Power Monitoring</h2>'
    htmlb = '<table border="1"><tr><td><strong>Current Solar Power Dada (W)</strong></td><td>'
    htmlbb= '</td></tr><tr><td><strong>Current Solar Nana (W)</strong></td><td>'
    htmlc = '</td></tr><tr><td><strong>Current Meter Reading (kWh)</strong></td><td>'
    htmlx = '</td></tr><tr><td><strong>Metered Net This Month (kWh)</strong></td><td>'
    htmly = '</td></tr><tr><td><strong>Current Power Consumption (W)</strong></td><td>'
    #html4 = '</td></tr></table><h2>Environment</h2><table border="1"><tr><td></td></tr><tr><td><strong>Basement Temp (F)</strong></td><td>'
    htmld = '</td></tr></table><h2>Environment</h2><table border="1"><tr><td><strong>Basement Temp (F)</strong></td><td>'
    htmle = '</td></tr><tr><td><strong>Basement Humidity (%)</strong></td><td>'
    htmlf = '</td></tr><tr><td><strong>Basement Pressure (in)</strong></td><td>'
    htmlg = '</td></tr><tr><td><strong>Outside Temp (F)</strong></td><td>'
    htmlh = '</td></tr><tr><td><strong>Outside Humidity (%)</strong></td><td>'
    htmlz = '</td></tr><tr><td><strong>Outside Wind (mph)</strong></td><td>'
    htmli = '</td></tr></table>'

    table1 = htmla + htmlb + str(currentPowera) + htmlbb + str(currentPowerb) + htmlx + str(netuse) + htmly + str(pwr) + htmlc + str(kWh) + htmld + str(temp_f) + htmle + str(humidity) + htmlf + str(pressure_in) + htmlg + str(outside_temp_f) + htmlh + str(outside_humidity_pct) + htmlz + str(outside_wind) + htmli

    htmlclose = '</body></html>'

    htmlj = '<h2>Network</h2>'
    table_rows = ''
#   for (host, status) in Intra_pings.items():
#   table_rows += "<tr><td><strong>{}</strong></td><td>{}</td></tr>".format(host, status)

    for key in Intra_pings:
        if Intra_pings[key]['Status'] == 'up':
            table_rows += '<tr><td><strong>' + key + '</strong></td><td   bgcolor="#00FF00">' + Intra_pings[key]['Status'] + "</td></tr>"
        elif Intra_pings[key]['Status'] == 'down':
            table_rows += '<tr><td><strong>' + key + '</strong></td><td   bgcolor="#FF0000">' + Intra_pings[key]['Status'] + "</td></tr>"
    htmll = '</td></tr></table>'
    htmlm = '<table border="1"><tr><td>'
#   htmltime = '<h2>Time:</h2>'
#   html15 = '<h2>Current picture</h2><img src="http://127.0.0.1:6600" alt="Pi Camera Picture">'
#   html15 = '<h2>Current picture</h2><img src="image.jpg" alt="Pi Camera Picture">'
#   html15 = '<h2>Current picture</h2><img src="/home/pi/projects/webServer/image.jpg" alt="Pi Camera Picture" style="width:304px;height:228px;">'
    htmlclose = '</center></body></html>'

    table2 = htmlj + '<table border="1">' +  table_rows + htmll + str(current_time)

    response_body = table1 + table2 + htmlclose
    status = "200 OK"

    # Some header magic, create response

    response_headers = [('Content-type','text/html'), ('Content-Length', str(len(response_body)))]

    print(response_headers)

    start_response(status, response_headers)
    return [response_body.encode()]


# Make it serve on all addresses
# can be changed to e.g. 192.168.0.10 of you want to restrict to local network

print('making server')
with make_server('0.0.0.0', portNumber, application) as httpd:
    print('staring server on port number ' + str(portNumber) )
    httpd.serve_forever()
