#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Utils.

Utilidades para Nightly Transfer.
"""

##############################################################################
############################### MODULOS. #####################################
##############################################################################

# Módulos de la librería estándar.
import logging
from typing import Text

# Módulos del PyPI.
from prompt_toolkit.shortcuts.prompt import prompt, KeyBindings, Keys

##############################################################################
############################# CONSTANTES .####################################
##############################################################################

LOG_FORMAT = logging.Formatter(
    fmt='NTRANSFER: {levelname}: {name}: {message} [{asctime}].',
    datefmt='%I:%M-%S %p',
    style='{',
)

LOG_FORMAT_FILE = logging.Formatter(
    fmt='{levelname}: {message} [{asctime}].',
    datefmt='%I:%M-%S %p',
    style='{',
)

##############################################################################
############################## FUNCIONES .####################################
##############################################################################

def pause(text: Text = '\n  Presione una tecla para continuar... ') -> None:
    """Genera una pausa en la durante la ejecución.
    
    :text: Texto a mostrar, por ejemplo: "Presione 
           una tecla para continuar...".
    """

    bind = KeyBindings() # Crear un grupo de escuchas de teclas.

    @bind.add(Keys.Any)
    def _(event): event.app.exit() # Añadir el evento de salida.

    prompt(text, key_bindings=bind) # Iniciar la pausa.

##############################################################################
################################# FIN. #######################################
##############################################################################
