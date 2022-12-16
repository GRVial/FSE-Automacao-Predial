from Sala import Sala, Conexao
import sys
from time import time

def main():
    jsonFile = sys.argv[1]
    sala = Sala(jsonFile)
    conn = Conexao(sala)
    conn.conectaCentral()
    conn.start()
    sala.sistemaAlarme = True
    sala.start()
    # loop principal
    hora = time()
    while True:
        if time() == hora+2:
            conn.sendState()
            hora = time()


if __name__ == '__main__':
    main()
