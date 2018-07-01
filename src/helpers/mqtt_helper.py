import paho.mqtt.client as mqtt
import json


# The callback for when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    # Printing the result code for debugging
    print("Connected with result code " + str(rc))

    # Subscribing to all the topics in on_connect in order
    # to resubscribe if the connection is lost
    client.subscribe("test")

# The callback used for interpreting received messages
def on_message(client, userdata, msg):
    print("Recevied message: topic:" + msg.topic + " - payload:" + str(msg.payload)[1:])

# Creating the client
client = mqtt.Client()

# Assigning the callbacks
client.on_connect = on_connect
client.on_message = on_message

# Parsing connection and authentication details from json
with open('helpers/mqtt_creds.json', 'r') as f:
    creds = json.loads(f.read())

# Setting up the credentials and connecting
client.username_pw_set(creds["username"], creds["password"])
client.connect(creds["host"], creds["port"], 60)
