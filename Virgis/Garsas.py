from influxdb import InfluxDBClient
import csv
from datetime import datetime, timedelta

CSV_FILE = "influx_results.csv"
start_time = (datetime.utcnow() - timedelta(hours=20)).strftime("%Y-%m-%dT%H:%M:%SZ")
end_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

# --- Configuration ---
HOST = "158.129.192.209"
PORT = 8086
USER = "dataread"
PASS = "y8G1e2fENG"
DB = "vgtu_ts"
QUERY = f'''
SELECT "field_value", "field_friendly_name"
FROM "vgtu_ts"."autogen"."MRK"
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
