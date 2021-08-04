# growatt-modbus

This python script reads a Growatt inverter over the Modbus RS485 RTU Protocol every 10 seconds. If the invert is working normally, the script sends the following data to the MQTT broker:
- total output
- current output

Works with a Growatt 6000 TL3-S, but it may work with other inverters as well.

Please change the values in config.yaml to match your setup.
