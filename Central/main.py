from Central import Central
import sys

def main():
    c = Central('192.168.1.103', 10010)
    c.start()
    c.recvEstados()
    

    # while True:
    #     for e in list(c.sockets.keys()):
    #         print(e)

if __name__ == '__main__':
    main()
