from RPi import GPIO
from time import sleep
PWM_PIN = 19
DIR_PIN = 16

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(PWM_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)
pwmPin = GPIO.PWM(PWM_PIN, 1000)
pwmPin.ChangeDutyCycle(100)
pwmPin.start(0)


direction = GPIO.LOW

while True:
    GPIO.output(DIR_PIN, direction)
    print("Running at speed ", 100)
    pwmPin.ChangeDutyCycle(100)
    sleep(5)
    print("Running at speed ", 50)
    pwmPin.ChangeDutyCycle(50)
    sleep(5)
    print("Running at speed ", 0)
    pwmPin.ChangeDutyCycle(0)
    sleep(2)
