# ================= Import packages =================
from zoneinfo import available_timezones

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ================= Import modules =================
from config import SUPABASE_URL, SUPABASE_KEY, HOME_LATITUDE, HOME_LONGITUDE
import db
import weather

st.title("Temperature Comparer Dashboard")

# ================= Functions =================
def data_available(status, reading_type):
    if status != 200:
        st.error(f"Failed to load {reading_type} (status {status})")
        return False
    return True

# ================= Logic =================
sensor_status, sensor_readings = db.fetch_sensor_readings(SUPABASE_URL, SUPABASE_KEY)
current_status, current_readings = weather.fetch_current_readings(HOME_LATITUDE, HOME_LONGITUDE)

sensor_check = data_available(sensor_status, "sensor readings")
current_check = data_available(current_status, "current readings")

if sensor_check:
    df = pd.DataFrame(sensor_readings)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp")

if sensor_check and current_check:
    indoor_temp = df["temperature"].iloc[-1]
    outdoor_temp = current_readings["current"]["temperature_2m"]

    col1, col2 = st.columns(2)
    col1.metric("Indoor (latest)", f"{indoor_temp:.1f}°C")
    col2.metric("Outside (now)", f"{outdoor_temp:.1f}°C") 
else:
    st.error(f"Failed to load sensor vs outdoor weather comparison")

if sensor_check:
    timezone_options = sorted(available_timezones())
    selected_tz = st.selectbox(
        "Display times in:",
        timezone_options,
        index=timezone_options.index("Europe/London")
    )
    df.index = df.index.tz_convert(selected_tz)

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(x=df.index, y=df["temperature"], name="Temperature (°C)", mode="markers"),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=df.index, y=df["pressure"], name="Pressure (Pa)", mode="markers"),
        secondary_y=True,
    )
    fig.update_yaxes(title_text="Temperature (°C)", secondary_y=False)
    fig.update_yaxes(title_text="Pressure (Pa)", secondary_y=True)
    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis_rangeslider_visible=True
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.error(f"Failed to load readings (status {sensor_status})")
