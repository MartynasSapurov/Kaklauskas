#Natalija_detailed.csv
import pandas as pd
from datetime import timezone
import datetime
import json
import paho.mqtt.client as mqtt
import numpy as np
import math

def my_times(time_str, offset_date):
    time_str = time_str.replace('.', ':').split(':')
    time_int_list = [int(item) for item in time_str]
    return str(offset_date + datetime.timedelta(
    time_int_list[0], time_int_list[1], time_int_list[2], time_int_list[3] * 1000))

def to_none(val):
    if math.isnan(val):
        return None
    return val

def np_encoder(object):
    if isinstance(object, np.generic):
        return object.item()

MQTT_HOST = "158.129.192.209"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
USER = "Natalija"
OFFSET_DATE = datetime.datetime(2024, 9, 11, 13, 20, 0, 0, timezone.utc)
DEVICE = "MA1"

def on_publish(client, userdata, mid):
    print("Message Published...")

def on_connect(client, userdata, flags, rc):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        # we should always subscribe from on_connect callback to be sure
        # our subscribed is persisted across reconnections.
        client.subscribe(MQTT_TOPIC)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, DEVICE) # client ID "mqtt-test"
client.on_connect = on_connect
client.on_publish = on_publish

client.username_pw_set("vgtu", "dPDIhIs2k0Cb")

df = pd.read_csv('Natalija_detailed.txt', sep='\t', header=6, float_precision='legacy')

"""
print(datetime.datetime(2024, 9, 11, 19, 20, 00, 1, timezone.utc))
print(datetime.datetime.now(timezone.utc))
"""

try:
    client.connect('158.129.192.209', 1883)
    required_columns = df.columns[1:]
    #required_columns = required_columns.remove('Video Time')
    for column in required_columns:
        for value in range(len(df)):
            #print(str(df[column][value]),str(column))

            try:

                time_str = my_times(df['Video Time'][value], OFFSET_DATE)
                transmit_data = {
                    "device": {
                        "name": DEVICE,
                        "user": USER,
                        "type": "data",
                        "time": time_str,
                    },
                    "field": {
                        "value": df[column][value],
                        "state": "good",
                        "friendly_name": str(column),
                        "unit": ""
                    }
                }

                MQTT_TOPIC = DEVICE+"/"+str(column)+"/"
                MQTT_MSG = json.dumps(transmit_data, default=np_encoder)
                client.publish(MQTT_TOPIC, MQTT_MSG)

            except:
                print("Unable to write data")
    client.loop_stop()
except:
    print("Unable to connect")

"""
print(df.columns)
print("*"*80)
print(df['Video Time'][0])
print("*"*80)
time = datetime.datetime.now(timezone.utc)
#print(str(time+datetime.timedelta(0, df['Video Time'][5])))
print(df['Video Time'][5012])
"""

