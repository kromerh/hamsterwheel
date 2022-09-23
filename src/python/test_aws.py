from datetime import datetime
import time
import logging

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

myMQTTClient = AWSIoTMQTTClient("rpi_hamsterwheel_sensor")
myMQTTClient.configureEndpoint("a72qba275aic3-ats.iot.eu-central-1.amazonaws.com", 8883)

myMQTTClient.configureCredentials(
    CAFilePath="/home/wilson/certificates/AmazonRootCA1.pem",
    KeyPath="/home/wilson/certificates/private-key.pem.key",
    CertificatePath="/home/wilson/certificates/device-certificate.pem.crt",
)

logger.info('Initiating Realtime Data Transfer From Raspberry Pi...')
Myvar= myMQTTClient.connect()
date = datetime.now().strftime("%Y-%m-%d %I:%M:%S")
logger.info(f"Starting logging. Timestamp: {date}.")


while True:
    date = datetime.now().strftime("%Y-%m-%d %I:%M:%S")
    message = "Test message"
    myMQTTClient.publish(
        "topic/pi",
        "{\"Timestamp\" :\""+ str(date) +
        "\", \"Mesage\":\""+ str(0) + "\"}", 0)
    logger.info(f'Published message {message}. Timestamp: {date}.')
    time.sleep(1)
