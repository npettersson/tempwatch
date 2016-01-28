#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import fnmatch
import time
import logging

BASE_DIR = "/home/pi/tempwatch"

logging.basicConfig(filename= BASE_DIR + "/logs/DS18B20_error.log",
  level=logging.DEBUG,
  format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger=logging.getLogger(__name__)

tempLogFile = BASE_DIR + "/tempData.log"

# Load the modules (not required if they are loaded at boot) 
# os.system('modprobe w1-gpio')
# os.system('modprobe w1-therm')

# Get readings from sensors and store them in a file

tempValues = []
sensorIds = []

timeString  = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())


# Read temp sensors
for filename in os.listdir("/sys/bus/w1/devices"):
  if fnmatch.fnmatch(filename, "28-*"):
    with open("/sys/bus/w1/devices/" + filename + "/w1_slave") as f_obj:
      lines = f_obj.readlines()
      if lines[0].find("YES"):
        pok = lines[1].find("=")
        tempValues.append(float(lines[1][pok+1:pok+6])/1000)
        sensorIds.append(filename)
      else:
        logger.error("Error reading sensor with ID: {0}".format(filename))

# Write values to file
if (len(tempValues)>0):
  writeMode = "a" if os.path.exists(tempLogFile) else "w"
  with open(tempLogFile, writeMode) as logFile:
    for i in range(0,len(tempValues)):
      logFile.write("{0};{1};{2}\n".format(timeString, sensorIds[i], tempValues[i]))
