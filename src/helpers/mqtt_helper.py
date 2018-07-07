import paho.mqtt.client as mqtt
import helpers.secret_parser as secret

# All the topics that the client will subscribe to
topics = ["test", "conn_status", "status_updates"]

# The MQTT message buffer
# global bufferStatusTopic
# global bufferStatusPayload
# global lastItem

# Creating the client
client = mqtt.Client("server", False)

# CALLBACKS
# The callback for when the client receives a CONNACK response from the server
def onConnect(client, userdata, flags, rc):
    # Printing the result code for debugging
    print("[MQTT]--Connected with result code " + str(rc))

    # Subscribing to all the topics in on_connect in order
    # to resubscribe if the connection is lost
    for i in topics:
        client.subscribe(i, 0)

    print("[MQTT]--Succefsully subscribed to all the topics")
    return

# The callback used for interpreting received messages
def onMessage(client, userdata, msg):
    # Extracting the topic and the payload
    topic = str(msg.topic)
    payload = str(msg.payload)
    payload = payload[2 : len(payload) - 1]
    # updateBuffer(topic, payload)

    print("[MQTT]--Recevied message:" + topic + " - payload:" + payload)
    return

# Initialize MQTT
def init():
    # lastItem = -1
    # bufferStatusTopic = list()
    # bufferStatusPayload = list()
    # Assigning the callbacks
    client.on_connect = onConnect
    client.on_message = onMessage
    # Parsing connection and authentication details from json
    creds = secret.retrieve('mqtt')
    # Setting up the credentials
    client.username_pw_set(creds["username"], creds["password"])
    # Connecting
    client.connect(creds["host"], creds["port"], 60)

    print("[MQTT]--Initialized")
    return

# Simple publish function
def publish(topic, payload):
    client.publish(topic, payload)

    print("[MQTT]Published a message to the topic(" + topic + ") with the payload(" + topic + ")")
    return

# def updateBuffer(topic, payload):
#     # Updating the buffer
#     lastItem += 1
#     bufferStatusTopic.append(topic)
#     bufferStatusPayload.append(payload)

# Retrieve a message from the bufferStatus
# def getMessage():
#     # Checking the bufferStatus
#     # If the bufferStatus is empty, returns 0
#     if lastItem == -1:
#         return lastItem
#     # Otherwise, creating a message as a dictionary
#     message = {"topic" : bufferStatusTopic[0],
#                "payload" : bufferStatusPayload[0]
#     }
#     # Then, we delete the message from the bufferStatus
#     del bufferStatusTopic[0]
#     del bufferStatusPayload[0]
#     lastItem -= 1
#     return message
