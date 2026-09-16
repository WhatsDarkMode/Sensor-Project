import network
import time
import urequests
import ujson
from config import WIFI_SSID, WIFI_PASSWORD, SUPABASE_URL, SUPABASE_KEY, SUPABASE_NODE_EMAIL, SUPABASE_NODE_PW

# Connect to WiFi
wifi = network.WLAN(network.WLAN.IF_STA)
wifi.active(True)
if not wifi.isconnected():
    print("Connecting to WiFi...")
    wifi.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wifi.isconnected():
        time.sleep(0.5)
print("WiFi connected:", wifi.ifconfig())

# Get Auth Token
auth_response = urequests.post(
    SUPABASE_URL + "/auth/v1/token?grant_type=password",
    headers={"Content-Type": "application/json", "apikey": SUPABASE_KEY},
    data=ujson.dumps({"email": SUPABASE_NODE_EMAIL, "password": SUPABASE_NODE_PW})
)
print("Auth status:", auth_response.status_code)
access_token = auth_response.json()["access_token"]
auth_response.close()

# Mock insert
insert_response = urequests.post(
    SUPABASE_URL + "/rest/v1/readings",
    headers={
        "Content-Type": "application/json",
        "apikey": SUPABASE_KEY,
        "Authorization": "Bearer " + access_token
    },
    data=ujson.dumps({"room": "spare_room", "temperature": 21.4, "humidity": 46.3})
)

print("Insert status:", insert_response.status_code)
print("Insert response:", insert_response.text)
insert_response.close()