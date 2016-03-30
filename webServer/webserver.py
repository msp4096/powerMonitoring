from wsgiref.simple_server import make_server
import time
import json
import urllib2
import sys
from sense_hat import SenseHat
import pingNet
import os

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

#Get current meter reading from the log file
def get_kWh():
    path = '/home/pi/projects/powerMonitoring/'
    tfile = open(path+'reading')
    text = tfile.read()
    tfile.close()
    data = json.loads(text)
    kWh = float(data['Message']['Consumption']) / 100
    return kWh

#start the server and get values when page is refreshed
def application(environ, start_response):
    # #network stuff
    # router = '192.168.0.1'
    # lcom   = '192.168.0.105'
    # ubnt   = '192.168.0.77'
    # seccam = '192.168.0.88'
    # HPprint= '192.168.0.112'
    # #nanaph = '192.168.0.115' #these won't ping...
    # #myphon = '192.168.0.101' #these won't ping...
    #
    # router_response = os.system("ping -c 1 " + router)
    # lcom_response   = os.system("ping -c 1 " + lcom)
    # ubnt_response   = os.system("ping -c 1 " + ubnt)
    # seccam_response = os.system("ping -c 1 " + seccam)
    # HPprint_response= os.system("ping -c 1 " + HPprint)
    # #nanaph_response = os.system("ping -c 1 " + nanaph)
    # #myphon_response = os.system("ping -c 1 " + myphon)
    #
    # #and then check the response...
    # if router_response == 0:
    #   print 'Router is up'
    #   router_response = 'Up'
    # else:
    #   print 'Router is down'
    #   router_response = 'Down'
    #
    # if lcom_response == 0:
    #   print 'DoomAlpha is up'
    #   lcom_response = 'Up'
    # else:
    #   print 'DoomAlpha is down'
    #   lcom_response = 'Down'
    #
    # if ubnt_response == 0:
    #   print 'Nana UBNT is up'
    #   ubnt_response = 'Up'
    # else:
    #   print 'Nana UBNT is down'
    #   ubnt_response = 'Down'
    #
    # if seccam_response == 0:
    #   print 'Cameras are up'
    #   seccam_response = "Up"
    # else:
    #   print 'Cameras are down'
    #   seccam_response = "Down"
    #
    # if HPprint_response == 0:
    #     print 'Printer is up'
    #     HPprint_response = "Up"
    # else:
    #     print 'Printer is down'
    #     HPprint_response = "Down"

    #solar stuff
    solar = get_solar()
    currentPower = solar['sitesOverviews']['siteEnergyList'][0]['siteOverview']['currentPower']['power']
    print currentPower

    #meter stuff
    kWh = get_kWh()
    print kWh

    #network stuff
    Intra_pings = pingNet.pingNet()
    print Intra_pings

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
    html4 = '</td></tr><tr><td><strong>Basement Temp (F)</strong></td><td>'
    html5 = '</td></tr><tr><td><strong>Basement Humidity (%)</strong></td><td>'
    html6 = '</td></tr><tr><td><strong>Basement Pressure (in)</strong></td><td>'
    html7 = '</td></tr></table>'

    table1 = html1 + html2 + str(currentPower) + html3 + str(kWh) + html4 + str(temp_f) + html5 + str(humidity) + html6 + str(pressure_in)+ html7
    # html8 = '<h2>Network</h2>'
    # html9 = '<table border="1"><tr><td><strong>Router</strong></td><td>'
    # html10 = '</td></tr><tr><td><strong>HP Printer</strong></td><td>'
    # html11 = '</td></tr><tr><td><strong>DoomAlpha</strong></td><td>'
    # html12 = '</td></tr><tr><td><strong>Nana&#39s UBNT</strong></td><td>'
    # html13 = '</td></tr><tr><td><strong>Cameras</strong></td><td>'
    # html14 = '</td></tr></table>'
    #htmltime = '<h2>Time:</h2>'

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
    htmlclose = '</body></html>'

    table2 = html8 + html9 + table_rows + html14
    #table2 = html8 + html9 + router_response + html10 + HPprint_response + html11 + lcom_response + html12 + ubnt_response + html13 + seccam_response+ html14

    # response_body
    response_body = table1 + table2 + htmlclose
    status = '200 OK'

    # Some header magic, create response
    response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)

    return [response_body]

# Make it serve on all addresses
# can be changed to e.g. 192.168.0.10 of you want to restric to local network
httpd = make_server('0.0.0.0', 80, application)
httpd.serve_forever()
