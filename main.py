from flask import Flask, jsonify, request
import random

app = Flask(__name__)
peliculas = [
    {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
    {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'},
    {'id': 3, 'titulo': 'Interstellar', 'genero': 'Ciencia ficción'},
    {'id': 4, 'titulo': 'Jurassic Park', 'genero': 'Aventura'},
    {'id': 5, 'titulo': 'The Avengers', 'genero': 'Acción'},
    {'id': 6, 'titulo': 'Back to the Future', 'genero': 'Ciencia ficción'},
    {'id': 7, 'titulo': 'The Lord of the Rings', 'genero': 'Fantasía'},
    {'id': 8, 'titulo': 'The Dark Knight', 'genero': 'Acción'},
    {'id': 9, 'titulo': 'Inception', 'genero': 'Ciencia ficción'},
    {'id': 10, 'titulo': 'The Shawshank Redemption', 'genero': 'Drama'},
    {'id': 11, 'titulo': 'Pulp Fiction', 'genero': 'Crimen'},
    {'id': 12, 'titulo': 'Fight Club', 'genero': 'Drama'}
]

"""
Codigos de estado HTTP:
- 200: 
- 201:
- 204:
- 404:
"""

def obtener_peliculas():
    return jsonify(peliculas)


def obtener_pelicula(id):
    # Lógica para buscar la película por su ID y devolver sus detalles
    for p in peliculas:
        if p['id'] == id:
            return jsonify(p), 200
    return jsonify({'mensaje': 'Película no encontrada por el ID.'}), 404


def agregar_pelicula():
    nueva_pelicula = {
        'id': obtener_nuevo_id(),
        'titulo': request.json['titulo'],
        'genero': request.json['genero']
    }
    peliculas.append(nueva_pelicula)
    print(peliculas)
    return jsonify(nueva_pelicula), 201


def actualizar_pelicula(id):
    # Lógica para buscar la película por su ID y actualizar sus detalles
    for i in range(len(peliculas)):
        if peliculas[i]['id'] == id:
            peliculas[i]['titulo'] = request.json['titulo']
            peliculas[i]['genero'] = request.json['genero']
            return jsonify(peliculas[i]), 200
    return jsonify({'mensaje': 'Película no encontrada por el ID para actualizarla.'}), 404


def eliminar_pelicula(id):
    # Lógica para buscar la película por su ID y eliminarla
    for p in peliculas:
        if p['id'] == id:
            del p
            return jsonify({'mensaje': 'Película eliminada correctamente'}), 200
    return jsonify({'mensaje': 'Película no encontrada por el ID para eliminarla.'}), 404


def obtener_peliculas_por_genero(genero):
    # Lógica para devolver el listado de películas de un género específico
    peliculas_genero = []
    for p in peliculas:
        if p['genero'] == genero:
            peliculas_genero.append(p)
    if peliculas_genero:
        return jsonify(peliculas_genero), 200
    else:
        return jsonify({'mensaje': 'No hay peliculas de ese genero.'}), 404


def obtener_peliculas_entitulo(texto):
    # Lógica para devolver el listado de películas que tengan determinado string en el título.
    peliculas_str = []
    for p in peliculas:
        if texto in p['titulo']:
            peliculas_str.append(p)
    if peliculas_str:
        return jsonify(peliculas_str), 200
    else:
        return jsonify({'mensaje': 'El texto "'+texto+'" no se encontro en ningun titulo.'}), 404


def random_pelicula():
    # Lógica para devolver/sugerir una película aleatoria.
    if len(peliculas) == 0:
        return jsonify({'mensaje': 'No hay peliculas.'}), 404
    return jsonify(random.choice(peliculas)), 200


def pelicula_random_por_genero(genero):
    # Lógica para devolver/sugerir una película aleatoria según género.
    peliculas_genero = []
    for p in peliculas:
        if p['genero'] == genero:
            peliculas_genero.append(p)
    if peliculas_genero:
        return jsonify(random.choice(peliculas_genero)), 200
    else:
        return jsonify({'mensaje': 'No hay peliculas de ese genero.'}), 404
        


def obtener_nuevo_id():
    if len(peliculas) > 0:
        ultimo_id = peliculas[-1]['id']
        return ultimo_id + 1
    else:
        return 1


app.add_url_rule('/peliculas',
                 'obtener_peliculas',
                 obtener_peliculas, 
                 methods=['GET'])

app.add_url_rule('/peliculas/<int:id>',
                 'obtener_pelicula',
                 obtener_pelicula, 
                 methods=['GET'])

app.add_url_rule('/peliculas',
                 'agregar_pelicula',
                 agregar_pelicula,
                 methods=['POST'])

app.add_url_rule('/peliculas/<int:id>',
                 'actualizar_pelicula',
                 actualizar_pelicula, 
                 methods=['PUT'])

app.add_url_rule('/peliculas/<int:id>', 
                 'eliminar_pelicula',
                 eliminar_pelicula, 
                 methods=['DELETE'])

app.add_url_rule('/peliculas/genero/<string:genero>',
                 'obtener_peliculas_por_genero',
                 obtener_peliculas_por_genero,
                 methods=['GET'])

app.add_url_rule('/peliculas/entitulo/<string:texto>',
                 'obtener_peliculas_entitulo',
                 obtener_peliculas_entitulo,
                 methods=['GET'])

app.add_url_rule('/peliculas/random',
                 'random_pelicula',
                 random_pelicula,
                 methods=['GET'])

app.add_url_rule('/peliculas/random/<string:genero>',
                 'pelicula_random_por_genero',
                 pelicula_random_por_genero,
                 methods=['GET'])

if __name__ == '__main__':
    app.run()
