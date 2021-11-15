#!/usr/bin/python3

from wsgiref.simple_server import make_server
import time
import json
import urllib.request as urllib2, json
import sys
import os
import os.path
from picamera import PiCamera
from sense_hat import SenseHat

sense = SenseHat()
camera = PiCamera()

# ------ User settings -------
portNumber = 82

print('User settings imported')

#Get time
def get_current_time():
    print('time...')
    current_time = time.strftime('%H:%M:%S')
    print(current_time)
    return current_time

#start the server and get values when page is refreshed
def application(environ, start_response):

#    with picamera.PiCamera() as camera:
#        camera.resolution = (1024,768)
#        camera.start_preview()
 #       white = (255,255,255)
    camera.resolution = (1024,768)
    camera.start_preview()
    white = (255,255,255)
    sense.clear(white)
    time.sleep(0.5)
    camera.capture('image.jpg')
    sense.clear()
    status = '200 OK'
    headers = [('Content-type','image/jpg')]
    print('Application started')
    print(environ['PATH_INFO'])
    start_response(status,headers)
    data = b''
    filename = r'image.jpg'
    with open(filename, 'rb', buffering=0) as f:
        data = f.readall()
    print(type(data))
    return [data]


# Make it serve on all addresses
# can be changed to e.g. 192.168.0.10 of you want to restrict to local network

print('making server')
with make_server('0.0.0.0', portNumber, application) as httpd:
    print('staring server on port number ' + str(portNumber) )
    httpd.serve_forever()
