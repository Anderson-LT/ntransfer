# ARQUITECTURA.

Nightly Transfer utiliza una arquitectura similar a la del protocolo HTTP.

El puerto utilizado por NTransfer de forma predeterminada es ***22314***.

## ESTABLECER CONEXIÓN.

Llamaremos `houseland` y `lionsden` al servidor y el cliente respectiva-mente.

Para comenzar *houseland* de escuchar algún puerto, en este caso el **22314**,
además de una dirección, en este caso elegimos **10.1.10.1**, por lo tanto el 
resultado sería **10.1.10.1:22314**, una vez *lionsden* se conecte, puede
comenzar a enviar menajes, por ejemplo, *"¡Hola Mundo!."*.

### CUERPO DEL MENSAJE.

```
+----------------------------------------------------------------------------+
| TAMAÑO DE LA CABECERA:                                                     |
| 0123 Bytes.                                                                |
+----------------------------------------------------------------------------+
     |
     V
+----------------------------------------------------------------------------+
| CABECERA:                                                                  |
| {                                                                          |
|     'protocol': 'ntp',                                              |
|     'version': '0.0.1',                                                    |
|     'mime': 'text/plain',                                                  |
|     'encoding': 'utf-8',                                                   |
|     'size': 14                                                             |
| }                                                                          |
+----------------------------------------------------------------------------+
                                                                        |    
                                                                        V
+----------------------------------------------------------------------------+
| MENSAJE:                                                                   |
| ¡Hola Mundo!.                                                              |
+----------------------------------------------------------------------------+
```

#### EXPLICACIÓN.

Primero se envian cuatro *octetos* de forma arbitraria, que son los que contienen el tamaño de la cabecera (en bytes), si el tamaño es menor a cuatro
digitos, se añaden tantos ceros como sean necesarios al comienzo.

```
0123
```

Luego, se envia la cabecera, en formato *JSON*, esta contiene información como el protocolo utilizado, su versión, el tipo *MIME* del objeto, su codificación
(en caso de ser necesaria, de lo contrario es una cadena vacía) y por último 
su tamaño en bytes.

```json
{
    'protocol': 'n-transfer',
    'version': '0.0.1',
    'mime': 'text/plain',
    'encoding': 'utf-8',
    'size': 14
}
```

Para finalizar se envía el mensaje.

```
¡Hola Mundo!.
```

##### FINALIZANDO...

Ahora *lionsden*, puede procesar ese menaje y decidr si contestarle o esperar
más mensajes...
