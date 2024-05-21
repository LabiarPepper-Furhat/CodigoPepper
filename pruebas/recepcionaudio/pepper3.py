# -*- coding: utf-8 -*-
import qi
import os
import speech_recognition
import paramiko
from scp import SCPClient
import time
from dotenv import load_dotenv # type: ignore
load_dotenv()
def download_file(scp,file_name):
    scp.get(file_name, local_path="/tmp/")
    print("[INFO]: File " + file_name + " downloaded")
    scp.close()
def blink_eyes(ls,rgb):
    ls.fadeRGB('AllLeds', rgb[0], rgb[1], rgb[2], 1.0)
def speech_to_text(recognizer,audio_file):
    audio_file = speech_recognition.AudioFile("/tmp/" + audio_file)
    with audio_file as source:
        audio = recognizer.record(source)
        recognized = recognizer.recognize_google(audio, language="en_US")
    return recognized
def listen(asr,ar,ms,ls,scp,recognizer):
    asr.setAudioExpression(False)
    asr.setVisualExpression(False)
    ar.stopMicrophonesRecording()
    print("[INFO]: Speech recognition is in progress. Say something.")
    while True:
        print(ms.getData("ALSpeechRecognition/Status"))
        if ms.getData("ALSpeechRecognition/Status") == "SpeechDetected":
            ar.startMicrophonesRecording("/home/nao/speech.wav", "wav", 48000, (0, 0, 1, 0))
            print("[INFO]: Robot is listening to you")
            blink_eyes(ls,[255, 255, 0])
            break

    while True:
        if ms.getData("ALSpeechRecognition/Status") == "EndOfProcess":
            ar.stopMicrophonesRecording()
            print("[INFO]: Robot is not listening to you")
            blink_eyes([0, 0, 0])
            break

    download_file(scp,"speech.wav")
    asr.setAudioExpression(True)
    asr.setVisualExpression(True)

    return speech_to_text(recognizer,"speech.wav")
def main():
    try:
        session = qi.Session()
        pepper_ip = os.getenv('IP_PEPPER')
        pepper_port = 9559
        session.connect("tcp://" + pepper_ip + ":" + str(pepper_port))
        
        # Obtener el servicio de reconocimiento de voz
        asr = session.service("ALSpeechRecognition")
        ms=session.service("ALMemory")
        ar=session.service("ALAudioRecorder")
        recognizer = speech_recognition.Recognizer()
        ls=session.service("ALLeds")
        ssh = paramiko.SSHClient()
        scp = SCPClient(ssh.get_transport())
        
    except Exception as e:
        print("Error al conectar con el robot Pepper:", e)
    
    try:
        pepper_listen=listen(asr,ar,ms,ls,scp,recognizer)
        print("Pepper escucho: ",pepper_listen)
    except Exception as e:
        print("Error de pepper al escuchar", e)

if __name__ == "__main__":
    main()



# -*- coding: utf-8 -*-
'''
import qi
import os
import speech_recognition as sr
import paramiko
from scp import SCPClient
import time
from dotenv import load_dotenv # type: ignore
load_dotenv()
def download_file(scp, file_name):
    scp.get(file_name, local_path="/tmp/")
    print("[INFO]: File " + file_name + " downloaded")
    scp.close()

def blink_eyes(ls, rgb):
    ls.fadeRGB('AllLeds', rgb[0], rgb[1], rgb[2], 1.0)
def speech_to_text(recognizer, audio_file):
    audio_file = sr.AudioFile("/tmp/" + audio_file)
    with audio_file as source:
        audio = recognizer.record(source)
        recognized = recognizer.recognize_google(audio, language="en_US")
    return recognized
def listen(asr, ms, ar, ls):
    asr.setAudioExpression(False)
    asr.setVisualExpression(False)
    ar.stopMicrophonesRecording()
    print("[INFO]: Speech recognition is in progress. Say something.")
    while True:
        print(ms.getData("ALSpeechRecognition/Status"))
        if ms.getData("ALSpeechRecognition/Status") == "SpeechDetected":
            ar.startMicrophonesRecording("/home/nao/speech.wav", "wav", 48000, (0, 0, 1, 0))
            print("[INFO]: Robot is listening to you")
            blink_eyes(ls, [255, 255, 0])
            break

    while True:
        if ms.getData("ALSpeechRecognition/Status") == "EndOfProcess":
            ar.stopMicrophonesRecording()
            print("[INFO]: Robot is not listening to you")
            blink_eyes(ls, [0, 0, 0])
            break

    return "speech.wav"
def main():
    try:
        session = qi.Session()
        pepper_ip = os.getenv('IP_PEPPER')
        pepper_port = 9559
        session.connect("tcp://" + pepper_ip + ":" + str(pepper_port))
        
        # Obtener los servicios
        asr = session.service("ALSpeechRecognition")
        ms = session.service("ALMemory")
        ar = session.service("ALAudioRecorder")
        ls = session.service("ALLeds")
        
        recognizer = sr.Recognizer()
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(pepper_ip, username=os.getenv('PEPPER_USER'), password=os.getenv('PEPPER_PASSWORD'))
        scp = SCPClient(ssh.get_transport())
        
    except Exception as e:
        print("Error al conectar con el robot Pepper:", e)
        return
    
    try:
        print("Robot escuchando...")
        asr.pause(False)
        time.sleep(4)
        audio_file = listen(asr, ms, ar, ls)
        download_file(scp, audio_file)
        recognized_text = speech_to_text(recognizer, audio_file)
        print("Recognized Text:", recognized_text)
    except Exception as e:
        print("Error during speech recognition:", e)
    
if __name__ == "__main__":
    main()
'''