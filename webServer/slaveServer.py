#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from sense_hat import SenseHat

PORT_NUMBER = 80



#This class will handles any incoming request from
#the browser
class myHandler(BaseHTTPRequestHandler):

	#Handler for the GET requests
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		# Send the html message

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

		self.wfile.write({'temp':temp_f,'pressure':pressure_in,'Humidity':humidity})
		return

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER

	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
