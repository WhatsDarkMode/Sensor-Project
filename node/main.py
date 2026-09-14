from machine import I2C, Pin
from bme280_float import BME280
import time

i2c = I2C(scl=Pin(22), sda=Pin(21))
bme = BME280(i2c=i2c, address=0x76)

while True:
    print(bme.values)
    time.sleep(5)