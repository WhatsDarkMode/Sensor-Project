import requests
from config import SUPABASE_URL, SUPABASE_KEY

response = requests.get(
    SUPABASE_URL + "/rest/v1/readings",
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": "Bearer " + SUPABASE_KEY
    },
    params = {"select": "*"}
)

print("Status: ", response.status_code)
print(response.json())