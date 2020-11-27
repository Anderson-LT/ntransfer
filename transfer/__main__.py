#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from socket import socket
from protocol import Transfer, ConnectionBrokenError
from repl import REPL, CMDS
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

name = get_config()['connections']

if url.startswith('#'):
    conn = name[url[1:]]
    conn = tuple(conn)
    nm = url[1:]
else:
    conn = url.split(':')
    conn[1] = int(conn[1])
    conn = tuple(conn)
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
repl = REPL(t, CMDS)
if nm: repl.nickname = nm

# Iniciar el REPL, y manejar los posibles errores.
try: repl.main_loop()
except ConnectionBrokenError: print('Conexión finalizada.')
except ConnectionAbortedError: print('Se ha anulado la conexión.')
except ConnectionResetError: 
    print('Se ha forzado la interrupción de la conexión.')

# Cerrar las conexiones.
if server: c.close()
socket.close()
