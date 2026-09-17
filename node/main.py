import time
from machine import I2C, Pin

# =========== From Modules =========== 
from bme280_float import BME280
import wifi
import db
from config import WIFI_SSID, WIFI_PASSWORD, SUPABASE_URL, SUPABASE_KEY, SUPABASE_NODE_EMAIL, SUPABASE_NODE_PW

ROOM = "spare_room"

i2c = I2C(scl=Pin(22), sda=Pin(21))
bme = BME280(i2c=i2c, address=0x76)

if not wifi.connect(WIFI_SSID, WIFI_PASSWORD):
    print("Initial WIFI connection failed")

access_token = db.login(SUPABASE_URL, SUPABASE_KEY, SUPABASE_NODE_EMAIL, SUPABASE_NODE_PW)

while True:
    if not wifi.connect(WIFI_SSID, WIFI_PASSWORD):
        print("WiFi reconnect failed, retrying")
        time.sleep(60)
        continue

    temperature, pressure, humidity = bme.values

    try:
        status = db.insert_reading(SUPABASE_URL, SUPABASE_KEY, access_token, ROOM, temperature, pressure, humidity):
        if status == 201:
            print("Reading sent successfully:", temperature, humidity)
        else:
            print("Insert failed, status:", status)
    except Exception as e:
        print("Insert error:", e)

    time.sleep(60)