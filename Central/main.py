from Central import Central
import sys

def main():
    c = Central('127.0.0.1', 10100)
    c.start()
    while True:
        for e in list(c.sockets.keys()):
            print(e)

if __name__ == '__main__':
    main()