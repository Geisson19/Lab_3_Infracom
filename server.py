import socket
import os
from threading import Thread
from hashlib import sha256
import time 
from datetime import datetime

threads = []

def main():
    # Variables de entorno
    host_ip = socket.gethostbyname(socket.gethostname())
    port = 1233

    print("[*] Iniciando servidor ...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("Archivo tipo 1: 100 MB")
    print("Archivo tipo 2: 250 MB")
    arch = input("[/] Seleccione el tipo de archivo a enviar: (1 o 2)\n")
    
    path = "archivosServidor/"
    if not os.path.isdir(path):
        os.mkdir(path)

    if(arch == "1"):
        path += "archivo1.txt"
        with open(path, "wb") as f:
            f.seek(100*1024**2)
            f.write("Infracom".encode())
    else:
        path += "archivo2.txt"
        with open(path, "wb") as f:
            f.seek(250*1024**2)
            f.write("Infracom".encode()) 

    # Numero de Threads para las conexiones concurrentes
    nThreads = int(input("Ingrese el número de threads: "))
    tup = (host_ip, port)
    server.bind(tup)
    server.listen()
    print("[*] El servidor está escuchando en el puerto {p}.".format(p=port))

    while True:
        connection, (ip, port) = server.accept()
        thread = Thread(target = operate, args = (connection, ip, port, path, nThreads))
        thread.start()
        threads.append([ip, port])
        
def operate(connection, ip, port, path, nThreads):
    print(f"Conexion establecida. {ip} @ {port}".encode())
    connection.send(f"Bienvenido, {ip}@ {port}!".encode())
    fhash = generarHash(path)
    fsize = os.path.getsize(path)
    connection.send(f"{fhash}".encode())
    connection.send(f"{nThreads}".encode())
    connection.send(f"Archivo: {path}".encode())

    tiempo1 = time.time()
    with open(path, "r") as f:
        file = f.read()
    connection.send(file.encode())

    tiempo2 = time.time()
    tiempo = tiempo2 - tiempo1
    generarLog(path, ip, port, fsize, tiempo)

def generarHash(path):
    hash = sha256()
    with open(path, "rb") as f:
        while True:
            bloque = f.read(4096)
            if not bloque:
                break
            hash.update(bloque)
    f.close()
    return hash.hexdigest()


def generarLog(path, ip, port, fsize, tiempo):

    if not os.path.isdir("./logs"):
        os.mkdir("./logs")

    fActual = datetime.now()
    log = f"{fActual.year}-{fActual.month}-{fActual.day}-{fActual.hour}-{fActual.minute}-{fActual.second}-log.txt"
    
    fileLog = open(f"logs/{log}", "x")

    fileLog.write("Log {}\n".format(fActual))
    fileLog.write("Nombre del archivo: {}\n".format(path.split("/")[1]))
    fileLog.write("Tamaño del archivo: {}".format(fsize))
    fileLog.write("\n")
    fileLog.write("####################################################\n")
    fileLog.write("* ip: {add}\n* port: {p}\n* time: {t}\n".format(add=ip, p=port, t = tiempo*1000))
    fileLog.write("")

    fileLog.close()

if __name__ == "__main__":
    main()
