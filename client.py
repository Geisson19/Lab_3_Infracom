import os
import socket
from hashlib import sha256

host_ip = socket.gethostbyname(socket.gethostname())
port = 1233


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
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    tam_bloque = 4096

    tup = (host_ip, port)
    client.connect(tup)

    bienvenida = client.recv(tam_bloque)
    print(bienvenida.decode())

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
        print("Los hashes NO coinciden :(")
        print(hash_servidor)
        print(hash_cliente)
        client.send("Los hashes no coinciden :(".encode())

if __name__ == "__main__":
    main()
