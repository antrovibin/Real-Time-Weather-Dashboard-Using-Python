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
**2. Setup PostgreSQL**
```bash
-- Connect to your PostgreSQL instance
CREATE DATABASE weatherdb;

-- Inside weatherdb
CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,
    location VARCHAR(50),
    temperature FLOAT,
    humidity FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**3. Run the Weather Simulator**
```bash
python app.py
```
This starts a Flask server that simulates and inserts new weather data every 5 seconds.

**4. Run the Streamlit Dashboard**
```bash
streamlit run dashboard.py
```

## Technologies Used
* Python

* Streamlit – Dashboard frontend

* Flask + Socket.IO – Real-time weather simulation

* PostgreSQL – Persistent storage

* Altair & Plotly – Visualizations

## Screenshots
![Output](https://github.com/antrovibin/Real-Time-Weather-Dashboard-Using-Python/blob/main/Output.png)


## How It Works
1. **Weather Generator (app.py):** Simulates data for 4 cities and inserts it into a PostgreSQL database every 5 seconds. Also emits it via Socket.IO.

2. **Dashboard (dashboard.py):** Continuously checks for new data and updates in real time, re-rendering the visual elements without user refresh.

## License
This project is licensed under the MIT License.
