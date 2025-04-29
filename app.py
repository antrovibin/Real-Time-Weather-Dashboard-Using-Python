from flask import Flask
from flask_socketio import SocketIO
import random, time, threading
import psycopg2

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

locations = ['New York', 'London', 'Tokyo', 'Mumbai']

# PostgreSQL connection
conn = psycopg2.connect(
    host="localhost",
    database="weatherdb",
    user="user",
)
cur = conn.cursor()

def generate_weather():
    while True:
        batch_data = []

        for city in locations:
            data = {
                'location': city,
                'temperature': round(random.uniform(15, 35), 2),
                'humidity': round(random.uniform(40, 80), 2)
            }
            batch_data.append(data)

            # Insert into DB
            cur.execute(
                "INSERT INTO weather_data (location, temperature, humidity) VALUES (%s, %s, %s)",
                (data['location'], data['temperature'], data['humidity'])
            )

        conn.commit()

        # Emit all city data at once
        for data in batch_data:
            socketio.emit('weather_update', data)
            print("Sent & Saved:", data)

        # Wait n seconds before generating the next batch
        time.sleep(5)

@app.route('/')
def index():
    return "Weather Simulator Running"

if __name__ == '__main__':
    threading.Thread(target=generate_weather).start()
    socketio.run(app, host="0.0.0.0", port=5000)


# To run the app, go to the terminal and type: python3 app.py
# drop the table if it exists:  psql -U user -h localhost postgres
# 
