import streamlit as st
import pandas as pd
import psycopg2
from datetime import datetime
import altair as alt
import plotly.graph_objects as go
import time

# Page setup
st.set_page_config(page_title="🌤️ Real-Time Weather Dashboard", layout="wide")

# PostgreSQL connection
@st.cache_resource
def get_conn():
    return psycopg2.connect(
        host="localhost",
        database="weatherdb",
        user="antropravin"
    )

conn = get_conn()

# Get latest timestamp
def get_latest_timestamp():
    with conn.cursor() as cur:
        cur.execute("SELECT MAX(timestamp) FROM weather_data;")
        return cur.fetchone()[0]

# Fetch latest data
def fetch_data():
    return pd.read_sql("SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 500", conn)

# Session state setup
if "last_known_timestamp" not in st.session_state:
    st.session_state.last_known_timestamp = get_latest_timestamp()

# Placeholder to hold all dashboard content
placeholder = st.empty()

# Location and map info
locations = ["New York", "London", "Tokyo", "Mumbai"]
city_coords = {
    "New York": [40.7128, -74.0060],
    "London": [51.5074, -0.1278],
    "Tokyo": [35.6895, 139.6917],
    "Mumbai": [19.0760, 72.8777],
}

# Infinite dashboard update loop
while True:
    with placeholder.container():
        df = fetch_data()
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df[df['location'].isin(locations)]

        if df.empty:
            st.title("🌍 Real-Time Weather Station Dashboard")
            st.caption("No data available yet. Waiting for updates...")
            time.sleep(5)
            continue

        st.title("🌍 Real-Time Weather Station Dashboard")
        st.caption("🔁 Auto-refreshing on new data")

        # Summary metrics
        col1, col2 = st.columns(2)
        col1.metric("🌡️ Avg. Temperature (°C)", f"{df['temperature'].mean():.2f}")
        col2.metric("💧 Avg. Humidity (%)", f"{df['humidity'].mean():.2f}")

        # Alerts
        st.subheader("🚨 Alerts")
        high_temp = df[df['temperature'] > 35]
        if high_temp.empty:
            st.success("✅ No high temperature alerts.")
        else:
            st.error("⚠️ High temperature detected!")
            st.dataframe(high_temp[['location', 'temperature', 'timestamp']], use_container_width=True)

        # Gauges
        st.subheader("🌡️ Temperature Gauges")
        gauge_cols = st.columns(len(locations))
        for i, city in enumerate(locations):
            city_df = df[df['location'] == city]
            if city_df.empty:
                continue
            latest_temp = city_df.iloc[0]['temperature']
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=latest_temp,
                title={'text': f"{city} Temperature (°C)"},
                gauge={
                    'axis': {'range': [0, 50]},
                    'bar': {'color': "orange" if latest_temp > 35 else "blue"},
                    'steps': [
                        {'range': [0, 20], 'color': "#d0f0fd"},
                        {'range': [20, 35], 'color': "#a0d6ff"},
                        {'range': [35, 50], 'color': "#ff9999"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 35
                    }
                }
            ))
            gauge_cols[i].plotly_chart(fig, use_container_width=True)

        # Latest Data Table
        st.subheader("🗃️ Latest Weather Data")
        st.dataframe(df.head(50), use_container_width=True, height=250)

        # Trends
        st.subheader("📈 Combined Trends")
        col1, col2 = st.columns(2)
        with col1:
            st.altair_chart(alt.Chart(df).mark_line(point=True).encode(
                x="timestamp:T",
                y="temperature:Q",
                color="location:N",
                tooltip=["location", "temperature", "timestamp"]
            ).interactive().properties(height=300), use_container_width=True)

        with col2:
            st.altair_chart(alt.Chart(df).mark_line(point=True).encode(
                x="timestamp:T",
                y="humidity:Q",
                color="location:N",
                tooltip=["location", "humidity", "timestamp"]
            ).interactive().properties(height=300), use_container_width=True)

        # Tabs for each city
        st.subheader("📍 City-wise Trends")
        tabs = st.tabs(locations)
        for i, city in enumerate(locations):
            with tabs[i]:
                city_df = df[df['location'] == city]
                st.markdown(f"### 🌆 {city}")
                st.dataframe(city_df.head(20), use_container_width=True)

                st.altair_chart(alt.Chart(city_df).mark_line(point=True).encode(
                    x="timestamp:T",
                    y="temperature:Q",
                    tooltip=["temperature", "timestamp"]
                ).interactive().properties(title=f"{city} Temperature", height=250), use_container_width=True)

                st.altair_chart(alt.Chart(city_df).mark_line(point=True).encode(
                    x="timestamp:T",
                    y="humidity:Q",
                    tooltip=["humidity", "timestamp"]
                ).interactive().properties(title=f"{city} Humidity", height=250), use_container_width=True)

                latest_temp = city_df.iloc[0]['temperature']
                if latest_temp > 35:
                    st.warning("🔥 Too hot! Stay hydrated.")
                elif latest_temp < 10:
                    st.info("❄️ Cold! Dress warmly.")
                else:
                    st.success("🌤️ Pleasant weather!")

        # Map View
        st.subheader("🗺️ City Map")
        map_df = pd.DataFrame([
            {"city": city, "lat": city_coords[city][0], "lon": city_coords[city][1]}
            for city in locations
        ])
        st.map(map_df, latitude="lat", longitude="lon", size=10)

        # Timestamp
        st.markdown("✅ **Updated at:** " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Check for new updates
    current_timestamp = get_latest_timestamp()
    if current_timestamp != st.session_state.last_known_timestamp:
        st.session_state.last_known_timestamp = current_timestamp
        st.rerun()

    # Delay before checking again
    time.sleep(5)
