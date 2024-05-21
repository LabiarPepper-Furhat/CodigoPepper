# -*- coding: utf-8 -*-
import qi
import os
from dotenv import load_dotenv # type: ignore
load_dotenv()

def on_word_recognized(value):
    if len(value) > 0:
        # value[0] contiene la palabra reconocida y value[1] la confianza del reconocimiento
        recognized_word = value[0]
        confidence = value[1]
        print("Palabra reconocida: {} con confianza: {}".format(recognized_word, confidence))

def main():
    session = qi.Session()
    try:
        pepper_ip = os.getenv('IP_PEPPER')
        pepper_port = 9559
        session.connect("tcp://" + pepper_ip + ":" + str(pepper_port))
        
        # Obtener el servicio de reconocimiento de voz
        asr = session.service("ALSpeechRecognition")
        
        # Suscribirse al reconocimiento de voz
        asr.setLanguage("Spanish")
        asr.setVocabulary(["hola", "adios", "si", "no", "gracias"], False)  # Configurar un vocabulario básico
        asr.subscribe("SocketTest")
        
        # Suscribirse al evento 'WordRecognized'
        memory = session.service("ALMemory")
        memory.subscribeToEvent("WordRecognized", "PythonApplication", "on_word_recognized")

        print("Pepper esta escuchando...")
        while True:
            pass
            
    except KeyboardInterrupt:
        # Desuscribirse del reconocimiento de voz al finalizar
        asr.unsubscribe("SocketTest")
        print("Desuscripción completada.")
    except Exception as e:
        print("Error al conectar con el robot Pepper:", e)

if __name__ == "__main__":
    main()
