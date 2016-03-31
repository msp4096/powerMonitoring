#!/usr/local/bin/python

from wsgiref.simple_server import make_server
import time
import json
import urllib2
import sys
from sense_hat import SenseHat
import pingNetONR
import os

#start the server and get values when page is refreshed
def application(environ, start_response):

    #network stuff
    Intra_pings = pingNetONR.pingNetONR()
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

    html1 = '<html><header><h1>ONR Raspberry Pi Monitoring System</h1><h2>Environmental Sensors</h2><title>North Transmitter</title></header><body>'
    html2 = '<table border="1">'
    html4 = '<tr><td><strong>Transmitter Temp (F)</strong></td><td>'
    html5 = '</td></tr><tr><td><strong>Transmitter Humidity (%)</strong></td><td>'
    html6 = '</td></tr><tr><td><strong>Transmitter Pressure (in)</strong></td><td>'
    html7 = '</td></tr></table>'

    table1 = html1 + html2 + html4 + str(temp_f) + html5 + str(humidity) + html6 + str(pressure_in)+ html7

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
