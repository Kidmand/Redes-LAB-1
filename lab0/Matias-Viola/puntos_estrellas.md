# Punto estrella 1 Lab 0

## Encoding

El encoding se refiere específicamente a la representación de caracteres de texto mediante códigos numéricos.

## Encabezados 💩

Los encabezados de las páginas web que contienen caracteres no ASCII, como `http://中文.tw/` o `https://💩.la1` no son compatibles con el sistema DNS (Domain Name System) por lo que directamente no se pueden traducir en direcciones IP numéricas, que son las que entienden las computadoras para localizar recursos en la red...

No funciona de forma directa pero aun asi es posible.
Esto es gracias al proceso de encoding estándar Punycod que los convierte en una forma compatible con el sistema DNS y al sistema IDN (Internationalized Domain Names) que se encarga de interpretar estos nombres de dominio para que se puedan ver como fueron escritos inicialmente.

Esto no solo permite nombres de dominio con 💩 en el nombre, ademas hace que las direcciones de Internet sean más accesibles y amigables para usuarios de diferentes idiomas y culturas pudiendo traducirlo a su alfabeto.

# Punto estrella 2 Lab 0

## Una pregunta y una observacion
### Por que HTTP en HTTPS?
Si ejecutan por la terminal el comando `python3 hget-https.py https://es.wikipedia.org/wiki/Wikipedia:Portada` por ejemplo, les saldra una pregunta implementada por mi como la de abajo:
```bash
----------------------------------------------Pregunta----------------------------------------------
Por que al ejecutar la linea aprox 196 'header = read_line(connection)' me devuelve HTTP en vez de HTTPS en el header? 
connection = <ssl.SSLSocket fd=3, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('192.168.0.191', 41030), raddr=('208.80.153.224', 443)> 
header = b'HTTP/1.1 200 OK\r\n'
----------------------------------------------------------------------------------------------------
```
No encontre respuesta, yo esperaba algo como `header = b'HTTPS/1.1 200 OK\r\n'` en vez de `header = b'HTTP/1.1 200 OK\r\n'`. 

### Obs: Con  SSL/TLS el programador no se encarga de buscar la ip
No especificamos la dirección IP en la llamada a connection.connect() porque cuando utilizamos SSL/TLS para establecer una conexión segura, el proceso de negociación SSL/TLS se encarga de manejar la comunicación con el servidor utilizando el nombre de dominio proporcionado (`server_name`). 
Luego, el sistema operativo se encarga de resolver este nombre de dominio a la dirección IP correspondiente utilizando DNS.

#### SSL/TLS y la negociación de certificados: 
Cuando se establece una conexión SSL/TLS, uno de los pasos importantes es la negociación de certificados. Durante este proceso, el servidor presenta su certificado SSL/TLS al cliente para autenticarse. El cliente, a su vez, verifica la autenticidad del certificado del servidor para asegurarse de que está comunicándose con el servidor correcto.

Parte de la validación del certificado implica verificar que el nombre de dominio en el certificado coincida con el nombre de dominio al que se está intentando conectar el cliente. Esto es importante para prevenir ataques de hombre en el medio y garantizar que el cliente se esté comunicando con el servidor esperado.

## Vista de principales cambios para la implementacion:
### hget-https.py (https)
```python
import ssl
import sys
import socket
import optparse

PREFIX = "https://"
HTTPS_PORT = 443   # 443 para HTTPS
HTTPS_OK = "200"  # El codigo esperado para respuesta exitosa.

```
```python
def connect_to_server(server_name):
    try:
        # Creamos un contexto SSL/TLS
        SSLContext = ssl.create_default_context()
        # Creamos un socket SSL/TLS
        connection = SSLContext.wrap_socket(socket.socket(socket.AF_INET),server_hostname=server_name)
    except ssl.SSLError as e:
        sys.stderr.write("Error creando el socket SSL/TLS: {}\n".format(e))
        raise e
    except socket.error as e:
        sys.stderr.write("Error creando el socket: {}\n".format(e))
        raise e

    try:
        # Nos conectamos al puerto HTTPS del servidor
        connection.connect((server_name, HTTPS_PORT)) # SSL no requiere ip
    except ConnectionRefusedError as e:
        sys.stderr.write("El servidor con {}:{} rechazo la conexion: {}\n".format(server_name, HTTPS_PORT, e))
        raise e
    except socket.error as e:
        sys.stderr.write("No se pudo conectar al servidor: {}\n".format(e))
        raise e
    
    return connection
```
### hget.py (http)
```python
import sys
import socket
import optparse

PREFIX = "http://"
HTTP_PORT = 80   # 80 es el puerto por convencion para HTTP
# según http://tools.ietf.org/html/rfc1700
HTTP_OK = "200"  # El codigo esperado para respuesta exitosa.
```
``` python
def connect_to_server(server_name):
    try:
        # Obtenemos la dirección IP del servidor y la asignamos a ip_address
        ip_address = socket.gethostbyname(server_name)
    except socket.gaierror as e:
        sys.stderr.write("Error obteniendo la direccion IP: {}\n".format(e))
        raise e

    sys.stderr.write("Contactando al servidor en %s...\n" % ip_address)

    try:
        # Creamos el socket
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        sys.stderr.write("Error creando el socket: {}\n".format(e))
        raise e
    try:
        # Nos conectamos al puerto correcto del servidor
        connection.connect((ip_address, HTTP_PORT))
    except ConnectionRefusedError as e:
        sys.stderr.write("El servidor en {ip_address}:{HTTP_PORT} rechazo la conexion: {}\n".format(e))
        raise e
    except socket.error as e:
        sys.stderr.write("No se pudo conectar al servidor: {}\n".format(e))
        raise e
    
    return connection
```
