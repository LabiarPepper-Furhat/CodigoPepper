# -*- coding: utf-8 -*-
import qi
import os
import time
from dotenv import load_dotenv # type: ignore
load_dotenv()
def main():
    try:
        session = qi.Session()
        pepper_ip = os.getenv('IP_PEPPER')
        pepper_port = 9559
        session.connect("tcp://" + pepper_ip + ":" + str(pepper_port))
        
        # Obtener el servicio de reconocimiento de voz
        asr = session.service("ALSpeechRecognition")
        ms = session.service("ALMemory")
        
        # Suscribirse al reconocimiento de voz
        asr.setLanguage("Spanish")
        asr.pause(True)
    except Exception as e:
        print("Error al conectar con el robot Pepper:", e)
    try:
        asr.setVocabulary(["hola", "adios", "si", "no", "gracias"], True) 
    except RuntimeError as error:
        print(error)
        asr.removeAllContext()
        asr.setVocabulary(["hola", "adios", "si", "no", "gracias"], True)
        asr.subscribe("Test_ASR")
    try:
        print("Robot escuchando...")
        asr.pause(False)
        time.sleep(4)
        words=ms.getData("WordRecognized")
        print("palabras: "+words[0])
        print(words)
    except:
        pass
    

if __name__ == "__main__":
    main()
