import sys
import os

router = '192.168.0.1'
lcom   = '192.168.0.105'
ubnt   = '192.168.0.77'
seccam = '192.168.0.88'
HPprint= '192.168.0.112'
#nanaph = '192.168.0.115' #these won't ping...
#myphon = '192.168.0.101' #these won't ping...

router_response = os.system("ping -c 1 " + router)
lcom_response   = os.system("ping -c 1 " + lcom)
ubnt_response   = os.system("ping -c 1 " + ubnt)
seccam_response = os.system("ping -c 1 " + seccam)
HPprint_response= os.system("ping -c 1 " + HPprint)
#nanaph_response = os.system("ping -c 1 " + nanaph)
#myphon_response = os.system("ping -c 1 " + myphon)

#and then check the response...
if router_response == 0:
  print 'Router is up'
  router_response = 'Up'
else:
  print 'Router is down'
  router_response = 'Down'

if lcom_response == 0:
  print 'DoomAlpha is up'
  lcom_response = 'Up'
else:
  print 'DoomAlpha is down'
  lcom_response = 'Down'

if ubnt_response == 0:
  print 'Nana UBNT is up'
  ubnt_response = 'Up'
else:
  print 'Nana UBNT is down'
  ubnt_response = 'Down'

if seccam_response == 0:
  print 'Cameras are up'
  seccam_response = "Up"
else:
  print 'Cameras are down'
  seccam_response = "Down"

if HPprint_response == 0:
    print 'Printer is up'
    HPprint_response = "Up"
else:
    print 'Printer is down'
    HPprint_response = "Down"
#return {router_response, lcom_response, ubnt_response, seccam_response, HPprint_response}
