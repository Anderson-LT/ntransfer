#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Config.

Lee la información de un archivo de configuración.
"""

##############################################################################
################################# MÓDULOS. ###################################
##############################################################################

# Módulos de librería estándar.
from json import dump, load
from os.path import abspath, dirname
from os.path import join as join_path
from typing import Dict, Text, Union

##############################################################################
############################### CONSTANTES. ##################################
##############################################################################

# Archivo de configuración.
CONFIG_FILE = join_path(abspath(dirname(__file__)), 'ntp.json')
# Archivo de configuración para el formato PYZ.
CONFIG_FILE_PYZ = join_path(dirname(dirname(CONFIG_FILE)), 'ntp.json')
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

try: get_config()
except FileNotFoundError: 
    try: set_config(BASE_CONFIG)
    except FileNotFoundError:
        CONFIG_FILE = CONFIG_FILE_PYZ # Usar rutas para PYZ.
        try: get_config()
        except FileNotFoundError: set_config(BASE_CONFIG)
except OSError:
    print(
        'Verifique que no halla ningún achivo o carpeta llamada:' \
        f'"{CONFIG_FILE}".',
    )
    exit(1)

##############################################################################
################################### FIN. #####################################
##############################################################################
