from flask import Flask
from flask import request, abort
# from flask import render_template

import helpers.mqtt as mqtt
import helpers.secret_parser as secret
import helpers.logging as logging
import db.db_helper as db
import helpers.token as tk

from threading import Thread
from time import sleep
import secrets
# import sys

import json

# --end imports


# --variables

app = Flask(__name__)

logger = logging.Logger()

tokens = tk.TokenUtility(logger)

database = db.Database(tokens, logger)

# --end variables


# --Flask routing------------------------------------------------

# USER

@app.route('/user', methods=['GET'])
def userGet():
    logger.logRouting("/user", "GET", "received the request")

    data = request.get_json(silent=True)
    logger.logRouting("/user", "GET", "extracted JSON")

    if data == None:
        logger.logRouting("/user", "GET", "no payload")
        abort(400)

    logger.logRouting("/user", "GET", "payload exists")

    email = data['email']
    password = data['password']
    logger.logRouting("/user", "GET", "payload conforms to standards")

    user = database.checkUser(email, password)

    if (user != False):
        logger.logRouting("/user", "GET", "valid credentials")
        return user, 200
    else:
        logger.logRouting("/user", "GET", "invalid credentials")
        return "forbidden", 403


@app.route('/user', methods=['POST'])
def userPost():
    logger.logRouting("/user", "POST", "received the request")

    data = request.get_json(silent=True)
    logger.logRouting("/user", "POST", "extracted JSON")

    if data == None:
        logger.logRouting("/user", "POST", "no payload")
        abort(400)

    logger.logRouting("/user", "POST", "payload exists")

    email = data['email']
    password = data['password']
    logger.logRouting("/user", "POST", "payload conforms to standards")

    result = database.checkUser(email, password)

    if (result == False):
        logger.logRouting("/user", "POST", "user already exists")
        return "conflict", 409
    else:
        logger.logRouting("/user", "POST", "user creation was succesful")
        return database.createUser(email, password)


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
    token = tokens.extractToken(request)
    user = database.getUserFromToken(token)

    if (user == None):
        return 'forbidden', 403

    device_list = database.getDeviceList(user[0])

    # convert to json
    return device_list, 200

@app.route('/device', methods=['POST'])
def devicePost():
    token = tokens.extractToken(request)
    user_id = database.getUserFromToken(token)[0]

    data = request.get_json(silent=True)
    if (data == None):
        return 'bad request', 400

    name = data['name']

    id = database.createDevice(name, user_id)

    return id, 200

@app.route('/device', methods=['PUT'])
def devicePut():
    token = tokens.extractToken(request)
    user = database.getUserFromToken(token)

    data = request.get_json(silent=True)
    if (data == None):
        return 'bad request', 400

    if (user == None):
        return 'forbidden', 403

    user_id = user[0]
    device_id = data['id']
    device_name = data['name']

    # update device --------------------------------------

@app.route('/device/status', methods=['PUT'])
def devicePut():
    token = tokens.extractToken(request)
    user = database.getUserFromToken(token)

    data = request.get_json(silent=True)
    if (data == None):
        return 'bad request', 400

    if (user == None):
        return 'forbidden', 403

    user_id = user[0]
    device_id = data['id']
    device_status = data['status']

    # update device status ---------------------------------

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

    tokens.set_signature(secret.retrieve('signature')['signature'])

    mqttThread = Thread(target = runMqtt)
    mqttThread.start()

    msgHandlerThread = Thread(target = runMessageHandler)
    msgHandlerThread.start()

    logger.logInfo("finished main()")

    runFlask()

if (__name__ == "__main__"):
    main()
# ------
