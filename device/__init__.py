import threading
import logging
import serial
import MySQLdb
#import picamera
import time
#import picamera
from datetime import datetime
import json
#MQTT package to publish and subscribe messages
import paho.mqtt.client as mqtt
import os


LOG_FILENAME = 'gateway.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG, format='[%(asctime)s]|[%(levelname)s]|%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
class MqttDevice:

    def __init__(self):
        logging.info('MQTT device initialized')
        self.host = "localhost"
        self.port = 1883
        self.scheduledata = {}
        self.mqttpub = mqtt.Client("python_pub")

    def sendMessage(self,topic,jsonMessage):
        try:
            self.mqttpub.connect(self.host, self.port, 60)
            self.mqttpub.publish(topic,jsonMessage)
            self.mqttpub.disconnect()
            logging.info("MQTT message sent to device")
        except Exception as e:
            logging.error("Error in the address or port")


class BluetoothDevice:

    def __init__(self):
        try:
            logging.info("Bluetoooh message received")
        except Exception as e:
            logging.error("Error initializing the bluetooth check MAC ID")

    def sendMessage(self,message):
        try:
            self.ser = serial.Serial('/dev/ttyUSB0', 9600)
            if(message=="1"):
                message="4"
                print message
            elif(message=="0"):
                message="3"
                print message
            self.ser.write(message)
            logging.info("xbee message sent to device")
        except Exception as e:
            logging.error("Error in sending xbee message:"+e.message)

    def __del__(self):
        self.ser.close()

class XbeeDevice:

    def init_(self):
        try:

            logging.info("Xbee is configured")
        except Exception as e:
            logging.error("Error initializing the xbee device")

    def sendMessage(self,message):
        try:
            self.ser = serial.Serial('/dev/ttyUSB0', 9600)
            self.ser.write(message)
            logging.info("xbee message sent to device")
        except Exception as e:
            logging.error("Error in sending xbee message:"+e.message)

    def __del__(self):
        self.ser.close()


class SqlDb:

    def __init__(self):
        self.db = MySQLdb.connect("localhost", "root", "aves", "aves")   # (IP,mysql-user,PWD,DBname) to connect with mysql DB
        self.cursor = self.db.cursor()   # Object to execute SQL commands

    def updateData(self,dev,status):
        try:
           self.cursor.execute("update gateway set "+dev+"="+status+" where sl_no=1")
           self.db.commit()
           logging.info("PRODUCT DATA UPDATED")
           return 1
        except Exception as e:
            logging.error("PRODUCT UPDATION ERROR" + e.message)
            return 0

    def getData(self):
        try:
            self.cursor.execute("select * from gateway where sl_no=1")
            queryResult = self.cursor.fetchall()
            print queryResult[0]
            return queryResult[0]
        except Exception as e:
            return 0
            logging.error("login failed")


class sensor(threading.Thread):
    sensorVal = ""

    def __init__(self):
        logging.info('sensor thread  started')
        self.ser = serial.Serial('/dev/ttyACM0', 9600)
        #self.camera=picamera.PiCamera()
        threading.Thread.__init__(self)

    def run(self):
        while 1:
            sensor.sensorVal = self.ser.readline()
            sensorlist=sensor.sensorVal.split(",")
            print sensorlist
            print (len(sensorlist))
            if(len(sensorlist)>=3):
                if(int(sensorlist[0])>40):
                    print "High temperature detected"
                if (int(sensorlist[1]) > 350):
                    print "High gas  detected"
                if (int(sensorlist[2]) == 0):
                    logging.info( "High gas  detected")
                    timestr = time.strftime("%Y-%m-%d-%H:%M:%S")
                    #self.camera.capture("/var/lib/tomcat8/webapps/hyttetech/photos/"+timestr+".jpg")
                    print timestr

    def getData(self):
        print sensor.sensorVal
        return sensor.sensorVal





  










