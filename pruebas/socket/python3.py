# -*- coding: utf-8 -*-
# Servidor en Python 3.12.3
import socket

def main():
    host = '127.0.0.1'
    port = 12345
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print("Esperando conexión...")
        conn, addr = server_socket.accept()
        with conn:
            print('Conexión establecida desde:', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                try:
                    print('Recibido:', data.decode('utf-8', errors='ignore'))
                except UnicodeDecodeError:
                    print('Error al decodificar los datos')
                conn.sendall(b'Recibido')

if __name__ == "__main__":
    main()
