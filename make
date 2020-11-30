#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Make.

Archivo de ordenes para crear binarios.
"""

import os
import os.path as path
import shutil

import sys

import zipapp

__version__ = '1'

PWD = os.getcwd()
PYTHON = '/usr/bin/env python3'
BUILD = path.join(PWD, '.tmp')

DEPENDENCES = [
    path.join(PWD, 'Lib', 'site-packages', 'prompt_toolkit'),
    path.join(PWD, 'Lib', 'site-packages', 'wcwidth'),
    path.join(PWD, 'Lib', 'site-packages', 'pygments'),
]

PROJECT = path.join(PWD, 'transfer')

PROJECT_VERSION = '0.0.2'
PROJECT_NAME = 'transfer'
PROJECT_STATE = 'preview'

TARGET = path.join(PWD, 'dist', 'PYZ')

CRASH = [
    '__pycache__',
    'ntp.json',
]

def error(description: str, code: int = 1) -> None:
    """Imprime un error a la salida de error estándar y cierra el programa."""

    print(f'\n\nMAKE: Error {code}: {str(description).capitalize()}.')
    sys.exit(code)

def copy_deps():
    """Copia las dependencias a un diectorio temporal."""    

    for dep in DEPENDENCES: shutil.copytree(dep, path.join(BUILD, path.split(dep)[-1]))

def copy_project():
    """Copia el proyeto a un directorio temporal."""

    shutil.copytree(PROJECT, BUILD)

def clean_crash():
    """Elimina la caché y archivos de configuración."""

    for crash in CRASH:
        try: os.remove(path.join(BUILD, crash))
        except OSError: shutil.rmtree(path.join(BUILD, crash))

def pyz(target):
    """Genera un archivo PYZ."""
    zipapp.create_archive(BUILD, target, PYTHON, compressed=True)

def main(args=sys.argv):
    """Rutina Principal."""

    print('PROYECTO:', PROJECT_NAME)
    print('VERSIÓN:', PROJECT_VERSION)
    print('ESTADO:', PROJECT_STATE)
    print('RUTA:', PROJECT, '\n')

    print('La versión del script de compilación es:', __version__, '\n')

    if path.exists(BUILD):
        print('Eliminando Residuos De Compilación Anterior...', end=' ')
        shutil.rmtree(BUILD)
        print('Hecho.')

    try: 
        input(
            'Verifique que todos los datos sean correctos, para cancelar ' \
            'la operación presione: "CTRL-C" o "CTRL-D", si desea ' \
            'continuar presione "ENTER": '
        )
    except KeyboardInterrupt: sys.exit(0)
    except EOFError: sys.exit(0)
    except RuntimeError as err: error(err, 9)

    print('Copiando Proyecto...', end=' ')
    copy_project()
    clean_crash()
    print('Hecho.')

    print('Generando Ejecutable Ligero...', end=' ')
    pyz(
        path.join(
            TARGET, 
            f'{PROJECT_NAME}{PROJECT_VERSION}{PROJECT_STATE}.pyz'
        )
    )
    print('Hecho.')

    print('Copiando Dependencias...', end=' ')
    copy_deps()
    print('Hecho.')

    print('Generando Ejecutable Completo...', end=' ')
    pyz(
        path.join(
            TARGET, 
            f'{PROJECT_NAME}{PROJECT_VERSION}{PROJECT_STATE}_full.pyz'
        )
    )
    print('Hecho.')

    print('Eliminando Archivos De Compilación Sobrantes...', end=' ')
    shutil.rmtree(BUILD)
    print('Hecho.')

if __name__ == '__main__': 
    try: main()
    except BaseException as err: error(err, 1)
