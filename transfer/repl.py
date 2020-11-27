#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""REPL.

Ofrece una clase para crear REPLs simples para NTransfer.
"""

#############################################################################
################################# MÓDULOS. ##################################
#############################################################################

# Módulos de la librería estándar.
from typing import Text, Dict, Callable, List, Tuple
from shlex import split

# Módulos del PyPI.
from prompt_toolkit import print_formatted_text as print
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.shortcuts import PromptSession, confirm, ProgressBar
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

    def __init__(self, 
        transfer: Transfer, 
        cmds: 
            Dict[Text, 
                Callable[[List[Text]], Tuple[bytes, Text, Text]]] = None,
    ) -> None:
        """Constructor.

        :transfer: Es la clase con el protocolo.
        """

        self.t = transfer
        self.cmd = cmds
        
        # Crear el indicador.
        self.p = PromptSession(self.prompt, # Indicador.
            history=InMemoryHistory(), # Historial en memoria.
            auto_suggest=AutoSuggestFromHistory(), # Sugerencias basadas en 
        )                                          # el historial.

        # Indicador para guardar archivos.
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

        if cmd and cmd[0].startswith('#'): # Ejecutar en caso de ser un comando.
            cmd = cmd[1:] # Eliminar el carácter #.
            args = split(cmd) # Separar.

            if args[0] in self.cmd:
                cmd = self.cmd[args[0]]
                try: data, mime, encoding = cmd(args)
                except: 
                    print('Error mientras se procesaba el comando.')
                else: self.t.send(data, mime, encoding)
                finally: data =  mime = encoding = ''
                return
            else: print(f'{cmd.title()}: No se reconoce el comando.')
            return

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
        rec = self.t.receive(
            confirm=self.confirm,
            per_cent=self.progress_bar) # Recibir el mensaje en crudo.

        # Recibir un archivo, si no es texto.
        if rec[1]['mime'] != 'text/plain' and rec[0] is not None:
            path = self.pf.prompt()
            if path == '#cancel': return # Si el usuario cancela el archivo.
            with open(path, 'wb') as fp:
                fp.write(rec[0]) # Guardar el archivo.

        elif rec[0] is None: pass

        # Mostrar el mensaje.
        else: self.print(rec[0].decode(rec[1]['encoding']))

    def confirm(self, header):
        """Pregunta al usuario si dsea descargar algún archivo."""

        self._file = False # Variable para verificar archivos.
        if header['mime'] != 'text/plain': # Si es diferente de texto plano.
            self._file = True
            size = header['size'] # Tamaño en bytes.
            if size > 1024: # KiloByte.
                size = size / 1024
                size_str = f'{size:.2f} KiB'
            if int(size) > 1024: # MegaByte.
                size = size / 1024
                size_str = f'{size:.2f} MiB'
            else: # Byte.
                size_str = f'{size} B'

            yes_no = confirm(
                f'¿Desea recibir este archivo ({size_str})?',
                ' ([y] Sí | [n] No): '
            )
            if yes_no == False: self._file = False
            return yes_no
        else: return True

    def progress_bar(self, pc):
        """Muestra una barra de progreso."""

        # Verificar que sea un archivo.
        if self._file == False: return
        else: 
            try: self.pb # Verificar que no exista una barra de progreso.
            except AttributeError: 
                self._pb = ProgressBar() # Inicializar la barra.
                self._pb = self._pb.__enter__() # Crear la barra.
                self.pb = self._pb(range(100)) # Añadir la capacidad máxima.

            self.pb.items_completed = int(pc) # Fijar porcentaje.
            self.pb.progress_bar.invalidate() # Mostrar porcentaje.

            if pc == 100: # Si la barra está llena.
                self.pb.done = True # Fija hecho a vedadero.
                self._pb.__exit__() # Eliminar la barra.
                del self._pb, self.pb # Liberar memoria.

##############################################################################
############################## FUNCIONES. ####################################
##############################################################################

# Definir algunos comandos básicos (comienzan con cmd_).
# 
#  Todos los comandos deben comenzar con el prefijo "cmd_", para poderlos 
#  diferenciar de funciones ordinarias, estos se invocan desde la línea del 
#  REPL con un # seguido del nombre del comando.
#
#  Las funciones de comandos reciben una lista con los argumentos, deben
#  devolver una tupla conteniendo los siguiente:
#   ('datos binarios a enviar', 'tipo MIME', 'codificación')
#
#  El atributo __doc__ de las funciones, se utiliza como el texto de ayuda
#  para los comandos.
#

def cmd_file(args):
    """Envía un archivo.

    SINTAXÍS: #file ruta_del_archivo

    Si la ruta hacia el archivo contiene espacios, utilizar comillas 
    simples o dobles para evitar confundirlo con un segundo argumento.
    """

    with open(args[1], 'rb') as fp: file = fp.read()

    return (file, 'file/download', '')

##############################################################################
############################### CONSTANTES. ##################################
##############################################################################

# Comandos básicos.
CMDS = {
    'file': cmd_file
}

##############################################################################
################################## FIN. ######################################
##############################################################################
