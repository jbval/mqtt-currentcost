#!/usr/bin/env python
#
# parse le flux xml d'un compteur de consommation CurrentCost
#

import os
import requests
import serial
import re
import time
import xmltodict
import json
import paho.mqtt.client as mqtt

# constantes a modifier
TTYUSB = "/dev/ttyUSB_CURRENTCOST"

MQTT_HOST = "192.168.1.144"
MQTT_PORT = 11884
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_TOPIC = "maison/conso"

# connexion au port serie
ser = None
try:
    ser = serial.Serial(port=TTYUSB, baudrate=57600, timeout=30)
except serial.SerialException, msg:
    print("Failed to connect to CurrentCost meter :: " + str(msg))
    exit(1)
print("Connected to " + TTYUSB)

# connection a mqtt 
mqttc = mqtt.Client()
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)


nbIterations = 0

while nbIterations >= 0:
    line = ser.readline()  # lit le flux xml
    print line
    parsedData = xmltodict.parse(line)
    jsonData = json.dumps(parsedData, indent=2)
    
    #print jsonData
    if line.find("hist") == -1:
      	mqttc.publish(MQTT_TOPIC, payload=jsonData)
    else:
      	mqttc.publish(MQTT_TOPIC + "/daily", payload=jsonData)
    nbIterations +=1
ser.close()
exit(0)
