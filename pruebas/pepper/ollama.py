# -*- coding: utf-8 -*-
import json
import socket
import requests
import re

# NOTE: ollama must be running for this to work, start the ollama app or run `ollama serve`
model = "llama3"  # TODO: update this for whatever model you wish to use
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
            # the response streams one token at a time, print that as we receive it
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
                print('Recibido:', data.decode())
                messages = [{"role": "user", "content": data.decode()}]
                message = chat(messages)
                print("\n")
                conn.sendall(message["content"].encode())


if __name__ == "__main__":
    main()
