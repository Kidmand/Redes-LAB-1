# Punto estrella

## ¿Como funcionan los nombres de dominio con caracteres no ASCII ?

## Desarrolló:

Según lo que investigue los sistemas de **DNS** solo admitían caracteres **ASCII estándar**, pero luego se desarrollaron mecanismos de **encoding** para permitir caracteres que sean **no ASCII**.

El principal mecanismo que permite los nombres de dominio con caracteres no ASCII es el **encoding** a través de **Punycode**. **Punycode** es un estándar que convierte caracteres **no ASCII** en una secuencia de caracteres ASCII que comienza con el prefijo `xn--`.

Ejemplos de **encoding** usando **Punycode**:

- `中文.tw` se convierte en `xn--fiq228c.tw` .
- `💩.la` se convierte en `xn--ls8h.la` .

## ¿Como funciona?

Cuando un navegador o cualquier otro cliente web encuentra un nombre de dominio que contiene caracteres no ASCII, realiza la conversión a **Punycode** antes de enviar la consulta al **DNS**. Después de resolver la consulta DNS y obtener la dirección IP del servidor correspondiente, el navegador termina su consulta.



### Obs: Con  SSL/TLS el programador no se encarga de buscar la ip
No especificamos la dirección IP en la llamada a connection.connect() porque cuando utilizamos SSL/TLS para establecer una conexión segura, el proceso de negociación SSL/TLS se encarga de manejar la comunicación con el servidor utilizando el nombre de dominio proporcionado (`server_name`). 
Luego, el sistema operativo se encarga de resolver este nombre de dominio a la dirección IP correspondiente utilizando DNS.

#### SSL/TLS y la negociación de certificados: 
Cuando se establece una conexión SSL/TLS, uno de los pasos importantes es la negociación de certificados. Durante este proceso, el servidor presenta su certificado SSL/TLS al cliente para autenticarse. El cliente, a su vez, verifica la autenticidad del certificado del servidor para asegurarse de que está comunicándose con el servidor correcto.

Parte de la validación del certificado implica verificar que el nombre de dominio en el certificado coincida con el nombre de dominio al que se está intentando conectar el cliente. Esto es importante para prevenir ataques de hombre en el medio y garantizar que el cliente se esté comunicando con el servidor esperado.


### Los cambios que hice para que ande con https fueron los siguientes:


```python

import ssl  

PREFIX = "https://"  # Cambiado a https      Si quuiero usar https cambio la variable Prefix. 
HTTP_PORT = 443   # Cambiado a puerto HTTPS estándar

``` 

### Los otros cambios los hice en la función server_connect() agregando las lineas siguientes. 

```python 

if PREFIX == "https://":
        ssl_socket = ssl.wrap_socket(mi_socket, ssl_version=ssl.PROTOCOL_TLS)
        ssl_socket.connect((ip_address, HTTP_PORT))
        return ssl_socket
    else:
        mi_socket.connect((ip_address, HTTP_PORT))
        return mi_socket


``` 

### Esas lineas de codigos están después de la conexión del servidor http. 
### Basicamente me fijo en el PREFIX si es http o https. 