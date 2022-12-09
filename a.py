import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

lampadas = [26, 19]
ar = 13
projetor = 6


GPIO.setup(lampadas, GPIO.OUT)
GPIO.setup(ar, GPIO.OUT)
GPIO.setup(projetor, GPIO.OUT)

def ligaLampada() -> bool:
    GPIO.output(lampadas, GPIO.HIGH)
    return True

def ligaProgetor() -> bool:
    GPIO.output(projetor, GPIO.HIGH)
    return True

def ligaAr() -> bool:
    GPIO.output(ar, GPIO.HIGH)
    return True

def desligaLampada() -> bool:
    GPIO.output(lampadas, GPIO.LOW)
    return False

def desligaProgetor() -> bool:
    GPIO.output(projetor, GPIO.LOW)
    return False

def desligaAr() -> bool:
    GPIO.output(ar, GPIO.LOW)
    return False

if __name__ == '__main__':
    lampadasState = desligaLampada()
    arState = desligaAr()
    projetorState = desligaProgetor()

    while(True):
        lampadasState = ligaLampada()
        arState = ligaAr()
        projetorState = ligaProgetor()
        print("Ligou!")
        sleep(3)

        lampadasState = desligaLampada()
        projetorState = desligaProgetor()
        arState = desligaAr()
        print("Desligou!")

        sleep(3)
