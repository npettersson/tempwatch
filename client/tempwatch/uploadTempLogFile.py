#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import time
import logging
import pysftp
import shutil

BASE_DIR = "/home/pi/tempwatch"

logging.basicConfig(filename= BASE_DIR + "/logs/upload.log",
  level=logging.INFO,
  format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger=logging.getLogger(__name__)

LOCAL_SOURCE_DIR = BASE_DIR + "/upload"
LOCAL_ARCHIVE_DIR = BASE_DIR + "/archive"

REMOTE_SFTP_HOST = "home.npet.se"
REMOTE_SFTP_PORT = 2224
REMOTE_SFTP_USER = "pi"
REMOTE_SFTP_KEYFILE = "/home/pi/.ssh/home_raspi2"
REMOTE_DEST_DIR = "/home/pi/tempwatch/stage"

filesToUpload = os.listdir(LOCAL_SOURCE_DIR)
nbrOfFilesToUpload = len(filesToUpload)

logger.info("Found {0} files to upload".format(nbrOfFilesToUpload))

if nbrOfFilesToUpload == 0:
    logger.info("No files to upload, quitting")
    exit()

logger.info("Starting upload to {0}".format(REMOTE_SFTP_HOST))

with pysftp.Connection(REMOTE_SFTP_HOST, port=REMOTE_SFTP_PORT, 
    username=REMOTE_SFTP_USER, private_key=REMOTE_SFTP_KEYFILE) as sftp:
    logger.info("Connected to host")
    sftp.chdir(REMOTE_DEST_DIR)
    for logFile in filesToUpload:
        try:
            logFilePath = LOCAL_SOURCE_DIR + "/" + logFile
            logger.info("Uploading {0}".format(logFile))
            sftp.put(logFilePath, preserve_mtime=True)
            logger.info("Moving {0} to archive".format(logFile))
            shutil.move(logFilePath, LOCAL_ARCHIVE_DIR)
        except Exception, e:
            logger.error("Error occured when uploading: "  + e.message)
        
    logger.info("Upload done!")