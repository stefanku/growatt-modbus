# growatt-modbus

This python script reads a Growatt inverter over the Modbus RS485 RTU Protocol every 60 seconds. It sends the inverter's status (working normally, waiting or error) and total output to a MQTT broker. 
Works with a Growatt 6000 TL3-S, but it may work with other inverters as well.

Please change the values in config.yaml to match your setup.
