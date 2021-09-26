import socket
from threading import Thread
import threading

# Informacion del servidor
ServerSocket = socket.socket()
# host_ip = socket.gethostbyname(socket.gethostname)
port = 1233


class ClienteThread(Thread):

    def __init__(self, ip, port, clientsock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsock = clientsock
        print('Nuevo thread @{p} para {add}'.format(p=self.port, add = self.ip))
    
    def run(self):
        print ("Connection from {add}: {p}".format(add = self.ip, p = self.port))

        self.clientsock.send("\nWelcome to the server\n\n")

        data = "dummydata"

        while len(data):
            data = self.clientsock.recv(2048)
            print("Cliente envió : "+data)
            self.clientsock.send("Usted me envió : "+data)

        print( "Cliente desconectado...")

