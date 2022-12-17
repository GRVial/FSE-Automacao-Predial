from Central import Central, Interface
import sys

def main():
    c = Central('192.168.1.132', 10010)
    c.start()
    c.recvEstados()
    i = Interface(c)
    while True:
        if c.sockets:
            i.menuInicial(True)
            

if __name__ == '__main__':
    main()
