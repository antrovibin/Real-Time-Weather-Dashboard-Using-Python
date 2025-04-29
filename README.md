# Real-Time-Weather-Dashboard-Using-Python
A real-time weather monitoring dashboard built using Streamlit, Flask, Socket.IO, and PostgreSQL. It continuously streams weather data for major cities, stores it in a database, and visualizes it in a live-updating dashboard with insightful charts, alerts, and maps.

## Features
- Real-time temperature and humidity simulation
- Auto-refreshing dashboard when new data is available
- Interactive visualizations using Altair and Plotly
- Alerts for high temperature events
- Geographic visualization of weather data on a map
- City-wise breakdown with recent history and suggestions

## Project Structure
```bash
weather-dashboard/
├── app.py                 # Flask server generating and emitting weather data
├── dashboard.py           # Streamlit dashboard consuming data from PostgreSQL
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── weatherdb_schema.sql   # PostgreSQL schema setup
```

## Setup Instructions
**1. Clone the Repository**
```bash
git clone https://github.com/your-username/weather-dashboard.git
cd weather-dashboard
```
