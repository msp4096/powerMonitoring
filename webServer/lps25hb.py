

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

try:
    # LPS25HB address, 0x5C(92)
    # Select Control register, 0x20(32)
    #		0x90(144)	Active mode, Continous update
    bus.write_byte_data(0x5C, 0x20, 0x90)

    time.sleep(0.1)

    # LPS25HB address, 0x5C(92)
    # Read data back from 0x28(40), with Command register, 0x80(128)
    # 3 bytes, Pressure LSB first
    data = bus.read_i2c_block_data(0x5C, 0x28 | 0x80, 3)

    # Convert the data to hPa
    pressure = (data[2] * 65536 + data[1] * 256 + data[0]) / 4096.0

    # Output data to screen
    print ("Barometric Pressure is : " + str(pressure) +  "hPa")

except:
    print("LPS25HB Pressure Senore Device not found")
