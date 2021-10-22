import os
import socket

#host_ip = "127.0.0.1"
host_ip = "192.168.81.128" #TODO
port = 8081 #TODO

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tam_bloque = 4096

    mensaje = "Estado: Listo"
    client.sendto(mensaje.encode(), (host_ip, port))

    bienvenida, addr = client.recvfrom(tam_bloque)
    print(bienvenida.decode("utf-8")) 

    numCliente, addr = client.recvfrom(tam_bloque)
    dec_num_cliente = numCliente.decode("utf-8")
    print(f"Numero de cliente: {dec_num_cliente}")

    cConexiones, addr = client.recvfrom(tam_bloque)
    dec_can_conexiones = cConexiones.decode("utf-8")
    print(f"Cantidad de conexiones: {dec_can_conexiones}")

    # ** Recibiendo el archivo
    buf_archivo = 64000

    path = 'archivosRecibidos/'
    if not os.path.isdir(path):
        os.mkdir(path)

    fname = f"{dec_num_cliente}-Prueba-{dec_can_conexiones}.txt"
    file = open(path + fname,'wb')
    data, addr = client.recvfrom(buf_archivo)
    try:
        while(data):
            file.write(data)
            client.settimeout(1)
            data, addr = client.recvfrom(buf_archivo)
    except socket.timeout:
        file.close()
        client.close()
        print("Archivo descargado")

    client.close()

if __name__ == "__main__":
    main()
