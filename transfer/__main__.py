#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from socket import socket
from protocol import Transfer
from repl import REPL
from config import get_config, set_config, BASE_CONFIG
from prompt_toolkit.shortcuts import prompt, confirm

# Pedir datos básicos.
url = prompt(
"""
Introduzca la dirección con el formato:
    i.p:port
Si tiene guardados atajos, escribalos con el formato:
    #atajo

Introduzca su dirección: """
)

while True:
    try: name = get_config()['connections']
    except FileNotFoundError: set_config(BASE_CONFIG)
    except: 
        print('Error desconocido.')
        exit(1)
    else: break

if url.startswith('#'):
    conn = name[url[1:]]
    conn = tuple(conn)
    nm = url[1:]
else:
    conn = url.split(':')
    nm = None

server = confirm('¿Desea ser un servidor?', ' ([y] Sí | [n] No): ')

# Crear el socket.
socket = socket()

if server:
    # Crear la escucha.
    socket.bind(conn)
    # Escuchar solamente una conexión.
    socket.listen(1)
    # Acceptar la conexión.
    c, _ = socket.accept()
else:
    socket.connect(conn)

# Crear el protocolo.
if server: t = Transfer(c)
else: t = Transfer(socket)

# Crear e iniciar el REPL.
repl = REPL(t)
if nm: repl.nickname = nm
repl.main_loop()

# Cerrar las conexiones.
if server: c.close()
socket.close()
