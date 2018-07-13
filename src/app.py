from flask import Flask
from flask import request
# from flask import render_template
import helpers.firebase_helper as firebase
import helpers.mqtt_helper as mqtt
import helpers.secret_parser as secret
from threading import Thread
from time import sleep
# import sys

# --Flask routing--
app = Flask(__name__)

@app.route('/upstream', methods=['POST'])
def handleUpstream():
    type = request.form['type']
    print("[FLASK]--Received POST request on /upstream : type " + type)

    # Store a new device registration id or check if it is registered
    if type == 'registration-id':
        return {
            "request-response" : ""
        }

    # Make a device update:
    #     -register and configure a new device
    #     -update a device's settings
    #     -delete a device from an account
    if type == 'device-update':
        operation = request.form['operation']

        if operation == 'add-new-device':
            return {
                "response" : ""
            }

        else if operation == 'update-status':
            mqtt.publish("status", request.form['status'])
            return {
                "response" : "updated-status"
            }

        else if operation == 'delete-device':
            return {
                "response" : ""
            }

        else
            return {
                "response" : "unknown-operation"
            }

    # Handle the request of:
    #     -device list
    #     -device status(online/offline, on/off)
    #     -preferences?
    # Data is sent back as a Firebase data message
    if type == 'data-request':
        return {
            "response" : ""
        }

    return {
        "response" : "unknown-request"
    }
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
    # flaskThread = Thread(target = runFlask)
    # flaskThread.start()
    #
    # while True:
    #     x = input()
    #     if x == "exit":
    #         print("stopping the server")
    #         sys.exit()
    runFlask()

if (__name__ == "__main__"):
    main()
# ------
