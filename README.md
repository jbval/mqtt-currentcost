# mqtt-currentcost
Send the currentcost data to a mqtt server
The python script should be install as a daemon/service

Docker compose Example:

services:
  currentcost:
    image: jbval/getcurrentcost2mqtt
    privileged: true
    restart: "unless-stopped"
    container_name: currentcost
    environment:
      - MQTT_HOST=192.168.x.x
      - MQTT_PORT=xxx
      - TTYUSB=/dev/ttyUSB0
    networks:
      - default