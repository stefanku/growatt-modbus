#!/usr/bin/env python3

# Imports
import time
from paho.mqtt import client as mqtt_client
import minimalmodbus
import yaml

# Function to read config
def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

# Read config
config = read_yaml("config.yaml")

# MQTT settings
broker = config["mqtt"]["broker"]
port = config["mqtt"]["port"]
topic_prefix = config["mqtt"]["topic_prefix"]
client_id = config["mqtt"]["client_id"]
username = config["mqtt"]["username"]
password = config["mqtt"]["password"]

# Modbus settings
instrument = minimalmodbus.Instrument(config["modbus"]["port"], 1)  # port name, slave address (in decimal)
instrument.serial.baudrate = config["modbus"]["baudrate"]
instrument.serial.bytesize = config["modbus"]["bytesize"]
instrument.serial.stopbits = config["modbus"]["stopbits"]
instrument.serial.timeout  = config["modbus"]["timeout"]
instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
instrument.clear_buffers_before_each_transaction = True

# MQTT Callback function
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker")
        else:
            print("Failed to connect, return code %d\n.", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

# Initial setting of online variablele
online = False

# Publish messages
def publish(client):
    while True:
        try:
            inverter_status = instrument.read_register(0, 0, 4, False)
            online = True
            print("Growatt is online")
            if inverter_status == 1:
               status = "ok"
            if inverter_status == 0:
               status = "waiting"
            if inverter_status == 3:
               status = "error"
            msg = status
            topic = topic_prefix + "/status"
            result = client.publish(topic, msg)
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")
        except:
            online = False
            print("Growatt is offline")
        msg = str(online).lower()
        topic = topic_prefix + "/online"
        result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        total_output_kwh = instrument.read_register(27, 1, 4, False)  # Registernumber, number of decimals, function code, signed? 
        msg = total_output_kwh
        topic = topic_prefix + "/total_output_kwh"
        result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
           print(f"Send `{msg}` to topic `{topic}`")
        else:
           print(f"Failed to send message to topic {topic}")
        time.sleep(60)

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
