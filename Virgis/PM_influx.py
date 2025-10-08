from influxdb import InfluxDBClient
import csv
from datetime import datetime, timedelta

CSV_FILE = "PM_influx_results.csv"
start_time = (datetime.utcnow() - timedelta(hours=600)).strftime("%Y-%m-%dT%H:%M:%SZ")
end_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

# --- Configuration ---
HOST = "158.129.192.209"
PORT = 8086
USER = "dataread"
PASS = "y8G1e2fENG"
DB = "vgtu_ts"
QUERY = f'''
SELECT "state", "topic" FROM "vgtu_ts"."autogen"."PM2" 
WHERE time > '{start_time}' AND time < '{end_time}'
AND ("topic"='PM2/sensor/steinel_co2/state' OR "topic"='PM2/sensor/steinel_abs_air_pressure/state'
OR "topic"='PM2/sensor/steinel_lux_2/state' OR "topic"='PM2/sensor/steinel_tmp_2/state'
OR "topic"='PM2/sensor/steinel_dptmp_2/state' OR "topic"='PM2/sensor/steinel_hih_2/state'
OR "topic"='PM2/sensor/steinel_abs_air_pressure_2/state' OR "topic"='PM2/sensor/steinel_rel_air_pressure_2/state'
OR "topic"='PM2/sensor/steinel_co2_2/state' OR "topic"='PM2/sensor/steinel_voc_2/state'
OR "topic"='PM2/sensor/ee_garso_lygis/state' OR "topic"='PM2/sensor/ee_lux_2/state'
OR "topic"='PM2/sensor/ee_hih_2/state' OR "topic"='PM2/sensor/ee_tmp_2/state'
OR "topic"='PM2/sensor/ee_sviesumas_2/state' OR "topic"='PM2/sensor/ee_sviesos_spalvos_temperatura_2/state'
OR "topic"='PM2/sensor/ee_saltos_spalvos_kiekis/state' OR "topic"='PM2/sensor/ee_siltos_spalvos_kiekis/state')
'''

AGREGATE_QUERY = f'''
SELECT COUNT("state") FROM "vgtu_ts"."autogen"."PM2" 
WHERE time > '{start_time}' AND time < '{end_time}'
AND ("topic"='PM2/sensor/steinel_co2/state' OR "topic"='PM2/sensor/steinel_abs_air_pressure/state'
OR "topic"='PM2/sensor/steinel_lux_2/state' OR "topic"='PM2/sensor/steinel_tmp_2/state'
OR "topic"='PM2/sensor/steinel_dptmp_2/state' OR "topic"='PM2/sensor/steinel_hih_2/state'
OR "topic"='PM2/sensor/steinel_abs_air_pressure_2/state' OR "topic"='PM2/sensor/steinel_rel_air_pressure_2/state'
OR "topic"='PM2/sensor/steinel_co2_2/state' OR "topic"='PM2/sensor/steinel_voc_2/state'
OR "topic"='PM2/sensor/ee_garso_lygis/state' OR "topic"='PM2/sensor/ee_lux_2/state'
OR "topic"='PM2/sensor/ee_hih_2/state' OR "topic"='PM2/sensor/ee_tmp_2/state'
OR "topic"='PM2/sensor/ee_sviesumas_2/state' OR "topic"='PM2/sensor/ee_sviesos_spalvos_temperatura_2/state'
OR "topic"='PM2/sensor/ee_saltos_spalvos_kiekis/state' OR "topic"='PM2/sensor/ee_siltos_spalvos_kiekis/state')
'''

# --- Connect ---
client = InfluxDBClient(host=HOST, port=PORT, username=USER, password=PASS, database=DB)

# --- Run InfluxQL query ---
result = client.query(QUERY)
amount_of_results = list(client.query(AGREGATE_QUERY).get_points())[0]["count"]

print(f"Grąžinta {amount_of_results} rezultatų")
# --- Extract points ---
points = list(result.get_points())

# --- Write to CSV ---
if points:
    with open(CSV_FILE, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=points[0].keys())
        writer.writeheader()
        writer.writerows(points)

    print(f"Results written to {CSV_FILE}")
else:
    print("No data returned.")