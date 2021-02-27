import time
from sense_hat import SenseHat

sense = SenseHat()

while True:
    acceleration = sense.get_accelerometer_raw()
    x = acceleration['x']
    y = acceleration['y']
    z = acceleration['z']

    x=round(x, 0)
    y=round(y, 0)
    z=round(z, 0)

    print("x={0}, y={1}, z={2}".format(x, y, z))
    time.sleep(1)

    north = sense.get_compass()
    print("North: %s" % north)

    # alternatives
    #print(sense.compass)
    gyro_only = sense.get_gyroscope()
    print("p: {pitch}, r: {roll}, y: {yaw}".format(**gyro_only))
    from sense_hat import SenseHat

    sense.show_message("FINNY FINNY STOOOOOOOONE", text_colour=[255, 0, 0])
