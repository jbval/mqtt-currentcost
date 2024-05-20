#!/usr/bin/env python
#
# parse le flux xml d'un compteur de consommation CurrentCost
#

import os
import serial
import xmltodict
import json
import paho.mqtt.client as mqtt

# constantes a modifier
TTYUSB = os.environ.get('TTYUSB') or "/dev/ttyUSB_CURRENTCOST"

MQTT_HOST = os.environ.get('MQTT_HOST') or "192.168.1.144"
MQTT_PORT = int(os.environ.get('MQTT_PORT') or 11884) 
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_TOPIC = os.environ.get('MQTT_TOPIC') or "maison/conso"

# connexion au port serie
ser = None
try:
    ser = serial.Serial(port=TTYUSB, baudrate=57600, timeout=30)
except serial.SerialException as msg:
    print("Failed to connect to CurrentCost meter :: " + str(msg))
    exit(1)
print("Connected to " + TTYUSB)

# connection a mqtt
mqttc = mqtt.Client()
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)


while True:
    # lit le flux xml
    line = ser.readline()
    print(line)
    parsedData = xmltodict.parse(line)
    jsonData = json.dumps(parsedData, indent=2)
    res = None
    # print jsonData
    if jsonData.find("hist") == -1:
        res = mqttc.publish(MQTT_TOPIC + "/realTime", payload=jsonData)
    else:
        res = mqttc.publish(MQTT_TOPIC + "/daily", payload=jsonData)

    if res.rc != mqtt.MQTT_ERR_SUCCESS:
        print("Failed to publish message :: " + str(res.rc))
        mqttc.reconnect()
ser.close()
exit(0)
