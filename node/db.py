import urequests
import ujson

def login(supabase_url, supabase_key, supabase_node_email, supabase_node_pw):
    auth_response = urequests.post(
        supabase_url + "/auth/v1/token?grant_type=password",
        headers={"Content-Type": "application/json", "apikey": supabase_key},
        data=ujson.dumps({"email": supabase_node_email, "password": supabase_node_pw})
    )
    access_token = auth_response.json()["access_token"]
    auth_response.close()
    return access_token

def insert_reading(supabase_url, supabase_key, access_token, room, temperature, pressure):
    response = urequests.post(
        supabase_url + "/rest/v1/readings",
        headers={
        "Content-Type": "application/json",
        "apikey": supabase_key,
        "Authorization": "Bearer " + access_token
        },
        data=ujson.dumps({"room": room, "temperature": temperature, "pressure": pressure})
    )
    status = response.status_code
    body = response.text
    response.close()
    return status, body