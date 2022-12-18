from Central import Central, Interface
import sys

def main():
    ip, port = sys.argv[1], sys.argv[2]
    c = Central(ip, int(port))
    c.start()
    c.recvEstados()
    i = Interface(c)
    while True:
        if c.sockets:
            i.menuInicial(True)
            

if __name__ == '__main__':
    main()
