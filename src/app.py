from flask import Flask
from flask import request
# from flask import render_template
import helpers.firebase_helper as fcm
import helpers.mqtt_helper as mqtt
import helpers.secret_parser as secret
from threading import Thread
from time import sleep
import sys

# --Flask routing--
app = Flask(__name__)

@app.route('/upstream', methods=['POST'])
def handleUpstream():
    # type = request.form['type']
    # if type == 'registration_id':
    #     return ''
    # if type == 'status_change':
    #     mqtt.publish("status", request.form['status'])
    #     return 'received status:' + request.form['status']
    # return 'unknown type'
    mqtt.publish("status", request.form['status'])
    return 'received status update'
# ------

# --Separate thread functions
def runFlask():
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
