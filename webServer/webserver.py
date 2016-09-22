from wsgiref.simple_server import make_server
import time
import json
import urllib2
import sys
from sense_hat import SenseHat
import pingNet
import os
#import picamera

portNumber = 80

#Get solar power data from the SolarEdge API
def get_solar():
	api_solar_url = "https://monitoringapi.solaredge.com/sites/196000/overview.json?api_key=JRPXUFIKH0KMXBAO7NXQWYF7A6IYRT8G"
	try:
	  	f = urllib2.urlopen(api_solar_url)
	except:
		print "Failed to get solar"
		return False
	json_solar = f.read()
	f.close()
	return json.loads(json_solar)

#Get current information from the log file
def get_kWh():
    
	path = '/home/pi/projects/powerMonitoring/logs/'
	fileTS = time.strftime("%Y-%m")
	tfile = open(path+'energy_'+fileTS+'.log')
	lines = tfile.readlines()
	if lines:
		first_line = str(lines[0].rstrip())
		last_line = str(lines[-1].rstrip())
	tfile.close()
	first_line = first_line.split(',')
	last_line  = last_line.split(',')
	print first_line
	print last_line
	kWh = last_line[1]
	netuse = last_line[3]
	pwr = last_line[2]
	return (kWh, netuse, pwr)

#start the server and get values when page is refreshed
def application(environ, start_response):

    print environ['PATH_INFO']

    #solar stuff
    solar = get_solar()
    currentPower = solar['sitesOverviews']['siteEnergyList'][0]['siteOverview']['currentPower']['power']
    print currentPower

    #meter stuff
    kWh, netuse, pwr = get_kWh()
    print kWh
    print netuse
    print pwr

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
    humidity = float("{0:.2f}".format(humidity))
    pressure_in = 0.0295301*(pressure_mb)
    pressure_in = float("{0:.2f}".format(pressure_in))

    print temp_f
    print humidity
    print pressure_in

    html1 = '<html><header><h1>Pi Monitoring System</h1><h2>Power & Environment</h2><title>Pi in the Basement</title></header><body>'
    html2 = '<table border="1"><tr><td><strong>Current Solar Output (W)</strong></td><td>'
    html3 = '</td></tr><tr><td><strong>Meter Reading (kWh)</strong></td><td>'
    htmlx = '</td></tr><tr><td><strong>Net this month (kWh)</strong></td><td>'
    htmly = '</td></tr><tr><td><strong>Current power (W)</strong></td><td>' 
    html4 = '</td></tr><tr><td><strong>Basement Temp (F)</strong></td><td>'
    html5 = '</td></tr><tr><td><strong>Basement Humidity (%)</strong></td><td>'
    html6 = '</td></tr><tr><td><strong>Basement Pressure (in)</strong></td><td>'
    html7 = '</td></tr></table>'

    table1 = html1 + html2 + str(currentPower) + html3 + str(kWh) + htmlx + str(netuse) + htmly + str(pwr) + html4 + str(temp_f) + html5 + str(humidity) + html6 + str(pressure_in)+ html7

    htmlclose = '</body></html>'
    html8 = '<h2>Network</h2>'
    html9 = '<table border="1">'
    table_rows = ''
#    for (host, status) in Intra_pings.items():
#        table_rows += "<tr><td><strong>{}</strong></td><td>{}</td></tr>".format(host, status)

    for key in Intra_pings:
        if Intra_pings[key]['Status'] == 'up':
            table_rows += '<tr><td><strong>' + key + '</strong></td><td   bgcolor="#00FF00">' + Intra_pings[key]['Status'] + "</td></tr>"
        elif Intra_pings[key]['Status'] == 'down':
            table_rows += '<tr><td><strong>' + key + '</strong></td><td   bgcolor="#FF0000">' + Intra_pings[key]['Status'] + "</td></tr>"

    html14 = '</td></tr></table>'
    #htmltime = '<h2>Time:</h2>'
#    html15 = '<h2>Current picture</h2><img src="http://127.0.0.1:6600" alt="Pi Camera Picture">'
#    html15 = '<h2>Current picture</h2><img src="image.jpg" alt="Pi Camera Picture">'
#    html15 = '<h2>Current picture</h2><img src="/home/pi/projects/webServer/image.jpg" alt="Pi Camera Picture" style="width:304px;height:228px;">'
    htmlclose = '</body></html>'

    table2 = html8 + html9 + table_rows + html14

    # response_body
    #response_body = table1 + table2 + html15 + htmlclose
    response_body = table1 + table2 + htmlclose
    status = '200 OK'

    # Some header magic, create response
    
    response_headers = [('Content-type', 'text/html'), ('Content-Length', str(len(response_body)))]

#    if '.jpg' in str(environ['PATH_INFO']):
#	response_headers = [('Content-type', 'image/jpg'), ('Content-Length', str(len(response_body)))]

#print response_headers

	#response_headers = [('Content-Type', 'image/jpeg'), ('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)

    return [response_body]

# Make it serve on all addresses
# can be changed to e.g. 192.168.0.10 of you want to restric to local network
httpd = make_server('0.0.0.0', portNumber, application)
httpd.serve_forever()
