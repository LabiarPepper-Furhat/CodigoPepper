# -*- coding: utf-8 -*-

# Este código es una prueba para recibir, enviar mensajes a ollama y enviar respuestas del modelo al código en Python 2.7.18
# Python 3.12.3

import json
import socket
import requests
import re

# NOTA: ollama debe estar en ejecución para que esto funcione, inicia la aplicación ollama o ejecuta `ollama serve`
modelo = "llama3"  # TODO: actualiza esto con el modelo que desees utilizar

def reemplazar_acentos(texto):
    # Reemplazar letras con acento por las equivalentes sin acento
    texto_sin_acentos = texto.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
    texto_sin_acentos = texto_sin_acentos.replace('Á', 'A').replace('É', 'E').replace('Í', 'I').replace('Ó', 'O').replace('Ú', 'U')
    return texto_sin_acentos
def filtrar_caracteres(texto):
    # Filtrar caracteres de exclamación e interrogación
    texto_filtrado = re.sub(r'[!¡?¿]', '', texto)  # Elimina !, ¡, ?, ¿
    return reemplazar_acentos(texto_filtrado)


def chat(messages):
    r = requests.post(
        "http://localhost:11434/api/chat",
        json={"model": model, "messages": messages, "stream": True},
    )
    r.raise_for_status()
    output = ""

    for line in r.iter_lines():
        body = json.loads(line)
        if "error" in body:
            raise Exception(body["error"])
        if body.get("done") is False:
            message = body.get("message", "")
            content = message.get("content", "")
            output += content
            # la respuesta se transmite un token a la vez, imprímelo a medida que lo recibimos
            print(content, end="", flush=True)

        if body.get("done", False):
            message["content"] = filtrar_caracteres(output)
            return message


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

                messages = [{"role": "user", "content": data.decode()}]
                message = chat(messages)
                messages.append(message)
                print("\n")
                conn.sendall(message["content"].encode())


if __name__ == "__main__":
    main()
