import RPi.GPIO as io
from datetime import datetime
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

myMQTTClient = AWSIoTMQTTClient("rpi_hamsterwheel_sensor")
myMQTTClient.configureEndpoint("a72qba275aic3-ats.iot.eu-central-1.amazonaws.com", 8883)

myMQTTClient.configureCredentials(
    CAFilePath="/home/wilson/certificates/AmazonRootCA1.pem",
    KeyPath="/home/wilson/certificates/private-key.pem.key",
    CertificatePath="/home/wilson/certificates/device-certificate.pem.crt",
)
 
# Set Broadcom mode so we can address GPIO pins by number.
io.setmode(io.BCM)
wheelpin = 18
logger.info(f'Setting io pin to {wheelpin}.')
io.setup(wheelpin, io.IN, pull_up_down=io.PUD_UP) 

logger.info('Initiating Realtime Data Transfer From Raspberry Pi...')
Myvar= myMQTTClient.connect()
date = datetime.now().strftime("%Y-%m-%d %I:%M:%S")
logger.info(f"Starting logging. Timestamp: {date}.")


while True:
    date = datetime.now().strftime("%Y-%m-%d %I:%M:%S")
    if (io.input(wheelpin) == 0):
        message = "Magnet closed."
        myMQTTClient.publish(
            "topic/pi",
            "{\"Timestamp\" :\""+ str(date) +
            "\", \"Magnet\":\""+ str(0) + "\"}", 0)
        logger.info(f'Published message {message}. Timestamp: {date}.')
    else:
        message = "Magnet open."
        myMQTTClient.publish(
            "topic/pi",
            "{\"Timestamp\" :\""+ str(date) +
            "\", \"Magnet\":\""+ str(1) + "\"}", 0)
        logger.info(f'Published message {message}. Timestamp: {date}.')
    time.sleep(1)
