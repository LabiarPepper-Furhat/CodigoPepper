# -*- coding: utf-8 -*-
import socket
import qi
import os
from dotenv import load_dotenv # type: ignore
load_dotenv()

def establecer_conexion():
    host = '127.0.0.1'
    port = 12345
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    return client_socket

def main():
    session = qi.Session()
    client_socket = establecer_conexion()
    try:
        pepper_ip = os.getenv('IP_PEPPER')
        pepper_port = 9559
        session.connect("tcp://" + pepper_ip + ":" + str(pepper_port))
        
        # Obtener el servicio de reconocimiento de voz
        asr = session.service("ALSpeechRecognition")
        tts = session.service("ALTextToSpeech")
        
        # Suscribirse al reconocimiento de voz
        asr.setLanguage("Spanish")
        asr.subscribe("SocketTest")
        
        # Manejar eventos de reconocimiento de voz
        print("Pepper esta escuchando...")
        while True:
            # Esperar hasta que se detecte un mensaje
            mensaje_escuchado = asr.recognize().encode()  # Reconocer la voz y codificarla como bytes
            #mensaje_escuchado = raw_input("Mensaje para enviar al servidor: ")
            print("Mensaje escuchado:", mensaje_escuchado)
            client_socket.sendall(mensaje_escuchado)
            data = client_socket.recv(1024)
            mensaje_recibido = data.decode()  # Decodificar los bytes a cadena de texto
            tts.say(mensaje_recibido)
            print('Respuesta del servidor:', mensaje_recibido)
            
    except KeyboardInterrupt:
        # Desuscribirse del reconocimiento de voz al finalizar
        asr.unsubscribe("SocketTest")
        print("Desuscripción completada.")
    except Exception as e:
        print("Error al conectar con el robot Pepper:", e)

if __name__ == "__main__":
    main()
