import sys
import time
import logging
import RPi.GPIO as GPIO

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

# Set the LED pin number
LED_PIN = 26

# Set the GPIO modes
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# Bring LED to blink for 30 seconds
try:
    cnt = 0
    while cnt < 30:
        GPIO.output(LED_PIN, GPIO.HIGH)
        logger.info("## Turned LED ON")
        time.sleep(1)
        GPIO.output(LED_PIN, GPIO.LOW)
        logger.info("## Turned LED OFF")
        time.sleep(1)
        cnt += 1
    GPIO.cleanup()

except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()
