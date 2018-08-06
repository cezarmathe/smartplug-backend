from flask import Flask
from flask import request
# from flask import render_template

import helpers.mqtt_helper as mqtt
import helpers.secret_parser as secret
import helpers.types as types

from threading import Thread
from time import sleep
# import sys

import json

from logzero import logger

# --Flask routing--
app = Flask(__name__)

device_list = {'list' : []}

@app.route('/device', methods=['POST'])
def handleUpstream():

    print(request.json)

    if request.json['type'] == 'DEVICE_LIST_REQUEST':

        global device_list

        return json.dumps(device_list.get('list'))


    if request.json['type'] == 'DEVICE_NEW':

        device_data = request.json['data']

        dl = device_list['list']

        dl.append(device_data)

        device_list['list'] = dl

        print(device_list)

        return "updated device list"

    if request.json['type'] == 'DEVICE_STATUS_UPDATE':

        dv = request.json['data']

        dl = device_list['list']

        for device in dl:

            if (device['id'] == dv['id']):

                device['status'] = dv['status']

                device_list[0] = device

                mqtt.publish("ID" + str(device['id']), str(device['status']))

        return "status update succesful"

# ------

# --Separate thread functions
def runFlask():
    print("[FLASK]--Thread started")
    flaskSecret = secret.retrieve('flask')
    app.run(host=flaskSecret["host"], port=flaskSecret["port"])

def runMqtt():
    print("[MQTT]--Thread started")
    mqttSecret = secret.retrieve('mqtt')
    mqtt.init(mqttSecret["host"], mqttSecret["port"], mqttSecret["username"], mqttSecret["password"])
    mqtt.client.loop_forever()

def runMessageHandler():
    print("[MQTT]--Message handling thread started")
    while True:
        sleep(1)
        v = mqtt.getMessage()
        if v == -1:
            continue
        print("[MQTT]--Handling message:topic \"" + v["topic"] + "\", payload \"" + v["payload"] + "\"")
# ------

# --Main functions
def main():
    mqttThread = Thread(target = runMqtt)
    mqttThread.start()
    msgHandlerThread = Thread(target = runMessageHandler)
    msgHandlerThread.start()

    runFlask()

if (__name__ == "__main__"):
    main()
# ------
