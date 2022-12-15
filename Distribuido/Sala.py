import json
import RPi.GPIO as GPIO
import board
import adafruit_dht
import threading
from time import time, sleep

class Sala:
    input : dict
    output : dict
    estado : dict
    pessoas : int
    temperatura : float
    umidade : float
    tempo : float
    sistemaAlarme : bool
    nome : str

    def __init__(self, jsonFile:str) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        with open(jsonFile) as f:
            cfg = json.load(f)

        out = cfg['outputs']
        self.output = {}
        for o in out:
            if o['tag'] == 'Lâmpada 01':
                self.output['L_01'] = o['gpio']
            elif o['tag'] == 'Lâmpada 02':
                self.output['L_02'] = o['gpio']
            elif o['tag'] == 'Projetor Multimidia':
                self.output['PR'] = o['gpio']
            elif o['tag'] == 'Ar-Condicionado (1º Andar)':
                self.output['AC'] = o['gpio']
            elif o['tag'] == 'Sirene do Alarme':
                self.output['AL_BZ'] = o['gpio']

        inp = cfg['inputs']
        self.input = {}
        for i in inp:
            if i['tag'] == 'Sensor de Presença':
                self.input['SPres'] = i['gpio']
            elif i['tag'] == 'Sensor de Fumaça':
                self.input['SFum'] = i['gpio']
            elif i['tag'] == 'Sensor de Janela':
                self.input['SJan'] = i['gpio']
            elif i['tag'] == 'Sensor de Porta':
                self.input['SPor'] = i['gpio']
            elif i['tag'] == 'Sensor de Contagem de Pessoas Entrada':
                self.input['SC_IN'] = i['gpio']
            elif i['tag'] == 'Sensor de Contagem de Pessoas Saída':
                self.input['SC_OUT'] = i['gpio']

        self.estado = {k: False for k in self.output}
        dht22 = cfg['sensor_temperatura'][0]['gpio']
        self.nome = cfg['nome']

        for e in self.output.values():
            GPIO.setup(e, GPIO.OUT)
        for e in self.input.values():
            GPIO.setup(e, GPIO.IN)

        GPIO.add_event_detect(self.input['SC_IN'], GPIO.RISING)
        GPIO.add_event_detect(self.input['SC_OUT'], GPIO.RISING)
        self.pessoas = 0
        self.temperatura = 0.0
        self.umidade =  0.0
        self.tempo = 0.0
        self.sistemaAlarme = False
        self.dhtDevice = adafruit_dht.DHT22(board.D18) if self.dht22 == 18 else adafruit_dht.DHT22(board.D4)

    def ligaX(self, gpio:str) -> None:
        GPIO.output(gpio, GPIO.HIGH)
        self.estado[gpio] = True

    def desligaX(self, gpio:str) -> None:
        GPIO.output(gpio, GPIO.LOW)
        self.estado[gpio] = False

    def desligaAll(self) -> None:
        for e in self.output:
            self.desligaX(e)

    def ligaAll(self) -> None:
        for e in self.output:
            self.ligaX(e)

    def getDHT22(self) -> None:
        try:
            self.temperatura, self.umidade = self.dhtDevice.temperature, self.dhtDevice.humidity
            print(f'Temperatura: {self.temperatura:0.1f}\tUmidade: {self.umidade:0.1f}')
        except:
            print('Erro DHT22')
    
    def contaPessoa(self) -> None:
        if GPIO.event_detected(self.input['SC_IN']):
            self.pessoas += 1
        if GPIO.event_detected(self.input['SC_OUT'] and self.pessoas > 0):
            self.pessoas -= 1    
        print(f'Pessoas: {self.pessoas}')

    def presencaLuz(self) -> None:
        if not self.sistemaAlarme and GPIO.input(self.input['SPres']):
            self.ligaX(self.output['L_01'])
            self.ligaX(self.output['L_02'])
            self.tempo = time()
        elif time() >= self.tempo + 15:
            self.desligaX(self.output['L_01'])
            self.desligaX(self.output['L_02'])

    def fumacaAlarme(self) -> None:
        GPIO.output(self.output['AL_BZ'], GPIO.HIGH if GPIO.input(self.input['SFum']) else GPIO.LOW)

    def checaAlarme(self) -> None:
        if GPIO.input(self.input['SPres']) or GPIO.input(self.input['SJan']) or GPIO.input(self.input['SPor']) or GPIO.input(self.input['SFum']):
            GPIO.output(self.output['AL_BZ'], GPIO.HIGH)
        else:
            GPIO.output(self.output['AL_BZ'], GPIO.LOW)



class SalaThread(threading.Thread):
    def __init__(self, sala:Sala) -> None:
        super().__init__()
        self.sala = sala

    def run(self):
        while True:
            self.sala.getDHT22()
            self.sala.contaPessoa()
            self.sala.presencaLuz()
            # alarme ligado
            if self.sala.sistemaAlarme:
                self.sala.checaAlarme()
            # alarme desligado
            else:
                self.sala.fumacaAlarme()
            sleep(0.1)