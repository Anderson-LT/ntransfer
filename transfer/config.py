#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Config.

Lee la información de un archivo de configuración.
"""

##############################################################################
################################# MÓDULOS. ###################################
##############################################################################

# Módulos de librería estándar.
import logging
from json import dump, load
from os.path import abspath, dirname
from os.path import join as join_path
from typing import Dict, Text, Union
from utils import LOG_FORMAT, LOG_FORMAT_FILE

##############################################################################
############################### REGISTROS. ###################################
##############################################################################

logger = logging.getLogger(__name__)

# Fijar el nivel a DEBUG.
#  Si está ayudando al dsarrollo, des-comente la siguiente línea.
#logger.setLevel(logging.DEBUG)

# Crear un manejador de consola.
_log_console = logging.StreamHandler()
#_log_file = logging.FileHandler('./ntransfer_config.log', 'w', 'utf-8')

# Añadir el formato.
_log_console.setFormatter(LOG_FORMAT)
#_log_file.setFormatter(LOG_FORMAT_FILE)

# Añadir los manejadores al registrador.
logger.addHandler(_log_console)
#logger.addHandler(_log_file)

##############################################################################
############################### CONSTANTES. ##################################
##############################################################################

# Archivo de configuración.
CONFIG_FILE = join_path(abspath(dirname(__file__)), 'ntp.json')
logger.debug(
    'La ruta inicial del archivo de configuración es: "%s"', 
    CONFIG_FILE,
)
# Archivo de configuración para el formato PYZ.
CONFIG_FILE_PYZ = join_path(dirname(dirname(CONFIG_FILE)), 'ntp.json')
logger.debug(
    'La ruta inicial del archivo de configuración PYZ es: "%s"', 
    CONFIG_FILE_PYZ,
)
BASE_CONFIG = {
    'colors': {
        'nickname': 'red',
        'message': 'white',
        'prompt': 'white',
        'user': 'white',
    },
    'connections': {
        'localhost': ('localhost', 22314),
        'public': ('10.1.10.1', 22314),
    },
}

##############################################################################
################################ FUNCIONES. ##################################
##############################################################################

def get_config(file: Union[Text, None] = None):
    """Carga la configuración de un archivo.
    
    :file: Es la ruta donde se buscará la configuración.

    Si "file" es "None" se utilizará el valor de la variable "CONFIG_FILE".
    """

    if file is None: file = CONFIG_FILE
    logger.debug('Obteniendo configuración del archivo: "%s"', file)

    with open(file, 'rt') as fp:
        file = load(fp)

    return file

def set_config(config: Dict[Dict, Dict], file: Union[Text, None] = None):
    """Establece la configuración de un archivo.
    
    :file:   Es la ruta donde se guardará la configuración.
    :config: Debe ser un diccionario conteniendo otros dos diccionarios, cada 
             uno contiene un aspecto de configuración de NTP (Ver la constante 
             "CONFIG_FILE").

    Si "file" es "None" se utilizará el valor de la variable "CONFIG_FILE".
    """

    if file is None: file = CONFIG_FILE
    logger.debug('Estableciendo configuración en el archivo: "%s"', file)

    with open(file, 'wt') as fp:
        dump(
            config, 
            fp, 
            indent=4,        # Identar el archivo.
            sort_keys=True,  # Ordenar las claves.
        )

    return

##############################################################################
############################ RUTINA PRINCIPAL. ###############################
##############################################################################

try: 
    logger.info('Probando disponibilidad del archivo de configuración')
    get_config()
except: 
    try: 
        logger.warning(
            'Podría sobre-escribirse el archivo: "%s"', 
            CONFIG_FILE,
        )
        set_config(BASE_CONFIG)
    except (FileNotFoundError, NotADirectoryError):
        logger.info('Usando ruta PYZ por defecto')
        CONFIG_FILE = CONFIG_FILE_PYZ # Usar rutas para PYZ.
        try: 
            logger.info(
                'Probando disponibilidad del archivo de configuración PYZ'
            )
            get_config()
        except FileNotFoundError: 
            logger.warning(
                'Podría sobre-escribirse el archivo: "%s"', 
                CONFIG_FILE,
            )
            set_config(BASE_CONFIG)

##############################################################################
################################### FIN. #####################################
##############################################################################
