#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""REPL.

Ofrece una clase para crear REPLs simples para NTransfer.
"""

#############################################################################
################################# MÓDULOS. ##################################
#############################################################################

# Módulos de la librería estándar.
from typing import Text

# Módulos del PyPI.
from prompt_toolkit import print_formatted_text as print
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.shortcuts import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

# Módulos Propios.
from protocol import Transfer

#############################################################################
################################# CLASES. ###################################
#############################################################################

class REPL:
    """Clase para crear un chat simpl con NTP."""

    prompt = '(NTP) '
    nickname = 'IP'

    def __init__(self, transfer: Transfer) -> None:
        """Constructor.

        :transfer: Es la clase con el protocolo.
        """

        self.t = transfer
        
        # Crear el indicador.
        self.p = PromptSession(self.prompt, # Indicador.
            history=InMemoryHistory(), # Historial en memoria.
            auto_suggest=AutoSuggestFromHistory(), # Sugerencias basadas en 
        )                                          # el historial.

        self.pf = PromptSession('Ruta donde desea guardar el archivo: ')

    def main_loop(self) -> None:
        """Inicia una sesión en el intérprete."""

        while True:
            try: usr = self.p.prompt()         # Solicitar una entrada.
            except KeyboardInterrupt: continue # Si presiona CTRL-C, pasar.
            except EOFError:                   # Con CTRL-D, cerrar el chat.
                print('Cerrando Chat...')
                break
            
            # Ejecutar el comando.
            self.one_cmd(usr)
            # Recibir algún mensaje.
            self.receive()

    def one_cmd(self, cmd: Text) -> None:
        """Ejecuta una línea.

        Este puede ser sobre-instanciado por una sub-clase.
        """

        cmd = cmd.strip() # Eliminar el exceso de espacios.
        cmd = cmd.split(' ') # Separar en cada espacio.

        if cmd[0].startswith('#'): # Ejecutar en caso de ser un comando.
            if cmd[0].startswith('#file'): # Comando para enviar archivo.
                try: self.t.send_file(cmd[1]) # Enviar el archivo.
                except OSError as err: 
                    print('Ocurrió un error:', err)
            else: print('No se reconoce el comando.')
            return

        cmd = ' '.join(cmd) # Rearmar la línea.

        # Enviar el mensaje.
        self.t.send(bytes(cmd, 'utf-8'), 'text/plain') 

    def print(self, text: Text) -> None:
        """Imprime un mensaje en pantalla.
        
        Puede ser sobre-instanciado por una sub-clase.
        """

        style = FormattedText([
            ('red', f'{self.nickname}: '), # Mostrar de color rojo el usuario.
            ('gray', text), # Mostrar de color gris el mensaje.
        ])

        # Imprimir el mensaje.
        print(style)

    def receive(self):
        rec = self.t.receive() # Recibir el mensaje en crudo.

        # Recibir un archivo, si no es texto.
        if rec[1]['mime'] != 'text/plain':
            path = self.pf.prompt()
            with open(path, 'wb') as fp:
                fp.write(rec[0]) # Guardar el archivo.

        # Mostrar el mensaje.
        else: self.print(rec[0].decode(rec[1]['encoding']))

##############################################################################
################################## FIN. ######################################
##############################################################################
