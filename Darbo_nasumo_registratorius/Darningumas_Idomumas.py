from datetime import timezone
import datetime
import json
from tkinter import Frame

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


def increase_productivity():
    value = int(lbl_productivity["text"])
    if value < 100:
        lbl_productivity["text"] = f"{value + 1}"


def decrease_productivity():
    value = int(lbl_productivity["text"])
    if value > 0:
        lbl_productivity["text"] = f"{value - 1}"

def increase_interest():
    value = int(lbl_interest["text"])
    if value < 100:
        lbl_interest["text"] = f"{value + 1}"


def decrease_interest():
    value = int(lbl_interest["text"])
    if value > 0:
        lbl_interest["text"] = f"{value - 1}"

def submit():
    productivity_value = int(lbl_productivity["text"])
    interest_value = int(lbl_interest["text"])

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
                "value": productivity_value,
                "state": "good",
                "friendly_name": "Actual productivity",
                "unit": "percent"
            }
        }
        MQTT_TOPIC = "MR10/productivity/"
        MQTT_MSG = json.dumps(transmit_data)
        client.publish(MQTT_TOPIC, MQTT_MSG)

        transmit_data = {
            "device": {
                "name": "MR10",
                "user": lbl_user["text"],
                "type": "data",
                "time": time_str,
            },
            "field": {
                "value": interest_value,
                "state": "good",
                "friendly_name": "Actual interest",
                "unit": "percent"
            }
        }
        MQTT_TOPIC = "MR10/interest/"
        MQTT_MSG = json.dumps(transmit_data)
        client.publish(MQTT_TOPIC, MQTT_MSG)

        client.loop_stop()

    except:
        print("Unable to read data")

window = tk.Tk()
#window.geometry("90x120+300+300")
frame = Frame(window)
frame.pack()

bottomframe = Frame(window)
bottomframe.pack(side = tk.BOTTOM )

middleframe = Frame(window)
middleframe.pack(side = tk.BOTTOM )


lbl_user = tk.Label(master=window, text=USER)
lbl_user.pack(side=tk.TOP)

btn_decrease_productivity = tk.Button(
    master=window,
    text=" - ",
    command=decrease_productivity
)
btn_decrease_productivity.pack(side=tk.LEFT)

lbl_productivity = tk.Label(master=window, text="50")
lbl_productivity.pack(side=tk.LEFT)

btn_increase_productivity = tk.Button(
    master=window,
    text=" + ",
    command=increase_productivity
)
btn_increase_productivity.pack(side=tk.LEFT)

btn_decrease_interest = tk.Button(
    master=window,
    text=" - ",
    command=decrease_interest
)
btn_decrease_interest.pack(side=tk.LEFT)

lbl_interest = tk.Label(master=window, text="50")
lbl_interest.pack(side=tk.LEFT)

btn_increase_interest = tk.Button(
    master=window,
    text=" + ",
    command=increase_interest
)
btn_increase_interest.pack(side=tk.LEFT)

lbl_text = tk.Label(master=middleframe, text="Darbingumas")
lbl_text.pack(side=tk.LEFT)

lbl_text = tk.Label(master=middleframe, text="Įdomumas")
lbl_text.pack(side=tk.RIGHT)

btn_submit = tk.Button(
    master=bottomframe,
    text="Submit",
    command=submit
)
btn_submit.pack(side = tk.BOTTOM)


window.mainloop()
