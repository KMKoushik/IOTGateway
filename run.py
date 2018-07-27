from device import MqttDevice,BluetoothDevice,XbeeDevice,SqlDb,sensor
import logging
import json
import smtplib
import time


#MQTT package to publish and subscribe messages
import paho.mqtt.client as mqtt
import os


host = "avesorg.ddns.net"
port = 1883


LOG_FILENAME = 'gateway.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG, format='[%(asctime)s]|[%(levelname)s]|%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
host = "localhost"
port = 1883
scheduledata={}
mqttpub= mqtt.Client("python_pub")


def on_hub_connect(client, userdata, rc):
    logging.info("Connected to MQTT broker")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([("control/send", 0),("givedata", 0),("sensordata", 0)])



def on_hub_message(client, userdata, msg):
    """This function will be called when a message is received in subscribed topics"""

    print ("Topic: ", msg.topic + "\nMessage: " + str(msg.payload))
    if(msg.topic=='control/send'):
        logging.info("----user configure message received----")
        userjson = json.loads(msg.payload)
        userlist = [userjson['device_type'], userjson['device_name'], userjson['status']]
        # recieved message will be in JSON format
        db=SqlDb()
        db.updateData(userlist[1],userlist[2])
        if (userlist[0]=='MQTT'): # Send message to MQTT device
            dev=MqttDevice()
            dev.sendMessage(userlist[1],"{\"status\":"+userlist[2]+"}")
            del dev

        if(userlist[0]=='xbee'): # Send message to XBEE device
            dev=XbeeDevice()
            dev.sendMessage(userlist[2])
            #del dev

        if (userlist[0] == 'bluetooth'): # Send message to bluetooth device
            dev = BluetoothDevice()
            dev.sendMessage(userlist[2])
            #del dev
    if(msg.topic=='givedata'):
        db=SqlDb()
        result=db.getData()
        print result[2],result[3]
        mqttpub.connect(host, port, 60)
        mqttpub.publish("getdata",str(result[2])+","+str(result[3]))
        mqttpub.disconnect()

    if (msg.topic == 'sensordata'):
        sch = sensor()
        sensorVal=sch.getData()
        mqttpub.connect(host, port, 60)
        mqttpub.publish("sensorreply",sensorVal )
        mqttpub.disconnect()




if __name__ == '__main__':
    logging.info("========IOT GATEWAY PROGRAM=======")
    #os.system("sudo rfcomm bind hci0 98:D3:32:20:4F:B9 1") #use this line first time ....used to connnect with bluetooth
    

    #sch = sensor()
    #sch.start()
    client = mqtt.Client()
    client.on_connect = on_hub_connect
    client.on_message = on_hub_message
    client.connect(host, port)
    client.loop_forever()

