import os
from datetime import datetime
import subprocess
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

import logging

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

# Get the user
username = os.getlogin()

# Script to get the wlan information
bash_get_wlan = f'/home/{username}/hamsterwheel/src/bash/get_wlan.sh'

# Get the wlan ip
subprocess.call(['sh', bash_get_wlan])

# Sleep for a few seconds to allow bash script to retrieve wlan information
time.sleep(3)

# Load the wlan information from file
ifconfig_file = f'/home/{username}/ifconfig.txt'
with open(ifconfig_file, 'r') as file:
    file_content = file.readlines()
    file.close()

# Clean the file info to extract only wlan0 content
nr_extract: int = 0
for i, line in enumerate(file_content):
    if 'wlan0' in line:
        nr_extract = i

file_content = [f.strip() for f in file_content[nr_extract:]]

# Send the file content to AWS

myMQTTClient = AWSIoTMQTTClient("rpi_hamsterwheel_sensor")
myMQTTClient.configureEndpoint("a72qba275aic3-ats.iot.eu-central-1.amazonaws.com", 8883)

myMQTTClient.configureCredentials(
    CAFilePath="/home/wilson/certificates/AmazonRootCA1.pem",
    KeyPath="/home/wilson/certificates/private-key.pem.key",
    CertificatePath="/home/wilson/certificates/device-certificate.pem.crt",
)

now = datetime.now().strftime("%Y-%m-%d %I:%M:%S")
message = ''.join(file_content)
topic = f'topic/{username}'
Myvar= myMQTTClient.connect()
myMQTTClient.publish(
    topic,
    "{\"Timestamp\" :\"" + str(now) +
    "\", \"ifconfig\":\"" + message + "\"}", 0)
print(f'Published message {message}. Timestamp: {now}. Topic: {topic}')

now = datetime.now().strftime("%Y-%m-%d %I:%M:%S")
message = ''.join(file_content)
topic = f'topic/wilson2'
Myvar= myMQTTClient.connect()
myMQTTClient.publish(
    topic,
    "{\"Timestamp\" :\"" + str(now) +
    "\", \"ifconfig\":\"" + message + "\"}", 0)
print(f'Published message {message}. Timestamp: {now}. Topic: {topic}')