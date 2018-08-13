from flask import Flask
from flask import request, abort
# from flask import render_template

import helpers.mqtt as mqtt
import helpers.secret_parser as secret
import helpers.logging as logging
import db.db_helper as db

from threading import Thread
from time import sleep
# import sys

import json

# --end imports


# --variables

app = Flask(__name__)

logger = logging.Logger()

database = db.Database()

tokens = TokenUtility()

# --end variables


# --Flask routing------------------------------------------------

# USER

@app.route('/user', methods=['GET'])
def userGet():
    data = request.get_json(silent=True)
    if data == None:
        abort(400)
    email = data['email']
    password = data['password']

    if (database.checkUser(email, password)):
        return database.getToken(email)
    else:
        return "forbidden"
        abort(403)


@app.route('/user', methods=['POST'])
def userPost():
    data = request.get_json(silent=True)
    if data == None:
        abort(400)
    email = data['email']
    password = data['password']

    if (database.createUser(email, password)):
        return tokens.createToken(email)
    else:
        return "conflict"
        abort(409)

@app.route('/user', methods=['PUT'])
def userPut():
    return 'forbidden', 403

@app.route('/user', methods=['DELETE'])
def userDelete():
    return 'forbidden', 403

# end USER


# DEVICE

@app.route('/device', methods=['GET'])
def deficeGet():
    return 'forbidden', 403

@app.route('/device', methods=['POST'])
def devicePost():
    return 'forbidden', 403

@app.route('/device', methods=['PUT'])
def devicePut():
    return 'forbidden', 403

@app.route('/device', methods=['DELETE'])
def deviceDelete():
    return 'forbidden', 403

# end DEVICE


# GROUP

@app.route('/group', methods=['GET'])
def groupGet():
    return 'forbidden', 403

@app.route('/group', methods=['POST'])
def groupPost():
    return 'forbidden', 403

@app.route('/group', methods=['PUT'])
def groupPut():
    return 'forbidden', 403

@app.route('/group', methods=['DELETE'])
def groupDelete():
    return 'forbidden', 403

# end GROUP



# ---------------------------------------------------------------


# --MQTT message handling

def runMessageHandler():
    logger.logMQTTMsg("thread started")
    while True:
        sleep(1)
        v = mqtt.getMessage()
        if v == -1:
            continue
        # print("[MQTT]--Handling message:topic \"" + v["topic"] + "\", payload \"" + v["payload"] + "\"")
        logger.logMQTTMsg("received message:topic \"" + v["topic"] + "\", payload \"" + v["payload"] + "\"")

# ------


# --Separate thread functions
def runFlask():
    logger.logFlask("thread started")
    flaskSecret = secret.retrieve('flask')
    app.run(host=flaskSecret["host"], port=flaskSecret["port"])

def runMqtt():
    logger.logMQTT("thread started")
    mqttSecret = secret.retrieve('mqtt')
    mqtt.init(mqttSecret["host"], mqttSecret["port"], mqttSecret["username"], mqttSecret["password"])
    mqtt.client.loop_forever()

# ------


# --Main functions
def main():

    tokens.set_signature(secret.retrieve('signature')[signature])

    mqttThread = Thread(target = runMqtt)
    mqttThread.start()

    msgHandlerThread = Thread(target = runMessageHandler)
    msgHandlerThread.start()

    logger.logInfo("finished main()")

    runFlask()

if (__name__ == "__main__"):
    main()
# ------
