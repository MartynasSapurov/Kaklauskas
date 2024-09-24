from datetime import timezone
import datetime
import json
import paho.mqtt.client as mqtt
import tkinter as tk

MQTT_HOST = "158.129.192.209"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
USER = "Jevgenijus"

def on_publish(client, userdata, mid):
    print("Message Published...")

def on_connect(client, userdata, flags, rc):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        # we should always subscribe from on_connect callback to be sure
        # our subscribed is persisted across reconnections.
        client.subscribe(MQTT_TOPIC)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "MR11") # client ID "mqtt-test"
client.on_connect = on_connect
client.on_publish = on_publish

client.username_pw_set("vgtu", "dPDIhIs2k0Cb")


def increase():
    value = int(lbl_value["text"])
    if value < 100:
        lbl_value["text"] = f"{value + 1}"


def decrease():
    value = int(lbl_value["text"])
    if value > 0:
        lbl_value["text"] = f"{value - 1}"

def submit():
    value = int(lbl_value["text"])
    try:
        client.connect('158.129.192.209', 1883)
        time_str = str(datetime.datetime.now(timezone.utc))

        transmit_data = {
            "device": {
                "name": "MR10",
                "user": lbl_user["text"],
                "type": "data",
                "time": time_str,
            },
            "field": {
                "value": value,
                "state": "good",
                "friendly_name": "Actual productivity",
                "unit": "percent"
            }
        }
        MQTT_TOPIC = "MR10/productivity/"
        MQTT_MSG = json.dumps(transmit_data)
        client.publish(MQTT_TOPIC, MQTT_MSG)

        client.loop_stop()

    except:
        print("Unable to read data")


window = tk.Tk()
window.geometry("90x50+300+300")

lbl_user = tk.Label(master=window, text=USER)
lbl_user.pack(side=tk.TOP)

btn_decrease = tk.Button(
    master=window,
    text=" - ",
    command=decrease
)
btn_decrease.pack(side=tk.LEFT)

lbl_value = tk.Label(master=window, text="50")
lbl_value.pack(side=tk.LEFT)

btn_increase = tk.Button(
    master=window,
    text=" + ",
    command=increase
)
btn_increase.pack(side=tk.LEFT)

btn_submit = tk.Button(
    master=window,
    text="Submit",
    command=submit
)
btn_submit.pack(side=tk.LEFT)

window.mainloop()
