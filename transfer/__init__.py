#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Nightly Transfer Protocol.

Es un protocolo de transferencia muy ligero y rápido, pensado para
hacer transferencias entre dos dispositivos (cliente-servidor).
"""

##############################################################################
############################## META-DATOS ####################################
##############################################################################

__author__ = 'Anderson Lizarazo Tellez.'
__credits__ = 'Ninguno Todavía.'
__date__ = 'Viernes, 27 de Noviembre de 2020.'
__copyright__ = '© 2020, Andrson Lizarazo Tellez.'
__license__ = 'Aurora License 0.1.'
__version__ = '0.0.2'

get_version = lambda: __version__.split('.') + ['preview']

# Añadir compatibilidad para "from transfer import *".
__all__ = [
    # Funciones.
    get_version,
    # Módulos.
    'protocol',
    'repl',
]

##############################################################################
################################## FIN. ######################################
##############################################################################
