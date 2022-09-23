from datetime import datetime
import time
import logging

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


from constants import (
    AWS_CLIENT_NAME,
    AWS_ENDPOINT,
    AWS_CA_FILE,
    AWS_KEY,
    AWS_CERT,
    AWS_TOPIC,
)

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

mqtt_client = AWSIoTMQTTClient(AWS_CLIENT_NAME)
mqtt_client.configureEndpoint(AWS_ENDPOINT, 8883)

mqtt_client.configureCredentials(
    CAFilePath=AWS_CA_FILE,
    KeyPath=AWS_KEY,
    CertificatePath=AWS_CERT
)

logger.info('Initiating Realtime Data Transfer From Raspberry Pi...')
mqtt_connect = mqtt_client.connect()
date = datetime.now().strftime("%Y-%m-%d %I:%M:%S")
logger.info(f"Starting logging. Timestamp: {date}.")


while True:
    date = datetime.now().strftime("%Y-%m-%d %I:%M:%S")
    message = "Test message"
    mqtt_client.publish(
        AWS_TOPIC,
        "{\"Timestamp\" :\""+ str(date) +
        "\", \"Message\":\""+ message + "\"}", 0)
    logger.info(f'Published message {message}. Timestamp: {date}.')
    time.sleep(1)
