#!/usr/bin/python
import os
import logging
import shutil
import datetime

BASE_DIR = "/home/pi/tempwatch"

logging.basicConfig(filename= BASE_DIR + "/logs/rotator_error.log",
  level=logging.DEBUG,
  format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger=logging.getLogger(__name__)

logUploadDir = BASE_DIR + "/upload"

tempLogFile = BASE_DIR + "/tempData.log"

logTime = datetime.datetime.now() - datetime.timedelta(days=1)

tempLogUploadFile = logUploadDir + "/" + logTime.strftime("tempData-%Y%m%dT%H%M%S.log")

print tempLogUploadFile

# Check that file exist
if not os.path.isfile(tempLogFile):
    logger.error("Could not find file: {0}".format(tempLogFile))
    exit()

# Move and rename data file
shutil.move(tempLogFile, tempLogUploadFile)