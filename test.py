import requests
import proximo_feriado as pf

# Obtener todas las películas
response = requests.get('http://localhost:5000/peliculas')
peliculas = response.json()
print("Películas existentes:")
for pelicula in peliculas:
    print(
        f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
print()

# Agregar una nueva película
nueva_pelicula = {
    'titulo': 'Pelicula de prueba',
    'genero': 'Acción'
}
response = requests.post(
    'http://localhost:5000/peliculas', json=nueva_pelicula)
if response.status_code == 201:
    pelicula_agregada = response.json()
    print("Película agregada:")
    print(
        f"ID: {pelicula_agregada['id']}, Título: {pelicula_agregada['titulo']}, Género: {pelicula_agregada['genero']}")
else:
    print("Error al agregar la película.")
print()

# Obtener detalles de una película específica
id_pelicula = 1  # ID de la película a obtener
response = requests.get(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 200:
    pelicula = response.json()
    print("Detalles de la película:")
    print(
        f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
else:
    print("Error al obtener los detalles de la película.")
print()

# Actualizar los detalles de una película
id_pelicula = 1  # ID de la película a actualizar
datos_actualizados = {
    'titulo': 'Nuevo título',
    'genero': 'Comedia'
}
response = requests.put(
    f'http://localhost:5000/peliculas/{id_pelicula}', json=datos_actualizados)
if response.status_code == 200:
    pelicula_actualizada = response.json()
    print("Película actualizada:")
    print(
        f"ID: {pelicula_actualizada['id']}, Título: {pelicula_actualizada['titulo']}, Género: {pelicula_actualizada['genero']}")
else:
    print("Error al actualizar la película.")
print()

# Eliminar una película
id_pelicula = 1  # ID de la película a eliminar
response = requests.delete(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 200:
    print("Película eliminada correctamente.")
else:
    print("Error al eliminar la película.")
print()

# Obtener todas las películas de "genero"
genero = "Ciencia ficción"
response = requests.get(f'http://localhost:5000/peliculas/genero/{genero}')
if response.status_code == 200:
    peliculas = response.json()
    print("Películas del genero {} existentes:".format(genero))
    for pelicula in peliculas:
        print(
            f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
elif response.status_code == 404:
    print(response.json()["mensaje"])
else:
    print("Error al obtener todas las peliculas de un genero.")
print()

# Obtener peliculas por contenido en el titulo
texto_a_buscar = "The"
response = requests.get(
    f'http://localhost:5000/peliculas/entitulo/{texto_a_buscar}')
if response.status_code == 200:
    peliculas = response.json()
    print("Películas con ({}) en el titulo existentes:".format(texto_a_buscar))
    for pelicula in peliculas:
        print(
            f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
elif response.status_code == 404:
    print(response.json()["mensaje"])
else:
    print("Error al obtener peliculas por contenido en el titulo.")
print()

# Obtener una pelicular random.
response = requests.get(f'http://localhost:5000/peliculas/random')
if response.status_code == 200:
    pelicula_random = response.json()
    print("Película random:")
    print(
        f"ID: {pelicula_random['id']}, Título: {pelicula_random['titulo']}, Género: {pelicula_random['genero']}")
elif response.status_code == 404:
    print(response.json()["mensaje"])
else:
    print("Error al obtener pelicula random.")
print()

# Obtener una pelicular random por genero.
genero = "Ciencia ficción"
response = requests.get(f'http://localhost:5000/peliculas/random/{genero}')
if response.status_code == 200:
    pelicula_random = response.json()
    print("Película random por genero:")
    print(
        f"ID: {pelicula_random['id']}, Título: {pelicula_random['titulo']}, Género: {pelicula_random['genero']}")
elif response.status_code == 404:
    print(response.json()["mensaje"])
else:
    print("Error al obtener pelicula random por genero.")
print()


# Obtener una película aleatoria de "genero" para el proximo feriado.
genero = "Ciencia ficción"
response = requests.get(
    f'http://localhost:5000/peliculas/proximoferiado/{genero}')
if response.status_code == 200:
    pelicula_random = response.json()
    print(
        f"Película random de {genero} para el proximo feriado:".format(genero))
    print(f"Película: {pelicula_random['pelicula']['titulo']}")
    print(f"Género: {pelicula_random['pelicula']['genero']}")
    print(f"Próximo feriado: {pelicula_random['proximo_feriado']['motivo']}")
    print(
        f"Fecha del próximo feriado: {pelicula_random['proximo_feriado']['dia']}/{pelicula_random['proximo_feriado']['mes']}")
    print(
        f"Info sobre el próximo feriado: {pelicula_random['proximo_feriado']['info']}")
elif response.status_code == 404:
    print(response.json()["mensaje"])
else:
    print("Error al obtener pelicula random por genero para el proximo feriado..")
print()
