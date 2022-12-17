import json
import RPi.GPIO as GPIO
import board
import adafruit_dht
import threading
from time import time, sleep
import socket

class Sala(threading.Thread):
    input : dict
    output : dict
    estado : dict
    pessoas : int
    temperatura : float
    umidade : float
    tempo : float
    sistemaAlarme : bool
    nome : str
    addrCentral : tuple

    def __init__(self, jsonFile:str) -> None:
        super().__init__()
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
        self.addrCentral = cfg['ip_servidor_central'], cfg['porta_servidor_central']
        self.sistemaAlarme = False
        dht22 = cfg['sensor_temperatura'][0]['gpio']
        if dht22 == 18:
            try:
                self.dhtDevice = adafruit_dht.DHT22(board.D18)
            except:
                self.dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)
        elif dht22 == 4:
            try:
                self.dhtDevice = adafruit_dht.DHT22(board.D4)
            except:
                self.dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

    def ligaX(self, tag:str) -> None:
        try:
            GPIO.output(self.output[tag], GPIO.HIGH)
            self.estado[tag] = True
        except KeyError:
            pass

    def desligaX(self, tag:str) -> None:
        try:
            GPIO.output(self.output[tag], GPIO.LOW)
            self.estado[tag] = False
        except KeyError:
            pass

    def desligaAll(self) -> None:
        for e in self.output:
            self.desligaX(e)

    def ligaAll(self) -> None:
        for e in self.output:
            self.ligaX(e)

    def getDHT22(self) -> tuple:
        try:
            self.temperatura, self.umidade = self.dhtDevice.temperature, self.dhtDevice.humidity
            # print(f'Temperatura: {self.temperatura:0.1f}\tUmidade: {self.umidade:0.1f}')
        except:
            print('Erro DHT22')
        return self.temperatura, self.umidade
    
    def contaPessoa(self) -> None:
        if GPIO.event_detected(self.input['SC_IN']):
            self.pessoas += 1
            # print(f'Pessoas: {self.pessoas}')
        if GPIO.event_detected(self.input['SC_OUT'] and self.pessoas > 0):
            self.pessoas -= 1    
            # print(f'Pessoas: {self.pessoas}')

    def presencaLuz(self) -> None:
        if GPIO.input(self.input['SPres']):
            self.ligaX('L_01')
            self.ligaX('L_02')
            self.tempo = time()
        elif self.tempo is not None and time() >= self.tempo + 15:
            self.desligaX('L_01')
            self.desligaX('L_02')
            self.tempo = None

    def fumacaAlarme(self) -> None:
        if GPIO.input(self.input['SFum']):
            self.ligaX('AL_BZ')
        else:
            self.desligaX('AL_BZ')

    def checaAlarme(self) -> None:
        if GPIO.input(self.input['SPres']) or GPIO.input(self.input['SJan']) or GPIO.input(self.input['SPor']) or GPIO.input(self.input['SFum']):
            self.ligaX('AL_BZ')
        else:
            self.desligaX('AL_BZ')

    def run(self):
        while True:
            # self.getDHT22()
            # alarme ligado
            if self.sistemaAlarme:
                self.checaAlarme()
            # alarme desligado
            else:
                self.contaPessoa()
                self.presencaLuz()
                self.fumacaAlarme()
            sleep(0.1)


class Conexao(threading.Thread):
    sock : socket.socket
    def __init__(self, sala:Sala) -> None:
        super().__init__()
        self.sala = sala

    def conectaCentral(self):
        nome = self.sala.nome
        self.sock = socket.create_connection(self.sala.addrCentral)
        self.sock.send(nome.encode('utf-8'))

    def sendState(self):
        estados = self.sala.estado.copy()
        for key, value in self.sala.input.items():
            estados[key] = True if GPIO.input(value) else False
        estados['temperatura'], estados['umidade'] = self.sala.getDHT22()
        estados['pessoas'] = self.sala.pessoas
        self.sock.send(json.dumps(estados).encode('utf-8'))
        print('Estado enviado!')

    def run(self):
        while True:
            msg = self.sock.recv(1024).decode('utf-8')
            if msg.upper() == 'LIGA ALL':
                self.sala.ligaAll()
            elif msg.upper() == 'DESLIGA ALL':
                self.sala.desligaAll()
            elif msg.upper() == 'LIGA SISTEMA ALARME':
                self.sala.sistemaAlarme = True
            elif msg.upper() == 'DESLIGA SISTEMA ALARME':
                self.sala.sistemaAlarme = False
            else:
                msg = msg.split()
                if msg[0].upper() == 'LIGA':
                    for e in msg[1:]:
                        self.sala.ligaX(e)
                elif msg[0].upper() == 'DESLIGA':
                    for e in msg[1:]:
                        self.sala.desligaX(e)
