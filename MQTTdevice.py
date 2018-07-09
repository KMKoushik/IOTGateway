import logging
import json
#MQTT package to publish and subscribe messages
import paho.mqtt.client as mqtt

host = "192.168.1.2"
port = 1883


LOG_FILENAME = 'device.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG, format='[%(asctime)s]|[%(levelname)s]|%(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def on_plug_connect(client, userdata, rc):
    logging.info("Connected to MQTT broker")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([("dev1", 0)])


# This function will be called when a message is received in subscribed topics
def on_plug_message(client, userdata, msg):
    print ("Topic: ", msg.topic + "\nMessage: " + str(msg.payload))
    logging.info("----user control message received----")
    userjson = json.loads(msg.payload)

    # recieved message will be in JSON format
    if(userjson["status"]==1):
        print "1"
    if(userjson["status"]==0):
        print "0"


if __name__ == '__main__':
    logging.info("========IOT GATEWAY PROGRAM=======")

    client = mqtt.Client()
    client.on_connect = on_plug_connect
    client.on_message = on_plug_message
    client.connect(host, port)
    client.loop_forever()


