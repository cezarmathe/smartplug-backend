from flask import Flask
from flask import request, abort
# from flask import render_template

import helpers.mqtt as mqtt
import helpers.secret_parser as secret
import helpers.logging as logging
import db.db_helper as db
import helpers.token as tk
import helpers.serializer as serializer

from threading import Thread
from time import sleep
# import secrets
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

    email = request.args.get('email')
    password = request.args.get('password')

    if (email == None or password == None):
        return "bad request", 400

    logger.logRouting("/user", "GET", "payload conforms to standards")

    user = database.checkUser(email, password, False)

    if (user != False):
        logger.logRouting("/user", "GET", "valid credentials")
        return user[5], 200
    else:
        logger.logRouting("/user", "GET", "invalid credentials")
        return "invalid", 409


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

    result = database.checkUser(email, password, True)

    if (result == False):
        logger.logRouting("/user", "POST", "user already exists")
        return "conflict", 409
    else:
        logger.logRouting("/user", "POST", "user creation was succesful")
        return database.createUser(email, password)


@app.route('/user', methods=['PUT'])
def userPut():
    return "forbidden", 403

@app.route('/user', methods=['DELETE'])
def userDelete():
    return 'forbidden', 403

# end USER


# DEVICE

@app.route('/device', methods=['GET'])
def deviceGet():
    token = tokens.extractToken(request)
    user = database.getUserFromToken(token)
    if (user == None):
        return 'forbidden', 403
    device_list = serializer.serializeDeviceList(database.getDeviceList(user[0][0]))

    # convert to json
    return json.dumps(device_list['list']), 200


@app.route('/device', methods=['POST'])
def devicePost():
    token = tokens.extractToken(request)
    user_id = database.getUserFromToken(token)[0][0]

    data = request.get_json(silent=True)
    args = request.args

    if (data == None and args == None):
        return 'bad request', 400

    elif(data == None):
        print(args.get('id') + "-" + args.get('user_id'))
        return "device permissions", 200
    else:
        name = data['name']

        id = database.createDevice(name, user_id)

        return str(id), 200


@app.route('/device/adduser', methods=['POST'])
def deviceAddUser():
    token = tokens.extractToken(request)
    user = database.getUserFromToken(token)[0][0]

    args = request.args

    if (args == None):
        abort(400)

    device_id = args.get("device_id")
    user_id = args.get("user_id")
    if (database.checkDeviceOwnership(device_id, user) == False):
        abort(409)

    database.addDeviceUserPair(device_id, user_id)

    return "added", 200



@app.route('/device', methods=['PUT'])
def devicePutStatus():
    logger.logRouting("/device", "PUT", "update device status")
    token = tokens.extractToken(request)
    user = database.getUserFromToken(token)

    id = request.args.get('id')
    status = request.args.get('status')

    if (status == 'true'):
        status = 1
    elif (status == 'false'):
        status = 0

    if (status == None or id == None):
        return 'bad request', 400

    if (user == None):
        return 'forbidden', 403

    user_id = user[0][0]

    database.updateDeviceStatus(id, status)

    mqtt.publish(str(id), str(status))

    return "succes", 200

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

        if (v["topic"] == "GET_FINAL_ID"):
            email = v["payload"]
            user = database.checkUserEmail(email)[0][0]

            dev_final_id = database.createDevice("temp", user)

            mqtt.publish("id", str(dev_final_id))


# ------


# --Separate thread functions
def runFlask():
    logger.logFlask("thread started")
    flaskSecret = secret.retrieve('flask')
    app.run(host=flaskSecret["host"])

# ------


# --Main functions
def main():

    tokens.set_signature(secret.retrieve('signature')['signature'])

    logger.logMQTT("thread started")
    mqttSecret = secret.retrieve('mqtt')
    mqtt.init(mqttSecret["host"], mqttSecret["port"], mqttSecret["username"], mqttSecret["password"])

    mqttThread = Thread(target = mqtt.client.loop_forever)
    mqttThread.start()

    mqtt.client.loop_forever()

    msgHandlerThread = Thread(target = runMessageHandler)
    msgHandlerThread.start()

    logger.logInfo("finished main()")

    runFlask()

if (__name__ == "__main__"):
    main()
# ------
