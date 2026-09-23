import requests

def fetch_sensor_readings(supabase_url, supabase_key):
    # Could make this function select more specific data 
    # to reduce network overhead and local compute
    params = {"select": "*"}

    response = requests.get(
        supabase_url + "/rest/v1/readings",
        headers = {
            "apikey": supabase_key,
            "Authorization": "Bearer " + supabase_key
        },
        params = params
    )

    return response.status_code, response.json()