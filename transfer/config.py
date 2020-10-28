#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Config.

Lee la información de un archivo de configuración.
"""

from json import dump, load
from os.path import dirname, abspath

CONFIG_FILE = abspath(dirname(__file__)) + '/ntp.json'
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

def get_config(file=CONFIG_FILE):
    """Carga la configuración de un archivo."""

    with open(file, 'rt') as fp:
        file = load(fp)

    return file

def set_config(config, file=CONFIG_FILE):
    """Establece la configuración de un archivo."""

    with open(file, 'wt') as fp:
        dump(
            config, 
            fp,
            indent=4,
            sort_keys=True,
        )

    return
