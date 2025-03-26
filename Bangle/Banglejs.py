#for btadv Banglejs App
import asyncio
from bleak import BleakClient, BleakScanner

from datetime import timezone
import datetime
import json
import paho.mqtt.client as mqtt

# Heart Rate Measurement UUID
HRM_CHAR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

MQTT_HOST = "158.129.192.209"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45


MQTT_TOPIC = "test/heartrate/"

# time_str = str(datetime.datetime.now(timezone.utc))

# MQTT_MSG=json.dumps({"device_id": "radar", "system":  "rpi", "version":  "0.0a", "time":time_str})

def on_publish(client, userdata, mid):
    print("Message Published...")

def on_connect(client, userdata, flags, rc):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        # we should always subscribe from on_connect callback to be sure
        # our subscribed is persisted across reconnections.
        client.subscribe(MQTT_TOPIC)


mqtt_client = mqtt.Client("test")  # client ID "mqtt-test"
mqtt_client.on_connect = on_connect
mqtt_client.on_publish = on_publish

mqtt_client.username_pw_set("vgtu", "dPDIhIs2k0Cb")


# client.connect('158.129.192.209', 1883)

async def main():
    print("Scanning for Bangle.js...")
    devices = await BleakScanner.discover()
    bangle = None
    for d in devices:
        if d.name and "Bangle.js" in d.name:
            bangle = d
            break

    if not bangle:
        print("Could not find Bangle.js!")
        return

    print(f"Connecting to {bangle.name}...")
    async with BleakClient(bangle) as client:
        print("Connected!")

        def hrm_callback(sender, data):
            bpm = data[1]
            print(f"Heart Rate: {bpm} bpm")

            time_str = str(datetime.datetime.now(timezone.utc))
            transmit_data = {
                "device": {
                    "name": "Test",
                    "user": "Simona",
                    "type": "sensor",
                    "time": time_str,
                },
                "field": {
                    "value": bpm,
                    "state": "good",
                    "friendly_name": "Heartrate",
                    "unit": ""
                }
            }
            MQTT_MSG = json.dumps(transmit_data)
            MQTT_TOPIC = "test/heartrate/"

            mqtt_client.connect('158.129.192.209', 1883)
            mqtt_client.publish(MQTT_TOPIC, MQTT_MSG)
            print(time_str)
            mqtt_client.loop_stop()
        await client.start_notify(HRM_CHAR_UUID, hrm_callback)

        print("Listening for heart rate data...")
        await asyncio.sleep(600)  # keep alive for 60 seconds
        await client.stop_notify(HRM_CHAR_UUID)

asyncio.run(main())
