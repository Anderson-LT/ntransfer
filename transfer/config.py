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
from typing import Dict, Text

##############################################################################
############################### CONSTANTES. ##################################
##############################################################################

CONFIG_FILE = join_path(abspath(dirname(__file__)), 'ntp.json')
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

def get_config(file: Text = CONFIG_FILE):
    """Carga la configuración de un archivo.
    
    :file: Es la ruta donde se buscará la configuración.
    """

    with open(file, 'rt') as fp:
        file = load(fp)

    return file

def set_config(config: Dict[Dict, Dict], file: Text = CONFIG_FILE):
    """Establece la configuración de un archivo.
    
    :file:   Es la ruta donde se guardará la configuración.
    :config: Debe ser un diccionario conteniendo otros dos diccionarios, cada 
             uno contiene un aspecto de configuración de NTP (Ver la constante 
             "CONFIG_FILE").
    """

    with open(file, 'wt') as fp:
        dump(
            config, 
            fp, 
            indent=4,        # Identar el archivo.
            sort_keys=True,  # Ordenar las claves.
        )

    return

##############################################################################
################################### FIN. #####################################
##############################################################################
