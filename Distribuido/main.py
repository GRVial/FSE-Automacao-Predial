from Sala import Sala
from Sala import SalaThread
import sys

def main():
    jsonFile = sys.argv[1]
    sala = Sala(jsonFile)
    thread = SalaThread(sala)
    sala.sistemaAlarme = False
    thread.start()

if __name__ == '__main__':
    main()
