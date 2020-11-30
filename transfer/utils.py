#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Utils.

Utilidades para Nightly Transfer.
"""

##############################################################################
############################### MODULOS. #####################################
##############################################################################

# Módulos de la librería estándar.
from typing import Text

# Módulos del PyPI.
from prompt_toolkit.shortcuts.prompt import prompt, KeyBindings, Keys

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
