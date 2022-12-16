import socket
import threading
import json

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

    def send(self, data:str):
        socket[0].send('Teste do bacana\n')

    def recvEstados(self) -> None:
        def recvEstado():
            while True:
                for nome in self.sockets.copy():
                    print('dentro')
                    self.estados[nome] = json.loads(self.sockets[nome].recv(4096).decode('utf-8'))
                    print(f'{nome}:\n{self.estados[nome]}')
        t = threading.Thread(target=recvEstado)
        t.start()

    def run(self):
        while True:
            conn, addr = self.sock.accept()
            nome = conn.recv(1024).decode('utf-8')
            self.sockets[nome] = conn
            print(f'{nome} conectado')
