#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##############################################################################
################################ MÓDULOS. ####################################
##############################################################################

# Módulos de la librería estándar.
import sys
from socket import gaierror as GAIError
from socket import socket

# Módulos del PyPI.
from prompt_toolkit.shortcuts import confirm, prompt

# Módulos propios.
from config import BASE_CONFIG, get_config, set_config
from protocol import ConnectionBrokenError, Transfer
from repl import CMDS, REPL
from utils import pause

##############################################################################
############################# RUTINA PRINCIPAL. ##############################
##############################################################################

# Pedir datos básicos.
url = prompt(
"""
Introduzca la dirección con el formato:
    i.p:port
Si tiene guardados atajos, escribalos con el formato:
    #atajo

Introduzca su dirección: """
)

# Obtener atajos.
name = get_config()['connections']

# Si es atajo.
if url.startswith('#'):
    try: conn = name[url[1:]]
    except KeyError:
        print('No existe ese atajo.')
        pause()
        sys.exit(1)
    conn = tuple(conn)
    nm = url[1:]
else:
    conn = url.split(':')
    try: conn[1] = int(conn[1])
    except IndexError:
        print('Sintaxis Inválida.')
        pause()
        sys.exit(1)
    except ValueError:
        print('Las direcciones solo están conformadas por números.')
        pause()
        sys.exit(1)
    conn = tuple(conn)
    nm = None

# Obtener desición.
server = confirm('¿Desea ser un servidor?', ' ([y] Sí | [n] No): ')

# Crear el socket.
socket = socket()

if server:
    # Crear la escucha.
    try: socket.bind(conn)
    except OSError: 
        print('La dirección no está disponible para ser usada como servidor.')
        pause()
        sys.exit(1)
    except GAIError:
        print('No es una dirección válida.')
        pause()
        sys.exit(1)
    # Escuchar solamente una conexión.
    socket.listen(1)
    # Acceptar la conexión.
    c, _ = socket.accept()
else:
    try: socket.connect(conn) # Conectar como cliente.
    except OSError:
        print('Esta dirección no tiene servidor.')
        pause()
        sys.exit(1)

# Crear el protocolo.
if server: t = Transfer(c)
else: t = Transfer(socket)

# Crear e iniciar el REPL.
repl = REPL(t, CMDS)
if nm: repl.nickname = nm

# Iniciar el REPL, y manejar los posibles errores.
try: repl.main_loop()
except ConnectionBrokenError: 
    print('Conexión finalizada.')
    pause()
except ConnectionAbortedError: 
    print('Se ha anulado la conexión.')
    pause()
except ConnectionResetError: 
    print('Se ha forzado la interrupción de la conexión.')
    pause()

# Cerrar las conexiones.
if server: c.close()
socket.close()

##############################################################################
################################### FIN. #####################################
##############################################################################
