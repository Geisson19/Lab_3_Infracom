import socket
import os
from threading import Thread
from client import ClienteThread

# Informacion del servidor
port = 1233
host_ip = socket.gethostbyname(socket.gethostname())

threads = []

def main():
    print('[*] Iniciando servidor ...')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print('Archivo tipo 1: 100 MB')
    print('Archivo tipo 2: 250 MB')
    arch = input('Seleccione el tipo de archivo a enviar: (1 o 2)')
    if(arch == '1'):
        with open("archivo1.txt", "w") as f:
            #f.seek(106970000)
            f.write("\0")
    else:
        with open("archivo2.txt", "w") as f:
            #f.seek(106970000*2.4)
            f.write("\0") 

    # Numero de Threads para las conexiones concurrentes
    nThreads = int(input('Ingrese el número de threads: '))
    tup = (host_ip, port)
    server.bind(tup)
    server.listen()
    print('[*] El servidor está escuchando en el puerto {p}.'.format(p=port))

    while True:
        server.listen(nThreads) # De los requerimientos
        print ("\nListening for incoming connections...")
        clientsock = server.accept()[0]
        newthread = ClienteThread(host_ip, port, clientsock=clientsock)
        newthread.start()
        threads.append(newthread)

    for t in threads:
        t.join()

if __name__ == '__main__':
    main()
