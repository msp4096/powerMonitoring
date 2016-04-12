#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
#from sense_hat import SenseHat
#import json

PORT_NUMBER = 6600

#This class will handles any incoming request from
#the browser
class myHandler(BaseHTTPRequestHandler):

	#Handler for the GET requests
   def do_GET(self):
	self.send_response(200)
	self.send_header('Content-type','image/jpg')
	self.end_headers()
	f = open('image.jpg','rb')	
# Send the html message	
	self.wfile.write(f.read())
	f.close()
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
