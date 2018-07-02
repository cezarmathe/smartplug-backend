import paho.mqtt.client as mqtt
import helpers.secret_parser as secret


# The callback for when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    # Printing the result code for debugging
    print("Connected with result code " + str(rc))

    # Subscribing to all the topics in on_connect in order
    # to resubscribe if the connection is lost
    client.subscribe([("test", 0), ("conn_status", 0), ("status_updates", 0)])

# The callback used for interpreting received messages
def on_message(client, userdata, msg):
    print("Recevied message: topic:" + msg.topic + " - payload:" + str(msg.payload)[1:])

# Creating the client
client = mqtt.Client("server", False)

# Assigning the callbacks
client.on_connect = on_connect
client.on_message = on_message

# Parsing connection and authentication details from json
creds = secret.retrieve('mqtt')

# Setting up the credentials
client.username_pw_set(creds["username"], creds["password"])

# Connect to the server
def mqqt_connect():
    client.connect(creds["host"], creds["port"], 60)
    client.publish("test", "succesfully connected")

def publish(topic, payload):
    return
