from picamera import PiCamera
from time import sleep
from sense_hat import SenseHat

camera = PiCamera()

sense = SenseHat()

white = (255,255,255)
red  = (255,0,0)
blue = (0,0,255)
sense.clear(blue)
camera.capture('image.jpg')
sense.clear()
exit()
