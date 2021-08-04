#!/usr/bin/env python3

# Which register value?
value = 12

# How many decimals
decimals = 1

# Imports
import minimalmodbus
import yaml
import os

# Function to read config
def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

# Load config file
config = read_yaml(os.path.dirname(os.path.realpath(__file__)) + "/config.yaml")

# Modbus settings (reading from config file)
instrument = minimalmodbus.Instrument(config["modbus"]["port"], 1)  # port name, slave address (in decimal)
instrument.serial.baudrate = config["modbus"]["baudrate"]
instrument.serial.bytesize = config["modbus"]["bytesize"]
instrument.serial.stopbits = config["modbus"]["stopbits"]
instrument.serial.timeout  = config["modbus"]["timeout"]
instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
instrument.clear_buffers_before_each_transaction = True

# Print single register value
print(instrument.read_register(value, decimals, 4, False))
