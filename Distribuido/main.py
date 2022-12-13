from Sala import Sala
from Sala import SalaThread
import sys

def main():
    jsonFile = sys.argv[1]
    thread = SalaThread(Sala(jsonFile))
    thread.start()

if __name__ == '__main__':
    main()
