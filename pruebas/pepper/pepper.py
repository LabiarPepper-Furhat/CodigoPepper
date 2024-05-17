# -*- coding: utf-8 -*-

import socket

def main():
    host = '127.0.0.1'
    port = 12345
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    try:
        while True:
            message = raw_input("Mensaje para enviar al servidor: ").encode('utf-8')  # Codificar la cadena de texto a bytes
            client_socket.sendall(message)
            data = client_socket.recv(1024)
            print('Respuesta del servidor:', data.decode('utf-8'))  # Decodificar los bytes a cadena de texto
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
