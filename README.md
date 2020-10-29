# NIGHTLY TRANSFER.

Nightly Transfer (abreviado NTransfer), es una utilidad que permite la 
transmisión de datos entre dos dispositivos de forma fácil y rápida.

## COMENZANDO.

Para comenzar debe tener [instalado](./INSTALL.md) NTransfer en su 
dispositivo...

Le recomendamos abrir **dos** sesiones de terminal para comenzar; para 
facilitar la explicación llamaremos a la primera terminal `houseland` y a la
segunda `lionsden`.

En `houseland` ejecute NTransfer, le aparecerá una pantalla similar a esta:

```
Introduzca la dirección con el formato:
    i.p:port
Si tiene guardados atajos, escribalos con el formato:
    #atajo

Introduzca su dirección: 
```

Podrá ver que puede escribir direcciones al azar, porque no prueba con
`localhost:8080`. Después verá lo siguiente:

```
¿Desea ser un servidor? ([y] Sí | [n] No):
```

A lo que responderemos sí, es decir, presionando `y`.

Veremos que nuestra terminal se congela, pero en realidad está esperando una
conexión entrante.

Ahora iniciemos NTransfer en `lionsden`, responderemos con la misma dirección 
que escribimos en el servidor y despues presionaremos `n`.

Veremos lo siguiente en las dos terminales:

```
(NTP) 
```

Prueba escribir `Soy Houseland` y `Soy Lionsden`, en las terminales 
`houseland` y `lionsden` respectivamente.

¡Genial! podemos enviar mensajes; ¿Por qué no pruebas enviar un archivo?

Escribe `#file /ruta/a/algun.archivo` en `lionsden` y presiona `ENTER` en
`houseland`, `houseland` te pedira una ruta, escribe `./archivo_de_prueba`
y mira tu directorio de trabajo actual...

Si eres curioso, te habras dado cuenta de que en el mensaje habla acerca de 
los atajos:

```
Si tiene guardados atajos, escribalos con el formato:
    #atajo
```

Puedes escribirlos en lugar de usar la dirección completa, NTransfer viene 
con dos atajos: `#localhost` y `#public`, que corresponden a las direcciones
`localhost:22314` y `10.1.10.1:22314`.

### MENÚ.

La siguiente es una lista de enlaces a diferentes archivos del proyecto.

 - [Créditos.](./AUTHORS.md)
 - [Agradecimientos.](./THANKS.md)
 - [Registro de cambios detallado (para desarrolladores).](./CHANGELOG.md)
 - [Registro de cambios básico (para usuarios).](./NEWS.md)
 - [Instrucciones de instalación.](./INSTALL.md)
 - [Licencia (Aurora License 0.1).](./LICENSE.txt)
 - [Errores conocidos y la manera de informarlos.](./BUGS.md)
 - [Preguntas frecuentes.](./FAQ.md)
 - [Futuras funcionalidades.](./TODO.md)
 - [¿Cómo contribuir al proyecto?](./CONTRIBUTING.md)

#### AGRADECIMIENTOS.

***Gracias a todos los que prueban, desarrollan y utilizan Nightly.***