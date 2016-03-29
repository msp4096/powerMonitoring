from sense_hat import SenseHat
import time

sense = SenseHat()
#sense.clear(255, 255, 255)
sense.low_light = True
#time.sleep(2)
#sense.low_light = False

#while True:
t = '%.3f' % sense.get_temperature()
tf = float(t)*(9.0/5.0) + 32
p = '%.3f' % sense.get_pressure()
h = '%.3f' % sense.get_humidity()

print "Temperature = %s C" %(t)
print "Temperature = %s F" %(tf)
print "Pressure = %s millibar" %(p)
print "Humidity = %s percent" %(h)


#    t = round(t, 1)
#    p = round(p, 1)
#    h = round(h, 1)

    #msg = "Temperature = %s, Pressure=%s, Humidity=%s" % (t,p,h)

    #sense.show_message(msg, scroll_speed=0.1)
