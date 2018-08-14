import paho.mqtt.client as mqtt

import helpers.logging as log


logger = log.Logger()

# A buffer class for keeping incoming messages
class MessageBuffer():
    def __init__(self):
        self.lastItem = -1
        self.bufferTopic = []
        self.bufferPayload = []
    def addMessage(self, topic, payload):
        # print("add message")
        self.bufferTopic.append(topic)
        self.bufferPayload.append(payload)
        self.lastItem += 1
    def getMessage(self):
        if self.lastItem == -1:
            # print("-1")
            return -1
        message = {
            "topic" : self.bufferTopic[0],
            "payload" : self.bufferPayload[0]
        }
        del self.bufferTopic[0]
        del self.bufferPayload[0]
        self.lastItem -= 1
        # print("1")
        return message

# Creating the buffer
messageBuffer = MessageBuffer()

# All the topics that the client will subscribe to
topics = ["test", "conn_status", "status_updates"]

# Creating the client
client = mqtt.Client("server", False)

# CALLBACKS
# The callback for when the client receives a CONNACK response from the server
def onConnect(client, userdata, flags, rc):
    # Printing the result code for debugging
    logger.logMQTT("connected with result code " + str(rc))

    # Subscribing to all the topics in on_connect in order
    # to resubscribe if the connection is lost
    for i in topics:
        client.subscribe(i, 0)

    logger.logMQTT("succefsully subscribed to all the topics")
    return

# The callback used for interpreting received messages
def onMessage(client, userdata, msg):
    # Extracting the topic and the payload
    topic = str(msg.topic)
    payload = str(msg.payload)
    payload = payload[2 : len(payload) - 1]
    messageBuffer.addMessage(topic, payload)

    logger.logMQTT("recevied message:" + topic + " - payload:" + payload)
    return

# Initialize MQTT
def init(host, port, username, password):
    # Assigning the callbacks
    client.on_connect = onConnect
    client.on_message = onMessage
    # Setting up the credentials
    client.username_pw_set(username, password)
    # Connecting
    client.connect(host, port, 60)

    logger.logMQTT("initialized")
    return

# Simple publish function
def publish(topic, payload):
    client.publish(topic, payload)

    logger.logMQTT("published a message to the topic(\"" + topic + "\") with the payload(\"" + payload + "\")")
    return

# Retrieve a message from the buffer
def getMessage():
    # print("get message")
    return messageBuffer.getMessage()
