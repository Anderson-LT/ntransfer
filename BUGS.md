# ERRORES CONOCIDOS Y LA MANERA DE INFORMARLOS.

**Estos son los *bugs* conocidos en Nightly Transfer.**

---

Puede informar los *bugs* que encuentre en la zona *ISSUES*...

## La siguiente es una lista de todos los errores conocidos:

 - Cuando se solicita una ruta al guardar un archivo y se responde con una ruta hacia una carpeta o se responde con 
   caracteres no válidos como _*_, se prodce un error.
 - Los ajustes de colores en el archivo *ntp.json* no surten efecto.
 - Hay algunos errores que cierran la ventana de forma repentina.
 - Al tener las operaciones de registro en modo *DEBUG* y mostrar una barra de estado, se genera una excepción.

## Historial de errores (parcialmente solucionados):

 - Cuando el protocolo genera una excepción no se maneja adecuadamente.

## Historial de errores (solucionados):

 - Después de colocar una ruta (para guardar algún archivo recibido), el 
   programa sigue solicitando una ruta, se puede salir del programa 
   presionando `CTRL-D`, el archivo si se guarda.
 - Al tratar de conectar con una dirección que no tiene servidor se produce un error.

---

## **ÚLTIMA ACTUALIZACIÓN:** *Viernes, 4 de Diciembre de 2020.*
