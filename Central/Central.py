import socket
import threading
import json

class Central(threading.Thread):
    addr : tuple
    sockets : dict
    estados : dict

    def __init__(self, ip:str, port:int):
        super().__init__()
        self.addr = ip, port
        self.sockets = {}
        self.sock = socket.create_server(self.addr)
        self.estados = {}

    def send(self, data:str):
        socket[0].send('Teste do bacana\n')

    def recvEstados(self, nome:str) -> None:
        self.estados[nome] = json.loads(self.sockets[nome].recv(4096))



    def run(self):
        while True:
            conn, addr = self.sock.accept()
            nome = conn.recv(1024).decode('utf-8')
            self.sockets[nome] = conn
