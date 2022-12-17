import socket
import threading
import json
import os
from time import sleep
from datetime import datetime

class Central(threading.Thread):
    addr : tuple
    sockets : dict
    estados : dict
    sistemaAlarme : bool

    def __init__(self, ip:str, port:int):
        super().__init__()
        self.addr = ip, port
        self.sockets = {}
        self.sock = socket.create_server(self.addr)
        self.estados = {}
        self.sistemaAlarme = False

    def sendData(self, data:str, name:str):
        self.sockets[name].send(data.encode('utf-8'))

    def recvEstados(self) -> None:
        def recvEstado():
            al = False
            while True:
                for nome in self.sockets.copy():
                    self.estados[nome] = json.loads(self.sockets[nome].recv(4096).decode('utf-8'))
                    if self.estados[nome]['AL_BZ'] and not al:
                        self.escreveLog(f'{nome}: Alarme Ligado')
                        al = True
                    if not self.estados[nome]['AL_BZ'] and al:
                        self.escreveLog(f'{nome}: Alarme Desligado')
                        al = False
        t = threading.Thread(target=recvEstado)
        t.start()

    def run(self):
        while True:
            conn, addr = self.sock.accept()
            nome = conn.recv(1024).decode('utf-8')
            self.sockets[nome] = conn
            # print(f'{nome} conectado')

    def escreveLog(self, output:str):
        with open('Log.csv', 'a') as log:
            log.write(f'{output},{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n')

    def ligarLuzes(self):
        for sock in self.sockets:
            self.sendData('liga L_01 L_02' ,sock)
        self.escreveLog('liga todas luzes')

    def desligarLuzes(self):
        for sock in self.sockets:
            self.sendData('desliga L_01 L_02' ,sock)
        self.escreveLog('desliga todas luzes')

    def switchSistemaAlarme(self) -> bool:
        if not self.sistemaAlarme:
            block = False
            estados = self.estados
            os.system('clear')
            for sala in estados:
                for key in ['SJan', 'SPor']:
                    if estados[sala][key]:
                        block = True
                        print(f'{sala} {key} ligado! Feche a porta/janela para acionar o sistema de alarme.')
            if block:
                return False
        
        sockets = self.sockets
        self.sistemaAlarme = False if self.sistemaAlarme else True
        for sala in sockets:
            if self.sistemaAlarme:
                self.sendData('liga sistema alarme', sala)
            else:
                self.sendData('desliga sistema alarme', sala)
        return True

class Interface:
    c : Central
    def __init__(self, central:Central) -> None:
        self.c = central

    def menuInicial(self, clear:bool) -> None:
        if clear:
            os.system('clear')
        sockets = self.c.sockets.copy()
        print('Salas conectadas:')
        for sala in sockets:
            print(sala)
        print('---------------------------------------------------\n\n\n')
        print(f'[0] Sistema de alarme: {self.c.sistemaAlarme}')
        print(f'[1] Ligar todas luzes')
        print(f'[2] Desligar todas luzes')
        print('Digite o nome da sala para escolher uma sala')
        option = input()
        if option == '0':
            if not self.c.switchSistemaAlarme():
                self.menuInicial(False)
            # self.c.sistemaAlarme = False if self.c.sistemaAlarme else True
            # for sala in sockets:
            #     if self.c.sistemaAlarme:
            #         self.c.sendData('liga sistema alarme', sala)
            #     else:
            #         self.c.sendData('desliga sistema alarme', sala)
        elif option == '1':
            self.c.ligarLuzes()
        elif option == '2':
            self.c.desligarLuzes()
        else:
            self.menuSala(option)

    def menuSala(self, sala:str) -> None:
        estados = self.c.estados.copy()
        os.system('clear')
        print(f'========={sala}=========')
        for key, value in estados[sala].items():
            print(f'{key}: {value}')
        print('=========================\n\n\n')
        print('[0] Voltar\n[1] Atualizar')
        print('Comandos:\nliga <outputs>\ndesliga <outputs>\nComando: ', end='')
        option = input()
        if option == '0':
            return
        if option == '1':
            self.menuSala(sala)
        else:
            self.c.sendData(option, name=sala)
            self.c.escreveLog(f'{sala}: {option}')
            self.menuSala(sala)
            