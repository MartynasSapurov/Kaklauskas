from influxdb import InfluxDBClient
import csv
from datetime import datetime, timedelta

CSV_FILE = "influx_results.csv"
start_time = (datetime.utcnow() - timedelta(hours=600)).strftime("%Y-%m-%dT%H:%M:%SZ")
end_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

# --- Configuration ---
HOST = "158.129.192.209"
PORT = 8086
USER = "dataread"
PASS = "y8G1e2fENG"
DB = "vgtu_ts"
QUERY = f'''
SELECT "arousal_value", "angry_value", "boredom_value", "disgusted_value", "happy_value",
"interest_value", "neutral_value", "sad_value", "scared_value", "surprised_value", "valence_value",
"right_eyebrow_value", "right_eye_value", "pitch_value", "mouth_value", "left_eye_value", "roll_value",
"verticalposition_value", "x-head_orientation_value", "y-head_orientation_value", "yaw_value" 
FROM "vgtu_ts"."autogen"."MA1"
WHERE time > '{start_time}' AND time < '{end_time}'
'''


# --- Connect ---
client = InfluxDBClient(host=HOST, port=PORT, username=USER, password=PASS, database=DB)

# --- Run InfluxQL query ---
result = client.query(QUERY)

# --- Extract points ---
points = list(result.get_points())

# --- Write to CSV ---
if points:
    with open(CSV_FILE, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=points[0].keys())
        writer.writeheader()
        writer.writerows(points)

    print(f"✅ Results written to {CSV_FILE}")
else:
    print("⚠️ No data returned.")
