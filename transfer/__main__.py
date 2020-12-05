#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##############################################################################
################################ MÓDULOS. ####################################
##############################################################################

# Módulos de la librería estándar.
import logging
import sys
from socket import gaierror as GAIError
from socket import socket

# Módulos del PyPI.
from prompt_toolkit.shortcuts import confirm, prompt

# Módulos propios.
from config import BASE_CONFIG, get_config, set_config
from protocol import ConnectionBrokenError, Transfer, logger as t_logger
from repl import CMDS, REPL
from utils import LOG_FORMAT, LOG_FORMAT_FILE, pause

##############################################################################
############################# RUTINA PRINCIPAL. ##############################
##############################################################################


# Crear el registrador.
logger = logging.getLogger(__name__)

# Fijar el nivel a DEBUG.
#logger.setLevel(logging.DEBUG)

# Crear un manejador de consola y archivo.
_log_console = logging.StreamHandler()
#_log_file = logging.FileHandler('./ntransfer.log', 'w', 'utf-8')

# Añadir el formato.
_log_console.setFormatter(LOG_FORMAT)
#_log_file.setFormatter(LOG_FORMAT_FILE)

# Añadir los manejadores al registrador.
logger.addHandler(_log_console)
#logger.addHandler(_log_file)
t_logger.addHandler(_log_console)

# Pedir datos básicos.
try: 
    url = prompt(
'''
Introduzca la dirección con el formato:
    i.p:port
Si tiene guardados atajos, escribalos con el formato:
    #atajo

Introduzca su dirección: '''
)
except EOFError: sys.exit(0)
except KeyboardInterrupt: sys.exit(0)

logger.debug('El texto introducido es: "%s"', url)

# Obtener atajos.
logger.info('Obteniendo atajos del archivo de configuración')
name = get_config()['connections']

# Si es atajo.
if url.startswith('#') and len(url) > 1:
    try: conn = name[url[1:]]
    except KeyError:
        logger.critical('No existe el atajo "%s"', url[1:])
        pause()
        sys.exit(1)
    conn = tuple(conn)
    nm = url[1:]
else:
    conn = url.split(':')
    try: conn[1] = int(conn[1])
    except IndexError:
        logger.critical('La sintaxís no es válida')
        pause()
        sys.exit(1)
    except ValueError:
        logger.critical('El puerto debe ser un número, no "%s"', conn[1])
        pause()
        sys.exit(1)
    conn = tuple(conn)
    nm = None

# Obtener desición.
server = confirm('¿Desea ser un servidor?', ' ([y] Sí | [n] No): ')
logger.debug('La elección del usuario al ser servidor es: %s', server)

# Crear el socket.
logger.info('Creando zócalo de red')
socket = socket()

if server:
    # Crear la escucha.
    logger.debug('Escuchando la dirección "%s:%d"', *conn)
    try: socket.bind(conn)
    except OSError: 
        logger.critical('La dirección no está disponible para ser usada como servidor')
        pause()
        sys.exit(1)
    except GAIError:
        logger.critical('No es una dirección válida.')
        pause()
        sys.exit(1)
    # Escuchar solamente una conexión.
    logger.info('Aceptando solamente una conexión')
    socket.listen(1)
    # Acceptar la conexión.
    c, ip = socket.accept()
    logger.debug('Conexión aceptada por: "%s:%d"', *ip)
else:
    logger.debug('Conectando como cliente a la dirección "%s:%d"', *conn)
    try: socket.connect(conn) # Conectar como cliente.
    except OSError:
        logger.critical('Esta dirección no tiene servidor.')
        pause()
        sys.exit(1)

# Crear el protocolo.
logger.info('Creando el manejador para el protocolo NTP')
if server: t = Transfer(c)
else: t = Transfer(socket)

# Crear e iniciar el REPL.
logger.info('Creando REPL')
repl = REPL(t, CMDS)
if nm: 
    logger.debug('Estableciendo apodo del REPL a "%s"', nm)
    repl.nickname = nm

# Iniciar el REPL, y manejar los posibles errores.
logger.info('Iniciando bucle principal del REPL')
try: repl.main_loop()
except ConnectionBrokenError: 
    logger.info('Conexión finalizada')
    print('Conexión finalizada.')
    pause()
except ConnectionAbortedError: 
    logger.error('Se ha anulado la conexión')
    pause()
except ConnectionResetError: 
    logger.error('Se ha forzado la interrupción de la conexión')
    pause()

# Cerrar las conexiones.
if server: 
    logger.info('Cerrando conexión del servidor dedicada al cliente')
    c.close()
logger.info('Cerrando conexión principal')
socket.close()

##############################################################################
################################### FIN. #####################################
##############################################################################
