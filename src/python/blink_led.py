import sys
import time
import RPi.GPIO as GPIO

# Set the LED pin number
LED_PIN = 4

# Set the GPIO modes
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# Bring LED to blink for 30 seconds
try:
    cnt = 0
    while cnt < 30:
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(1)
        cnt += 1
    GPIO.cleanup()

except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()
