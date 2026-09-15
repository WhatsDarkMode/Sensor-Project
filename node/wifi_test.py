import network
import time
from config import WIFI_SSID, WIFI_PASSWORD

sta_if = network.WLAN(network.WLAN.IF_STA)
sta_if.active(True)

if not sta_if.isconnected():
    print("Connecting to WiFi...")
    sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
    while not sta_if.isconnected():
        time.sleep(0.5)

print("Connected: Network config - ", sta_if.ifconfig())