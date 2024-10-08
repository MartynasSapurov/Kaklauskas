import pandas as pd
from datetime import timezone
import datetime
import json
import paho.mqtt.client as mqtt
import numpy as np
import math

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

def on_publish(client, userdata, mid):
    print("Message Published...")

def on_connect(client, userdata, flags, rc):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        # we should always subscribe from on_connect callback to be sure
        # our subscribed is persisted across reconnections.
        client.subscribe(MQTT_TOPIC)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "MR4") # client ID "mqtt-test"
client.on_connect = on_connect
client.on_publish = on_publish

client.username_pw_set("vgtu", "dPDIhIs2k0Cb")

df = pd.read_csv('MartPro3split2.csv', sep=',', header=0, float_precision='legacy')

"""
print(datetime.datetime(2024, 9, 11, 19, 20, 00, 1, timezone.utc))
print(datetime.datetime.now(timezone.utc))
"""

try:
    client.connect('158.129.192.209', 1883)
    for column in df.columns:
        for value in range(len(df)):
            #print(str(df[column][value]),str(column))
            try:
                #client.connect('158.129.192.209', 1883)
                #time = datetime.datetime.now(timezone.utc)
                time = datetime.datetime(2024, 9, 11, 15, 31, 3, 240001, timezone.utc)
                time_str = str(time+datetime.timedelta(0, df['endPosSec'][value]))
                print(df['endPosSec'][value])
                print(time_str)
                transmit_data = {
                    "device": {
                        "name": "MR101",
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
                #MQTT_TOPIC = "MR101/" + str(column) + "/"
                MQTT_TOPIC = "MR4/"+str(column)+"/"
                MQTT_MSG = json.dumps(transmit_data, default=np_encoder)

                client.publish(MQTT_TOPIC, MQTT_MSG)

                #client.loop_stop()

            except:
                print("Unable to write data")
    client.loop_stop()
except:
    print("Unable to connect")

"""
print(df.columns)
print("*"*80)
print(df['index'][0])
print("*"*80)
time = datetime.datetime.now(timezone.utc)
print(str(time+datetime.timedelta(0, df['endPosSec'][5])))
print(df['endPosSec'][5])
"""
