from influxdb import InfluxDBClient
import csv
from datetime import datetime, timedelta

PM = "PM1" #Sistemos pasirinkimas PM1, PM2, PM3, PM4, PM5, PM6, PM7, PM8, PM9

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
SELECT "state", "topic" FROM "vgtu_ts"."autogen"."{PM}"
WHERE time > '{start_time}' AND time < '{end_time}'
AND ("topic"='{PM}/sensor/steinel_abs_air_pressure/state' OR "topic"='{PM}/sensor/steinel_dptmp/state'
OR "topic"='{PM}/sensor/steinel_hih/state' OR "topic"='{PM}/sensor/steinel_lux/state'
OR "topic"='{PM}/sensor/steinel_rel_air_pressure/state' OR "topic"='{PM}/sensor/steinel_tmp/state'
OR "topic"='{PM}/sensor/steinel_voc/state' OR "topic"='{PM}/sensor/ee_hih/state' OR "topic"='{PM}/sensor/ee_lux/state'
OR "topic"='{PM}/sensor/ee_saltos_spalvos_kiekis/state' OR "topic"='{PM}/sensor/ee_siltos_spalvos_kiekis/state'
OR "topic"='{PM}/sensor/ee_sviesos_spalvos_temperatura/state' OR "topic"='{PM}/sensor/ee_sviesumas/state'
OR "topic"='{PM}/sensor/ee_tmp/state')
'''

AGREGATE_QUERY = f'''
SELECT COUNT("state") FROM "vgtu_ts"."autogen"."{PM}" 
WHERE time > '{start_time}' AND time < '{end_time}'
AND ("topic"='{PM}/sensor/steinel_abs_air_pressure/state' OR "topic"='{PM}/sensor/steinel_dptmp/state'
OR "topic"='{PM}/sensor/steinel_hih/state' OR "topic"='{PM}/sensor/steinel_lux/state'
OR "topic"='{PM}/sensor/steinel_rel_air_pressure/state' OR "topic"='{PM}/sensor/steinel_tmp/state'
OR "topic"='{PM}/sensor/steinel_voc/state' OR "topic"='{PM}/sensor/ee_hih/state' OR "topic"='{PM}/sensor/ee_lux/state'
OR "topic"='{PM}/sensor/ee_saltos_spalvos_kiekis/state' OR "topic"='{PM}/sensor/ee_siltos_spalvos_kiekis/state'
OR "topic"='{PM}/sensor/ee_sviesos_spalvos_temperatura/state' OR "topic"='{PM}/sensor/ee_sviesumas/state'
OR "topic"='{PM}/sensor/ee_tmp/state')
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
