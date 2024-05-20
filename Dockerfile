FROM python:3.11.9-alpine3.19
RUN pip install pyserial
RUN pip install xmltodict
RUN pip install paho-mqtt

WORKDIR /source
COPY ./GetCurrentCostConso.py ./


ENV MQTT_HOST=""
ENV MQTT_PORT=""
ENV MQTT_TOPIC=""
ENV TTYUSB=""

ENTRYPOINT [ "python", "GetCurrentCostConso.py" ]
