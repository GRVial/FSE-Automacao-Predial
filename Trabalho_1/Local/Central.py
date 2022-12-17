import socket
import threading
import json
import os
from time import sleep

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
            while True:
                for nome in self.sockets.copy():
                    self.estados[nome] = json.loads(self.sockets[nome].recv(4096).decode('utf-8'))
        t = threading.Thread(target=recvEstado)
        t.start()

    def run(self):
        while True:
            conn, addr = self.sock.accept()
            nome = conn.recv(1024).decode('utf-8')
            self.sockets[nome] = conn
            # print(f'{nome} conectado')


class Interface:
    c : Central
    def __init__(self, central:Central) -> None:
        self.c = central

    def menuInicial(self) -> None:
        os.system('clear')
        sockets = self.c.sockets.copy()
        print('Salas conectadas:')
        for sala in sockets:
            print(sala)
        print('---------------------------------------------------\n\n\n')
        print(f'[0] Sistema de alarme: {self.c.sistemaAlarme}')
        print('Digite o nome da sala para escolher uma sala')
        option = input()
        if option == '0':
            self.c.sistemaAlarme = False if self.c.sistemaAlarme else True
            for sala in sockets:
                if self.c.sistemaAlarme:
                    self.c.sendData('liga sistema alarme', sala)
                else:
                    self.c.sendData('desliga sistema alarme', sala)
        else:
            self.menuSala(option)

    def menuSala(self, sala:str) -> None:
        estados = self.c.estados.copy()
        os.system('clear')
        print(f'========={sala}=========')
        for key, value in estados[sala].items():
            print(f'{key}: {value}')
        print('=========================\n\n\n')
        print('[0] Voltar\n[1] Atualizar\nComando: ', end='')
        option = input()
        if option == '0':
            return
        if option == '1':
            self.menuSala(sala)
        else:
            self.c.sendData(option, name=sala)
            self.menuSala(sala)
            