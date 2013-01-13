#!/usr/bin/env python
# -*- coding: utf-8 -*
from xml.dom import minidom
# import RPi.GPIO as GPIO

class Config:

    def getConfig(self):
        config = []
        DOMTree = minidom.parse("ioconfig.xml")
        nodes = DOMTree.childNodes

        for i in nodes[0].getElementsByTagName("pin"):
            pinConf = {}
            for elem in i.childNodes:
                if elem.nodeType == elem.ELEMENT_NODE:
                    pinConf[elem.localName] = elem.childNodes[0].toxml()

            config.append(pinConf)
        return config

    def configureGPIO(self, config):
	# GPIO.setmode(GPIO.BOARD)
        for pin in config:
            if "direction" in pin:
                id = pin["id"]
                direction = pin["direction"]
                if direction == "IN":
                    print("IN")
                    # GPIO.setup(int(id), GPIO.IN)
                else:
                    print("OUT")
                    # GPIO.setup(int(id), GPIO.OUT)
                    if pin["state"]:
                        print("state")
                        # GPIO.output(int(id), GPIO.HIGH)