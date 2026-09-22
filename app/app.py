from zoneinfo import available_timezones

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from config import SUPABASE_URL, SUPABASE_KEY
import db

st.title("Temperature Comparer Dashboard")

status, readings = db.fetch_readings(SUPABASE_URL, SUPABASE_KEY)

if status == 200:
    df = pd.DataFrame(readings)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp")

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
    st.error(f"Failed to load readings (status {status})")
