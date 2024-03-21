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
