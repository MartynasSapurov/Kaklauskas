from datetime import timezone
import datetime
import serial
import json
import paho.mqtt.client as mqtt

MQTT_HOST = "158.129.192.209"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
#MQTT_TOPIC = "MR1/radar/"

#time_str = str(datetime.datetime.now(timezone.utc))

#MQTT_MSG=json.dumps({"device_id": "radar", "system":  "rpi", "version":  "0.0a", "time":time_str})

def on_publish(client, userdata, mid):
    print("Message Published...")

def on_connect(client, userdata, flags, rc):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        # we should always subscribe from on_connect callback to be sure
        # our subscribed is persisted across reconnections.
        client.subscribe(MQTT_TOPIC)
    
client = mqtt.Client("MR1") # client ID "mqtt-test"
client.on_connect = on_connect
client.on_publish = on_publish

client.username_pw_set("vgtu", "dPDIhIs2k0Cb")
#client.connect('158.129.192.209', 1883)

#client.publish(MQTT_TOPIC, MQTT_MSG)

ser = serial.Serial("/dev/ttyS0", 115200, timeout=3, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS)
print(ser.name)
ser.write(b'\x53\x59\x85\x00\x00\x01\x01\x33\x54\x43')

while(1):
    x = ser.read_until(b'\x54\x43')
    my_list = [hex(item) for item in x]
    #print(my_list)
    try:
        if my_list[2] == hex(7):
            #value = "out of range" if my_list[6] == hex(0) else "in range"
            value = int(my_list[6], 16)
            time_str = str(datetime.datetime.now(timezone.utc))
            transmit_data={
            "device":{
                        "name":"MR1",
                        "type":"sensor",
                        "time":time_str,
                     },
            "field":{
                        "value":position_x,
                        "state":"good",
                        "friendly_name":"Location is in range",
                        "unit":""
                    }
            }
            MQTT_MSG=json.dumps(transmit_data)
            MQTT_TOPIC = "MR1/l_in_re/"
            client.connect('158.129.192.209', 1883)
            client.publish(MQTT_TOPIC, MQTT_MSG)
            client.loop_stop()
            #print(MQTT_MSG)
            #print(f"Value: {my_list}, lenght: {len(my_list)}, parsing: {my_list[2]}")
	
        if my_list[2] == hex(128) and my_list[3] == hex(2):
            """
            if my_list[6] == hex(1):
                value = "Still"
            elif my_list[6] == hex(2):
                value = "Acctive"
            else:
                value = "None"
            """
            value = int(my_list[6], 16)
            time_str = str(datetime.datetime.now(timezone.utc))
            transmit_data={
            "device":{
                        "name":"MR1",
                        "type":"sensor",
                        "time":time_str,
                     },
            "field":{
                        "value":value,
                        "state":"good",
                        "friendly_name":"Human body sports state",
                        "unit":""
                    }
            }
            MQTT_MSG=json.dumps(transmit_data)
            MQTT_TOPIC = "MR1/hb_sport/"
            client.connect('158.129.192.209', 1883)
            client.publish(MQTT_TOPIC, MQTT_MSG)
            client.loop_stop()
            #print(MQTT_MSG)
            #print(f"Human body sports state is {state}")

        if my_list[2] == hex(128) and my_list[3] == hex(3):
            #value = str(int(my_list[6], 16))
            value = int(my_list[6], 16)
            time_str = str(datetime.datetime.now(timezone.utc))
            transmit_data={
            "device":{
                        "name":"MR1",
                        "type":"sensor",
                        "time":time_str,
                     },
            "field":{
                        "value":value,
                        "state":"good",
                        "friendly_name":"Physical activity range (0 - 100)",
                        "unit":"%"
                    }
            }
            MQTT_MSG=json.dumps(transmit_data)
            MQTT_TOPIC = "MR1/ph_active/"
            client.connect('158.129.192.209', 1883)
            client.publish(MQTT_TOPIC, MQTT_MSG)
            client.loop_stop()
            #print(MQTT_MSG)
            #print(f"Physical activity range (0 - 100) is {int(my_list[6], 16)}")
        
        if my_list[2] == hex(128) and my_list[3] == hex(4):
            value = int((my_list[6]+ (my_list[7] if len(my_list[7]) > 3 else "0x0" + my_list[7][2:])[2:]), 16)
            time_str = str(datetime.datetime.now(timezone.utc))
            transmit_data={
            "device":{
                        "name":"MR1",
                        "type":"sensor",
                        "time":time_str,
                     },
            "field":{
                        "value":value,
                        "state":"good",
                        "friendly_name":"Distance in cm (0 - 65535)",
                        "unit":""
                    }
            }
            MQTT_MSG=json.dumps(transmit_data)
            MQTT_TOPIC = "MR1/dist_cm/"
            client.connect('158.129.192.209', 1883)
            client.publish(MQTT_TOPIC, MQTT_MSG)
            client.loop_stop()
            #print(MQTT_MSG)
            #print(f"Distance in cm (0 - 65535) is {value}")
    
        if my_list[2] == hex(129) and my_list[3] == hex(2):
            value = int(my_list[6], 16)
            time_str = str(datetime.datetime.now(timezone.utc))
            transmit_data={
            "device":{
                        "name":"MR1",
                        "type":"sensor",
                        "time":time_str,
                     },
            "field":{
                        "value":value,
                        "state":"good",
                        "friendly_name":"Breath respiratory value (0 - 25)",
                        "unit":""
                    }
            }
            MQTT_MSG=json.dumps(transmit_data)
            MQTT_TOPIC = "MR1/breath/"
            client.connect('158.129.192.209', 1883)
            client.publish(MQTT_TOPIC, MQTT_MSG)
            client.loop_stop()
            #print(MQTT_MSG)
            #print(f"Breath respiratory value (0 - 25): {value}")
    
        if my_list[2] == hex(133) and my_list[3] == hex(2):
            value = int(my_list[6], 16)
            time_str = str(datetime.datetime.now(timezone.utc))
            transmit_data={
            "device":{
                        "name":"MR1",
                        "type":"sensor",
                        "time":time_str,
                     },
            "field":{
                        "value":value,
                        "state":"good",
                        "friendly_name":"Heart beat rate value (1 - 100)",
                        "unit":""
                    }
            }
            MQTT_MSG=json.dumps(transmit_data)
            MQTT_TOPIC = "MR1/heart/"
            client.connect('158.129.192.209', 1883)
            client.publish(MQTT_TOPIC, MQTT_MSG)
            client.loop_stop()
            #print(MQTT_MSG)
            #print(f"Heart rate value (1 - 100): {value}")
    except:
        print(f"Unable to read data{my_list}")
ser.close()
