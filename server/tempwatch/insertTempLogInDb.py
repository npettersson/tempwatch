#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import time
import logging
import fnmatch
import MySQLdb as mdb
import shutil

BASE_DIR = "/home/pi/tempwatch"

logging.basicConfig(filename= BASE_DIR + "/logs/insert.log",
  level=logging.INFO,
  format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger=logging.getLogger(__name__)

STAGE_DIR = BASE_DIR + "/stage"
PROCESSED_DIR = BASE_DIR + "/processed"

LOG_FILE_PATTERN = "tempData-*.log"
LOG_DELIM = ";"

DB_HOST = "localhost"
DB_NAME = "tempwatch"
DB_USER = "tempwatch"
DB_PWD = "tempwatch"

SQL_INSERT = "INSERT INTO templog(log_date, temp_value, sensor_id) VALUES (%s, %s, %s)"

def insertIntoDB(aDateValues, aSensorIds, aTempValues):
    try:
    
        con = mdb.connect(host=DB_HOST,user=DB_USER,passwd=DB_PWD,db=DB_NAME)
        cursor = con.cursor()
        
        for i in range(0,len(aTempValues)):
            cursor.execute(SQL_INSERT, (aDateValues[i], float(aTempValues[i]), aSensorIds[i]))
            con.commit()
            
        con.close()
        logger.info("Inserted {0} records in db".format(i + 1))
  
    except mdb.Error, e:
        logger.error(e)

aDateValues = []
aTempValues = []
aSensorIds = []

aLogFilesToProcess = fnmatch.filter(os.listdir(STAGE_DIR), LOG_FILE_PATTERN)

if len(aLogFilesToProcess) == 0:
    logger.info("No files to process, quitting")
    exit()

logger.info("Found {0} files to process".format(len(aLogFilesToProcess)))

for logFileName in aLogFilesToProcess:
    logger.info("Processing file {0}".format(logFileName))
    logFilePath = STAGE_DIR + "/" + logFileName
    with open(logFilePath) as logFile:
      logLines = logFile.readlines()
      logger.info("File contains {0} records".format(len(logLines)))
      for logLine in logLines:
          aLog = logLine.split(LOG_DELIM)
          aDateValues.append(aLog[0])
          aSensorIds.append(aLog[1])
          aTempValues.append(aLog[2])

      if (len(aTempValues) > 0):
          insertIntoDB(aDateValues, aSensorIds, aTempValues)
    
    logger.info("Moving file {0} to archive".format(logFileName))
    shutil.move(logFilePath, PROCESSED_DIR)
