from flask import Flask
from flask import request
# from flask import render_template
import helpers.firebase_helper as fcm
import helpers.mqtt_helper as mqtt
from threading import Thread
from time import sleep

def runMqtt():
    print("[MQTT]--Thread started")
    mqtt.init()
    mqtt.client.loop_forever()
    # while True:
    #     sleep(50)
    #     v = mqtt.getMessage()
    #     if v == 0:
    #         continue
    #     print(v["topic"] + "->" + v["payload"])

app = Flask(__name__)

@app.route('/upstream', methods=['POST'])
def handleUpstream():
    type = request.form['type']
    if type == 'registration_id':
        return
    if type == 'status_change':
        return
    return 'unknown type'

def main():
    mqttThread = Thread(target = runMqtt)
    mqttThread.start()
    # thread.join()
    app.run(host='192.168.0.157', port='1234')

if (__name__ == "__main__"):
    main()









# fb.print_result()
#
# mqtt.mqqt_connect()
# mqtt.client.loop_forever()
