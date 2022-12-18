from Sala import Sala, Conexao
import sys
from time import time, sleep

def main():
    jsonFile = sys.argv[1]
    sala = Sala(jsonFile)
    conn = Conexao(sala)
    while conn.sock is None:
        try:
            conn.conectaCentral()
        except ConnectionRefusedError:
            pass
    conn.start()
    sala.start()
    # loop principal
    hora = time()
    while True:
        if time() >= hora+2:
            conn.sendState()
            sleep(0.2)
            hora = time()


if __name__ == '__main__':
    main()
