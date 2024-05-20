# -*- coding: utf-8 -*-
# Cliente en Python 2.7

# Código para enviar mensajes al servidor en Python 3.12.3

import socket
import re
import sys
import codecs

# Asegurarse de que la salida usa UTF-8
if sys.version_info < (3,):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    

def reemplazar_acentos(texto):
    # Reemplazar letras con acento por las equivalentes sin acento
    texto_sin_acentos = texto.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
    texto_sin_acentos = texto_sin_acentos.replace('Á', 'A').replace('É', 'E').replace('Í', 'I').replace('Ó', 'O').replace('Ú', 'U')
    return texto_sin_acentos

def filtrar_caracteres(texto):
    # Filtrar caracteres de exclamación e interrogación
    texto_filtrado = re.sub(r'[!¡?¿]', '', texto)  # Elimina !, ¡, ?, ¿
    return reemplazar_acentos(texto_filtrado)

#def main():
    host = '127.0.0.1'
    port = 12345
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    try:
        while True:
            message = raw_input("Mensaje para enviar al servidor: ")
            message = filtrar_caracteres(message)
            client_socket.sendall(message.encode('utf-8'))
            data = client_socket.recv(1024)
            print('Respuesta del servidor:', data.decode('utf-8'))
    finally:
        client_socket.close()

def main():
    mensajeprueba = u"¡Hola! ¿Cómo estás?"
    print(mensajeprueba)

    mensaje_filtrado = filtrar_caracteres(mensajeprueba)
    print(mensaje_filtrado)
    

if __name__ == "__main__":
    main()


