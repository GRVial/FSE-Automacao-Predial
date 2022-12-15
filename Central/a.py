import socket

s = socket.create_connection(('127.0.0.1', 10100))
s.send('Meu nome é marreco'.encode('utf-8'))