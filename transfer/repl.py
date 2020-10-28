#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""REPL.

Ofrece una clase para crear REPLs simples para NTransfer.
"""

# Módulos del PyPI.
from prompt_toolkit import print_formatted_text as print
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.shortcuts import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

# Módulos Propios.
from protocol import Transfer

class REPL:
    """Clase para crear REPLs compatibles con NTP."""

    prompt = '(NTP) '
    nickname = 'IP'

    def __init__(self, transfer: Transfer):
        self.t = transfer

        self.p = PromptSession(self.prompt,
            history=InMemoryHistory(),
            auto_suggest=AutoSuggestFromHistory(),
        )

    def main_loop(self):
        while True:
            try: usr = self.p.prompt()
            except KeyboardInterrupt: continue
            except EOFError: 
                print('Cerrando Chat...')
                break
            
            self.one_cmd(usr)
            self.receive()

    def one_cmd(self, cmd):
        """Ejecuta una línea."""

        cmd = cmd.strip()
        cmd = cmd.split(' ')

        if cmd[0].startswith('#'):
            if cmd[0].startswith('#file'):
                try: self.t.send_file(cmd[1])
                except OSError as err: 
                    print('Ocurrió un error:', err)
            else: print('No se reconoce el comando.')
            return

        cmd = ' '.join(cmd)

        self.t.send(bytes(cmd, 'utf-8'), 'text/plain')

    def print(self, text: str):
        """Imprime texto en pantalla."""

        style = FormattedText([
            ('red', f'{self.nickname}: '),
            ('gray', text),
        ])

        print(style)

    def receive(self):
        rec = self.t.receive()

        if rec[1]['mime'] != 'text/plain':
            path = self.p.prompt('Ruta donde desea guardar el archivo: ')
            with open(path, 'wb') as fp:
                fp.write(rec[0])

        else: self.print(rec[0].decode(rec[1]['encoding']))