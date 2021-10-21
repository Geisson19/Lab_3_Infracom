import os
import socket
from hashlib import sha256

host_ip = socket.gethostbyname(socket.gethostname())
port = 1233
inp = int(input("Cuántos clientes quiere conectar?:"))

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

def main():

    for i in range(0, inp): #inicia los N clientes
        connid = i + 1
        print('starting connection', connid, 'to', (host_ip, port))

        message = str(connid)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        tam_bloque = 4096

        tup = (host_ip, port)
        client.connect(tup)
        client.send(message.encode('ascii'))
        bienvenida = client.recv(tam_bloque)
        print(bienvenida.decode())

    for i in range(0, inp): #Pone a los N clientes a escuchar al server
        hash_servidor = client.recv(tam_bloque).decode()

        cConexiones = client.recv(tam_bloque).decode()
        print(f"Cantidad de conexiones: {cConexiones}")

        path = client.recv(tam_bloque).decode()
        fname = path.split("/")[1]

        archivo_recibido = client.recv(300 * 1024**2)
        path = 'archivosRecibidos/'
        if not os.path.isdir(path):
            os.mkdir(path)

        with open(path + fname, "wb") as f:
            f.write(archivo_recibido)

        hash_cliente = generarHash(path + fname)
        if hash_servidor == hash_cliente:
            print("Los hashes coinciden :)")
            print(hash_servidor)
            print(hash_cliente)
            client.send("Los hashes coinciden :)".encode())
        else:
            print(hash_servidor)
            print(hash_cliente)
            client.send("Los hashes no coinciden :(".encode())

if __name__ == "__main__":
    main()
