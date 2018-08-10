from flask import Flask
from flask import request, abort
# from flask import render_template

import helpers.mqtt_helper as mqtt
import helpers.secret_parser as secret

from threading import Thread
from time import sleep
# import sys

import json

import logzero
from logzero import logger

# --end imports


# --variables

app = Flask(__name__)

# --end variables


# --Flask routing------------------------------------------------

# LOGIN
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True)
    if data == None:
        abort(400)
    username = data['username']
    pass
    return

# USER
@app.route('/user', methods=['GET'])
def userGet():
    return 'forbidden', 403

@app.route('/user', methods=['POST'])
def userPost():
    return 'forbidden', 403

@app.route('/user', methods=['PUT'])
def userPut():
    return 'forbidden', 403

@app.route('/user', methods=['DELETE'])
def userDelete():
    return 'forbidden', 403
# end USER



# ---------------------------------------------------------------


# --MQTT message handling

def runMessageHandler():
    print("[MQTT]--Message handling thread started")
    while True:
        sleep(1)
        v = mqtt.getMessage()
        if v == -1:
            continue
        print("[MQTT]--Handling message:topic \"" + v["topic"] + "\", payload \"" + v["payload"] + "\"")

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

# ------


# --Main functions
def main():
    logzero.logfile('logs/latest.log')
    mqttThread = Thread(target = runMqtt)
    mqttThread.start()
    msgHandlerThread = Thread(target = runMessageHandler)
    msgHandlerThread.start()

    logger.info("working")

    runFlask()

if (__name__ == "__main__"):
    main()
# ------
