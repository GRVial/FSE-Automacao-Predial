import RPi.GPIO as GPIO
import json
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def setup(dict):
    for e in dict['IN'].values():
        GPIO.setup(e, GPIO.IN)
    for e in dict['OUT'].values():
        GPIO.setup(e, GPIO.OUT)

def ligaX(value):
    GPIO.output(value, GPIO.HIGH)

def desligaX(value):
    GPIO.output(value, GPIO.LOW)

def loadConfig() -> dict:
    with open('conf2.json', 'r') as json_file:
        conf = json.load(json_file)
    return conf

def main():
    conf = loadConfig()
    setup(conf)

    while True:
        ligaX(conf['OUT']['L_01'])
        ligaX(conf['OUT']['L_02'])
        sleep(2)
        desligaX(conf['OUT']['L_01'])
        desligaX(conf['OUT']['L_02'])
        sleep(1)

if __name__ == '__main__':
    main()