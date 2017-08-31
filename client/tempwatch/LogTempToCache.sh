#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import fnmatch
import logging
import MySQLdb as mdb
import ConfigParser

# Load the modules (not required if they are loaded at boot) 
# os.system('modprobe w1-gpio')
# os.system('modprobe w1-therm')

SQL_INSERT = "INSERT INTO tempvalues(sensor_id, temp_value, log_date) VALUES (%s, %s, NOW())"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = BASE_DIR + "/tempwatch.ini"

# Setup logging
logging.basicConfig(filename= BASE_DIR + "/logs/LogTempToCache.log",
  level=logging.DEBUG,
  format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger=logging.getLogger(__name__)

def getDbConfig():
    
    logger.info("Reading config from {0}".format(CONFIG_FILE))
    
    Config = ConfigParser.ConfigParser()
    Config.read(CONFIG_FILE)

    dbconf = {}

    dbconf['host'] = Config.get("Database", "host")
    dbconf['db'] = Config.get("Database", "name")
    dbconf['user'] = Config.get("Database", "user")
    dbconf['passwd'] = Config.get("Database", "password")
    
    return dbconf

def readTempSensors():
    
    readings = []
    
    logger.info("Reading temp probes...")
    
    for sensorId in os.listdir("/sys/bus/w1/devices"):
        if fnmatch.fnmatch(sensorId, "28-*"):
            with open("/sys/bus/w1/devices/" + sensorId + "/w1_slave") as f_obj:
                lines = f_obj.readlines()
                if lines[0].find("YES"):
                    pok = lines[1].find("=")
                    tempValue = float(lines[1][pok+1:pok+6])/1000
                    readings.append(dict(sensor = sensorId, temp = tempValue))
                    logger.info("Read sensor {0}".format(sensorId))
                else:
                    logger.error("Error reading sensor with ID: {0}".format(sensorId))
    logger.info("Got {0} readings from probes".format(len(readings)))
    return readings

try:
    logger.info("Starting temp reading...")
    
    # Get config
    dbConfig = getDbConfig()
    
    # Read temp sensors
    tempReadings = readTempSensors()
    
    # Write readings to database
    logger.info("Writing temp readings to db...")
    con = mdb.connect(host=dbConfig['host'], user=dbConfig['user'], passwd=dbConfig['passwd'],db = dbConfig['db'])
    cursor = con.cursor()

    for tempReading in tempReadings:
        cursor.execute(SQL_INSERT, (tempReading['sensor'], float(tempReading['temp'])))

    con.commit()
    con.close()

    logger.info("Inserted {0} temp readings in db".format(len(tempReadings)))
    
except mdb.Error, e:
    logger.error("An error occured!")
    logger.error(e)

