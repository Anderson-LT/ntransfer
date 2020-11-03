#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Nightly Transfer Protocol.

Define un protocolo de transferencia simple y de alto nivel para Socket.
"""

##############################################################################
############################### META-DATOS. ##################################
##############################################################################

__author__ = 'Anderson Lizarazo Tellez'
__date__ = 'Martes, 27 de Octubre de 2020.'
__copyright__ = '© 2020, Anderson Lizarazo Tellez.'
__license__ = 'Aurora License 0.1.'
__version__ = '0.0.1'
version_info = __version__.split('.').append('preview')

##############################################################################
################################# MÓDULOS. ###################################
##############################################################################

# Módulos de la librería estándar.
import json
import mimetypes
import socket
import zlib
from typing import IO, BinaryIO, NewType, Text, Tuple, Union

##############################################################################
################################ CONSTANTES. #################################
##############################################################################

# Valores más comunes de la cabecera.
PROTO = 'ntp'
VERSION = __version__[:]
UTF8 = 'utf-8'

# Tamaños en bytes.
B = 1
KB = B * 1024

##############################################################################
################################ TYPING. #####################################
##############################################################################

Socket = NewType('Socket', socket.socket)

##############################################################################
################################ CLASES. #####################################
##############################################################################

class Transfer:
    """Genera una interfaz de alto nivel para Socket."""

    bufsize = KB

    def __init__(self, connection: Socket) -> None:
        """Constructor.
        
        :connection: Recibe un objeto Socket ya conectado.
        """

        self.connection = connection

    def send(self, data: bytes, mime: Text, encoding: Text = UTF8) -> int:
        """Envia un objeto binario utilizando el protocolo NTP.
        
        :data: Son los datos a enviar.
        :mime: Tipo MIME del objeto a enviar.
        :encoding: Codificación del objeto a envia (solo para texto).

        Devuelve el número de octetos enviados.

        Los argumentos mime y encoding solo son meta-datos y su correcta 
        interpretación depende del cliente utilizado.
        """

        # Lista con las partes del cuerpo del mensaje.
        message = []

        # Generar la cabecera.
        header = self.__make_header(
            len(data),
            mime,
            encoding,
        )

        # Armar el mensaje.
        message.append(self.__len_header(header)) # Longitud de la cabecera.
        message.append(header) # Cabecera.
        message.append(data) # Cuerpo del mensaje.
        
        # Unir el mensaje.
        msg = b''.join(message)

        # Enviar el mensaje.
        self.connection.sendall(msg)

        # Devolver la cantidad de bytes enviados.
        return len(msg)

    def send_file(self, path: Union[Text, IO], binary: bool = True) -> int:
        """Envía un archivo.
        
        :path:   Es la ruta donde se encuentra el archivo, también puede pasar
                 el objeto retornado por la función "open", el único requisito
                 es tener acceso de lectura.
        :binary: Es un "bool" indicando si el objeto usa una codificación
                 binaria, es decir, una imagen, un vídeo, etc...

        Esto es solo un envoltorio para el método "send", también devuelve
        el número de octetos enviados.
        """

        # Crear el lector en caso de recibir una ruta.
        if isinstance(path, str):
            mode = 'rb' if binary else 'r'
            path = open(path, mode)

        # Obtener el contenido.
        content = path.read()

        # Obtener el tipo MIME.
        mime = mimetypes.guess_type(path.name)
        mime = mime[1] if mime[1] else mime[0]

        # Obtener la codificación.
        try: encoding = path.encoding
        except AttributeError: encoding = None

        # Cerrar el puntero al archivo, si fué creado aquí.
        if isinstance(path, str): path.close()

        return self.send(content, mime, encoding)

    def receive(self, bufsize: int = bufsize) -> Tuple[bytes, dict]:
        """Recibe contenido de la conexión.
        
        :bufsize: Es el número máximo de octetos que recibirán en cada 
                  solicitud, por defecto es el atributo "Transfer.bufsize", 
                  debe ser un entero.
        
        Retorna una tupla conteniendo el mensaje y su cabecera.
        """

        # Obtener tamaño de la cabecera.
        hlen = self.connection.recv(4)

        # Obtener la cabecera y decodificarla.
        header = self.connection.recv(int(hlen))
        header = header.decode(UTF8)
        header = json.loads(header)

        # Obtener tamaño del mensaje.
        size = header['size']

        # Partes del mensaje y cantidad de datos recibidos.
        msg = []
        rec = 0

        # Recibir el mensaje por partes.
        while rec < size: 
            if rec < bufsize: # En caso de ser la última parte del mensaje.
                bufsize = size - rec # Fijar el bufér al tamaño del mensaje.
            r = self.connection.recv(bufsize) # Recibir una parte del mensaje.
            rec += len(r) # Contar el tamaño del mensaje recibido.
            msg.append(r) # Almacenar las partes del mensaje recibidas.

        # Juntar todas las partes del mensaje.
        content = b''.join(msg)

        # Devolver el mensaje y la cabecera.
        return content, header

    def __make_header(self, size, mime, encoding, protocol=PROTO, 
    version=VERSION):

        # Armar la cabecera.
        header = {
            'protocol': protocol,
            'version': version,
            'mime': mime,
            'encoding': encoding,
            'size': size,
        }

        # Codificar la cabecera.
        header = json.dumps(header, 
            ensure_ascii=True, 
            indent=None, 
            sort_keys=True)

        # Compilar la cabecera.
        header = bytes(header, UTF8)

        return header

    def __read_header(self, header):

        # Descodificar la cabecera.
        header = header.decode(UTF8)
        header = json.loads(header)

        return header

    def __len_header(self, header): 

        # Contar el número de dígitos de la cabecera.
        h = str(len(header))

        # Añadir tantos ceros como sea necesario.
        if len(h) > 4: raise OverflowError('La cabecera es muy larga.')
        elif len(h) == 3: h = '0' + h
        elif len(h) == 2: h = '00' + h
        elif len(h) == 1: h = '000' + h
        
        return bytes(h, UTF8)

    def __len_content(self, content):

        # Tamaño de la cabecera.
        return len(content)

##############################################################################
################################### FIN. #####################################
##############################################################################
