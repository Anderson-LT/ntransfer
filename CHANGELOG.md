# REGISTRO DE CAMBIOS DETALLADO (PARA DESARROLLADORES).

**Registro de cambios de Nightly Transfer.**

---

**0.0.2 (En Desarrollo)** Esta versión está en desarrollo, para utilizarla y 
probarla, deberá desacargar el último commit.

 - **config.py** Ahora se soporta el fomato PYZ.
   - El argumento *file* en las funciones *set_config* y *get_config* ahora aceptan *None* como argumento.
     - El comportamiento es el mismo.
     - Es 100 % compatible con *0.0.2 preview*.
 - Se añadió un nuevo módulo: *utils.json*.
   - Contiene una función *pause*.
     - Esta función genera una pausa en el programa hasta que el usuario presione una tecla.
     - Tiene un argumento *text*, el cual muestra un texto de ayuda al usuario.
 - **__main__.py** Cuando se genera una excepción, genera una pausa.

**0.0.2 _preview_**

 - **protocol.py** Obtener información acerca del proceso de descarga, confirmar el proceso y ofrecer un búffer 
   alternativo.
   - Se añadió un argumento *per_cent*, que llama a una función con el porcentaje actual descargado.
     - Este argumento es opcional.
   - Se añadió un argumento *confrm*, el cual llama una función con la cabecera y espera un booleano.
     - Este booleano decidirá la descarga del archivo.
     - Si el booleano es *False*, la función retornará None junto con la cabecera.
     - Este argumento es opcional.
   - Se añadió un argumnto *buffer*, que ofrece una estructura alternativa, para evitar desbordes de memoria.
     - Debe ser una función que tome como argumento un objeto *bytes*.
     - Este argumento es opcional.
 - **repl.py** Se permite escribir comandos propios en la clase *REPL*, se añadió un diccionario *CMDS* con comandos 
   básicos, la clase REPL, contiene dos métodos nuevos *progress_bar* y *confirm*.
     - Solo debes añadir un diccionario con el nombre de tu comando y su respectiva función.
     - Todo es funcional, la actualización es compatible con la vrsión 0.0.1.
 - **config.py** Solucionar los conflictos de *ntp.json* aquí y no en *__main__.py*.
 - Las pruebas de *Android*, ahora se hacen en *Termux (Python 3.9.0)*.
 - Se corrigieron los errores que seguían solicitando rutas, y el rastreo por un mensaje cuando se interrumpe la 
   conexión.

---

**0.0.1 (Actual)** Esta al ser la primera versión, se incluirán las características:

 - Compatibilidad con *Android* (Probado en *QPython 3.0.0*).
 - Compatibilidad con *Windows* (Probado en *Windows 7*).
 - Rápido envio de datos.
 - REPL incluida.
 - Uso de *Python* puro, no se necesitan ejecutar librerías escritas en otros idiomas.
 - Rápida ejecución.
 - Baja latencia.
