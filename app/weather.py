import requests

def fetch_current_readings(home_latitude, home_longitude):
    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": home_latitude,
            "longitude": home_longitude,
            "current": "temperature_2m,surface_pressure",
            "timezone": "auto"
        }
    )

    return response.status_code, response.json()