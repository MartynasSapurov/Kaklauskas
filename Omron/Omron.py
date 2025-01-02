from datetime import timezone
import datetime
import serial
import json
import paho.mqtt.client as mqtt
import time

def hex2signed(input_hex):
    value = int(input_hex, 16)

    if value > 127:
        value = (value - 128) * (-1)
    return int(value)

def longhex2signed(input_hex):
    value = int(input_hex, 16)

    if value > 32767:
        value = (value - 32768) * (-1)
    return int(value)

MQTT_HOST = "158.129.192.209"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
#MQTT_TOPIC = "MR2/omron/"



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

client = mqtt.Client("MR2") # client ID "mqtt-test"
client.on_connect = on_connect
client.on_publish = on_publish

client.username_pw_set("vgtu", "dPDIhIs2k0Cb")


while True:
    ser = serial.Serial("/dev/ttyACM0", 115200, timeout=3, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS)
    print(ser.name)
    #ser.write(b'\xFE\x00\x00\x00') #Get version
    #ser.write(b'\xFE\x02\x00\x00') #Get cammera angle
    ser.write(b'\xFE\x06\x00\x00') #Get treshhold values
    #ser.write(b'\xFE\x05\x08\x00\xF4\x01\xF4\x01\x4B\x00\xF4\x01') #Set treshhold values
    
    #ser.write(b'\xFE\x04\x03\x00\xFC\x01\x00') #Execute detection


    data = ser.read(6)
    my_header = [hex(item) if len(hex(item)) > 3 else "0x0" + hex(item)[2:] for item in data]
    print(my_header)

    data_lengt = [item for item in my_header[-1:1:-1]]
    data_lengt_str = ''
    for item in data_lengt:
        data_lengt_str+=item[2:]

    data_lengt_int=int(data_lengt_str, 16)

    data = ser.read(data_lengt_int)
    my_data = [hex(item) if len(hex(item)) > 3 else "0x0" + hex(item)[2:] for item in data]

    print(my_data)
    #print(f"Number of detected bodies {my_data[0]}") 
    #print(f"Number of detected hands {my_data[1]}")
    print(f"Number of detected faces {my_data[2]}")
    #print(f"Reserved always 0 {my_data[3]}")
    if data_lengt_int > 4:
        try:
            position_x = int(my_data[5][2:]+my_data[4][2:], 16)
            position_y = int(my_data[7][2:]+my_data[6][2:], 16)
            position_size = int(my_data[9][2:]+my_data[8][2:], 16)
            position_confidence = int(my_data[11][2:]+my_data[10][2:], 16)
            """
            print(f"position_x = {position_x}")
            print(f"position_y = {position_y}")
            print(f"position_size = {position_size}")
            print(f"position_confidence (0 = 1000)= {position_confidence}")
            """
            face_direction_yaw_angle = longhex2signed(my_data[13][2:]+my_data[12][2:])
            face_direction_pich_angle = longhex2signed(my_data[15][2:]+my_data[14][2:])
            face_direction_rall_angle = longhex2signed(my_data[17][2:]+my_data[16][2:])
            face_direction_yaw_confidence = int(my_data[19][2:]+my_data[18][2:], 16)
            """
            print(f"face_direction_yaw_angle = {face_direction_yaw_angle}")
            print(f"face_direction_pich_angle = {face_direction_pich_angle}")
            print(f"face_direction_rall_angle = {face_direction_rall_angle}")
            print(f"face_direction_yaw_confidence (0 = 1000)= {face_direction_yaw_confidence}")
            """
            age_estimation = int(my_data[20], 16)
            age_estimation_confidence = int(my_data[22][2:]+my_data[21][2:], 16)
            """
            print(f"age_estimation = {age_estimation}")
            print(f"age_estimation_confidence (0 = 1000)= {age_estimation_confidence}")
            """
            genre_estimation = int(my_data[23], 16)
            genre_estimation_confidence = int(my_data[25][2:]+my_data[24][2:], 16)
            """
            print(f"genre_estimation (1:Male, 0:Female) = {genre_estimation}")
            print(f"genre_estimation_confidence (0 = 1000)= {genre_estimation_confidence}")
            """
            gaze_estimation_yaw_angle = hex2signed(my_data[26])
            gaze_estimation_pich_angle = hex2signed(my_data[27])
            """
            print(f"gaze_estimation_yaw_angle (-90 - 90) = {gaze_estimation_yaw_angle}")
            print(f"gaze_estimation_pich_angle (-90 - 90) = {gaze_estimation_pich_angle}")
            """
            blink_estimation_degree_left = int(my_data[29][2:]+my_data[28][2:], 16)
            blink_estimation_degree_right = int(my_data[31][2:]+my_data[30][2:], 16)
            """
            print(f"blink_estimation_degree_left (0 = 1000)= {blink_estimation_degree_left}")
            print(f"blink_estimation_degree_right (0 = 1000)= {blink_estimation_degree_right}")
            """
            expression_estimation_neutral = int(my_data[32], 16)
            expression_estimation_happiness = int(my_data[33], 16)
            expression_estimation_surprise = int(my_data[34], 16)
            expression_estimation_anger = int(my_data[35], 16)
            expression_estimation_sadness = int(my_data[36], 16)
            expression_estimation_degree = hex2signed(my_data[37])
            """
            print(f"expression_estimation_neutral (0 - 100) = {expression_estimation_neutral}")
            print(f"expression_estimation_happiness (0 - 100) = {expression_estimation_happiness}")
            print(f"expression_estimation_surprise (0 - 100) = {expression_estimation_surprise}")
            print(f"expression_estimation_anger (0 - 100) = {expression_estimation_anger}")
            print(f"expression_estimation_sadness (0 - 100) = {expression_estimation_sadness}")
            print(f"expression_estimation_degree positive/negative (-100 - 100) = {expression_estimation_degree}")  
            """
            
            client.connect('158.129.192.209', 1883)
            time_str = str(datetime.datetime.now(timezone.utc))
            
            transmit_data = {
            "device":{
                        "name":"MR2",
                        "type":"sensor",
                        "time":time_str,
                     },
            "field":{
                        "value":position_x,
                        "state":"good",
                        "friendly_name":"Position of face center x",
                        "unit":"pixel"
                    }
            }
            MQTT_TOPIC = "MR2/position_x/"
            MQTT_MSG = json.dumps(transmit_data)
            client.publish(MQTT_TOPIC, MQTT_MSG)
            
            transmit_data = {
            "device":{
                        "name":"MR2",
                        "type":"sensor",
                        "time":time_str,
                     },
            "field":{
                        "value":position_y,
                        "state":"good",
                        "friendly_name":"Position of face center y",
                        "unit":"pixel"
                    }
            }
            MQTT_TOPIC = "MR2/position_y/"
            MQTT_MSG = json.dumps(transmit_data)
            client.publish(MQTT_TOPIC, MQTT_MSG)
            
            
            transmit_data = {
            "device":{
                        "name":"MR2",
                        "type":"sensor",
                        "time":time_str,
                     },
            "field":{
                        "value":position_size,
                        "state":"good",
                        "friendly_name":"Size of detected face",
                        "unit":"pixel"
                    }
            }
            MQTT_TOPIC = "MR2/position_size/"
            MQTT_MSG = json.dumps(transmit_data)
            client.publish(MQTT_TOPIC, MQTT_MSG)
            
            transmit_data = {
            "device":{
                        "name":"MR2",
                        "type":"sensor",
                        "time":time_str,
                     },
            "field":{
                        "value":7,
                        "state":"good",
                        "friendly_name":"Face detection confidence (0 - 1000)",
                        "unit":""
                    }
            }
            MQTT_TOPIC = "MR2/position_confidence/"
            MQTT_MSG = json.dumps(transmit_data)
            client.publish(MQTT_TOPIC, MQTT_MSG)
            
            transmit_data = {
            "device":{
                        "name":"MR2",
                        "type":"sensor",
                        "time":time_str,
                     },
            "field":{
                        "value":face_direction_yaw_angle,
                        "state":"good",
                        "friendly_name":"Detected jaw angle (-180 - 179)",
                        "unit":"degree"
                    }
            }
            MQTT_TOPIC = "MR2/face_direction_yaw_angle/"
            MQTT_MSG = json.dumps(transmit_data)
            client.publish(MQTT_TOPIC, MQTT_MSG)
            
            transmit_data = {
            "device":{
                        "name":"MR2",
                        "type":"sensor",
                        "time":time_str,
                     },
            "field":{
                        "value":face_direction_pich_angle,
                        "state":"good",
                        "friendly_name":"Detected pich angle (-180 - 179)",
                        "unit":"degree"
                    }
            }
            MQTT_TOPIC = "MR2/face_direction_pich_angle/"
            MQTT_MSG = json.dumps(transmit_data)
            client.publish(MQTT_TOPIC, MQTT_MSG)
            
            transmit_data = {
            "device":{
                        "name":"MR2",
                        "type":"sensor",
                        "time":time_str,
                     },
            "field":{
                        "value":face_direction_rall_angle,
                        "state":"good",
                        "friendly_name":"Detected rall angle (-180 - 179)",
                        "unit":"degree"
                    }
            }
            MQTT_TOPIC = "MR2/face_direction_rall_angle/"
            MQTT_MSG = json.dumps(transmit_data)
            client.publish(MQTT_TOPIC, MQTT_MSG)
            
            transmit_data = {
            "device":{
                        "name":"MR2",
                        "type":"sensor",
                        "time":time_str,
                     },
            "field":{
                        "value":face_direction_yaw_confidence,
                        "state":"good",
                        "friendly_name":"Face direction detection confidence (0 - 1000)",
                        "unit":""
                    }
            }
            MQTT_TOPIC = "MR2/face_direction_yaw_confidence/"
            MQTT_MSG = json.dumps(transmit_data)
            client.publish(MQTT_TOPIC, MQTT_MSG)
            
            transmit_data = {
            "device":{
                        "name":"MR2",
                        "type":"sensor",
                        "time":time_str,
                     },
            "field":{
                        "value":age_estimation,
                        "state":"good",
                        "friendly_name":"Estimated age",
                        "unit":"year"
                    }
            }
            MQTT_TOPIC = "MR2/age_estimation/"
            MQTT_MSG = json.dumps(transmit_data)
            client.publish(MQTT_TOPIC, MQTT_MSG)
            
            transmit_data = {
            "device":{
                        "name":"MR2",
                        "type":"sensor",
                        "time":time_str,
                     },
            "field":{
                        "value":age_estimation_confidence,
                        "state":"good",
                        "friendly_name":"Age estimation confidence",
                        "unit":""
                    }
            }
            MQTT_TOPIC = "MR2/age_estimation_confidence/"
            MQTT_MSG = json.dumps(transmit_data)
            client.publish(MQTT_TOPIC, MQTT_MSG)
            
            transmit_data = {
            "device":{
                        "name":"MR2",
                        "type":"sensor",
                        "time":time_str,
                     },
            "field":{
                        "value":genre_estimation,
                        "state":"good",
                        "friendly_name":"Estimated genre (Male:1, Female:0)",
                        "unit":""
                    }
            }
            MQTT_TOPIC = "MR2/genre_estimation/"
            MQTT_MSG = json.dumps(transmit_data)
            client.publish(MQTT_TOPIC, MQTT_MSG)
            
            transmit_data = {
            "device":{
                        "name":"MR2",
                        "type":"sensor",
                        "time":time_str,
                     },
            "field":{
                        "value":genre_estimation_confidence,
                        "state":"good",
                        "friendly_name":"Genre estimation confidence (0 - 1000)",
                        "unit":""
                    }
            }
            MQTT_TOPIC = "MR2/genre_estimation_confidence/"
            MQTT_MSG = json.dumps(transmit_data)
            client.publish(MQTT_TOPIC, MQTT_MSG)
            
            transmit_data = {
            "device":{
                        "name":"MR2",
                        "type":"sensor",
                        "time":time_str,
                     },
            "field":{
                        "value":gaze_estimation_yaw_angle,
                        "state":"good",
                        "friendly_name":"Estimated gaze yaw angle (-90 - 90)",
                        "unit":"degree"
                    }
            }
            MQTT_TOPIC = "MR2/gaze_estimation_yaw_angle/"
            MQTT_MSG = json.dumps(transmit_data)
            client.publish(MQTT_TOPIC, MQTT_MSG)
            
            transmit_data = {
            "device":{
                        "name":"MR2",
                        "type":"sensor",
                        "time":time_str,
                     },
            "field":{
                        "value":gaze_estimation_pich_angle,
                        "state":"good",
                        "friendly_name":"Estimated gaze pich angle (-90 - 90)",
                        "unit":"degree"
                    }
            }
            MQTT_TOPIC = "MR2/gaze_estimation_pich_angle/"
            MQTT_MSG = json.dumps(transmit_data)
            client.publish(MQTT_TOPIC, MQTT_MSG)
            
            transmit_data = {
            "device":{
                        "name":"MR2",
                        "type":"sensor",
                        "time":time_str,
                     },
            "field":{
                        "value":blink_estimation_degree_left,
                        "state":"good",
                        "friendly_name":"Blink degree left (0 - 1000)",
                        "unit":""
                    }
            }
            MQTT_TOPIC = "MR2/blink_estimation_degree_left/"
            MQTT_MSG = json.dumps(transmit_data)
            client.publish(MQTT_TOPIC, MQTT_MSG)
            
            transmit_data = {
            "device":{
                        "name":"MR2",
                        "type":"sensor",
                        "time":time_str,
                     },
            "blink_estimation_degree_right":{
                        "value":blink_estimation_degree_right,
                        "state":"good",
                        "friendly_name":"Blink degree right (0 - 1000)",
                        "unit":""
                    }
            }
            MQTT_TOPIC = "MR2/blink_estimation_degree_right/"
            MQTT_MSG = json.dumps(transmit_data)
            client.publish(MQTT_TOPIC, MQTT_MSG)
            
            transmit_data = {
            "device":{
                        "name":"MR2",
                        "type":"sensor",
                        "time":time_str,
                     },
            "field":{
                        "value":expression_estimation_neutral,
                        "state":"good",
                        "friendly_name":"Neutral expression (0 - 100)",
                        "unit":"%"
                    }
            }
            MQTT_TOPIC = "MR2/expression_estimation_neutral/"
            MQTT_MSG = json.dumps(transmit_data)
            client.publish(MQTT_TOPIC, MQTT_MSG)
            
            transmit_data = {
            "device":{
                        "name":"MR2",
                        "type":"sensor",
                        "time":time_str,
                     },
            "field":{
                        "value":expression_estimation_happiness,
                        "state":"good",
                        "friendly_name":"Expression of happiness (0 - 100)",
                        "unit":"%"
                    }
            }
            MQTT_TOPIC = "MR2/expression_estimation_happiness/"
            MQTT_MSG = json.dumps(transmit_data)
            client.publish(MQTT_TOPIC, MQTT_MSG)
            
            transmit_data = {
            "device":{
                        "name":"MR2",
                        "type":"sensor",
                        "time":time_str,
                     },
            "field":{
                        "value":expression_estimation_surprise,
                        "state":"good",
                        "friendly_name":"Surprise expression (0 - 100)",
                        "unit":"%"
                    }
            }
            MQTT_TOPIC = "MR2/expression_estimation_surprise/"
            MQTT_MSG = json.dumps(transmit_data)
            client.publish(MQTT_TOPIC, MQTT_MSG)
            
            transmit_data = {
            "device":{
                        "name":"MR2",
                        "type":"sensor",
                        "time":time_str,
                     },
            "fiedl":{
                        "value":expression_estimation_anger,
                        "state":"good",
                        "friendly_name":"Anger expression (0 - 100)",
                        "unit":"%"
                    }
            }
            MQTT_TOPIC = "MR2/expression_estimation_anger/"
            MQTT_MSG = json.dumps(transmit_data)
            client.publish(MQTT_TOPIC, MQTT_MSG)
            
            transmit_data = {
            "device":{
                        "name":"MR2",
                        "type":"sensor",
                        "time":time_str,
                     },
            "field":{
                        "value":expression_estimation_sadness,
                        "state":"good",
                        "friendly_name":"Expression of sadness (0 - 100)",
                        "unit":"%"
                    }
            }
            MQTT_TOPIC = "MR2/expression_estimation_sadness/"
            MQTT_MSG = json.dumps(transmit_data)
            client.publish(MQTT_TOPIC, MQTT_MSG)
            
            transmit_data = {
            "device":{
                        "name":"MR2",
                        "type":"sensor",
                        "time":time_str,
                     },
            "field":{
                        "value":expression_estimation_degree,
                        "state":"good",
                        "friendly_name":"Positive/negative expression (-100 - 100)",
                        "unit":""
                    }
            }
            MQTT_TOPIC = "MR2/expression_estimation_degree/"
            MQTT_MSG = json.dumps(transmit_data)
            client.publish(MQTT_TOPIC, MQTT_MSG)
            
            client.loop_stop()
            
        except:
            print("Unable to read data")
    time.sleep(3)
