import socket
import os
from threading import Thread
import threading
from client import ClienteThread
from hashlib import sha256
import time 
from datetime import datetime
# struct, hashlib, time
# Informacion del servidor
port = 1233
host_ip = socket.gethostbyname(socket.gethostname())

threads = []

def main():
    print('[*] Iniciando servidor ...')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    arch = input('[/] Seleccione el tipo de archivo a enviar: (1 o 2)')
    print('Archivo tipo 1: 100 MB')
    print('Archivo tipo 2: 250 MB')
    path = 'archivosServidor/'
    if(arch == '1'):
        path += 'archivo1.txt'
        with open(path, "wb") as f:
            f.seek(100*1024**2)
            f.write("\0")
    else:
        path += 'archivo2.txt'
        with open(path, "wb") as f:
            f.seek(250*1024**2)
            f.write("\0") 

    # Numero de Threads para las conexiones concurrentes
    nThreads = int(input('Ingrese el número de threads: '))
    tup = (host_ip, port)
    server.bind(tup)
    server.listen()
    print('[*] El servidor está escuchando en el puerto {p}.'.format(p=port))

    while True:
        connection, (ip, port) = server.accept()
        thread = threading.Thread(target = operate, args = (connection, ip, port, path, nThreads))
        thread.start()
        threads.append([ip, port])
        
def operate(connection, ip, port, path, nThreads):
    print('Conexión establecida. {add} @ {p}'.format(add=ip, p = port))
    connection.send('Bienvenido, {}!'.format(ip))
    fhash = generarHash(path)
    fsize = os.path.getsize(path)
    connection.sendall('Hash: {}'.format(fhash))
    tiempo1 = time.time()
    with open(path, 'r') as f:
        file = f.read()
    connection.send(file)
    tiempo2 = time.time()
    tiempo = tiempo2 - tiempo1
    

def generarHash(path):
    hash = sha256()
    with open(path, 'rb') as f:
        while True:
            bloque = f.read(4096)
            if not bloque:
                break
            hash.update(bloque)
    f.close()
    return hash.hexdigest()


def generarLog(path, ip, port, tiempo):
    fechaActual = datetime.now()
    log = '{actualAnho}-{actualMes}-{actualDia}-{actualHora}-{actualMinuto}-{actualSegundo}-log.txt'.format(actualAnho = fechaActual.year,
                                                                                                            actualMes = fechaActual.month, 
                                                                                                            actualDia = fechaActual.day,
                                                                                                            actualHora = fechaActual.hour,
                                                                                                            actualMinuto = fechaActual.minute,
                                                                                                            actualSegundo = fechaActual.second )
    fileLog = open('logs/{}'.format(log), 'x')

    fileLog.write('Log {}\n'.format(fechaActual))
    fileLog.write('Nombre del archivo: {}\n'.format(path.split('/')[1]))
    fileLog.write('Tamaño del archivo: {}'.format(os.path.getsize(path)))
    fileLog.write('')
    fileLog.write('####################################################\n')
    fileLog.write('* ip: {add}\n* port: {p}\n* time: {t}\n'.format(add=ip, p=port, t = tiempo*1000))
    fileLog.write('')

    fileLog.close()



    

if __name__ == '__main__':
    main()
