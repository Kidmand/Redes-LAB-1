import requests
import pytest
import requests_mock
import proximo_feriado as pf

BASE_URL_API = 'http://localhost:5000/peliculas'


@pytest.fixture
def mock_response():
    with requests_mock.Mocker() as m:
        # Simulamos la respuesta para obtener todas las películas
        m.get('http://localhost:5000/peliculas', json=[
            {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
            {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'}
        ])

        # Simulamos la respuesta para agregar una nueva película
        m.post('http://localhost:5000/peliculas', status_code=201,
               json={'id': 3, 'titulo': 'Pelicula de prueba', 'genero': 'Acción'})

        # Simulamos la respuesta para obtener detalles de una película específica
        m.get('http://localhost:5000/peliculas/1',
              json={'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'})

        # Simulamos la respuesta para actualizar los detalles de una película
        m.put('http://localhost:5000/peliculas/1', status_code=200,
              json={'id': 1, 'titulo': 'Nuevo título', 'genero': 'Comedia'})

        # Simulamos la respuesta para eliminar una película
        m.delete('http://localhost:5000/peliculas/1', status_code=200)

        yield m

# Las pruebas con el sufijo "WHIH_MOCK" son las que utilizan el mock.


def test_obtener_peliculas_WHIH_MOCK(mock_response):
    response = requests.get(BASE_URL_API)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_agregar_pelicula_WHIH_MOCK(mock_response):
    nueva_pelicula = {'titulo': 'Pelicula de prueba', 'genero': 'Acción'}
    response = requests.post(BASE_URL_API, json=nueva_pelicula)
    assert response.status_code == 201
    assert response.json()['id'] == 3


def test_obtener_detalle_pelicula_WHIH_MOCK(mock_response):
    response = requests.get(BASE_URL_API + '/1')
    assert response.status_code == 200
    assert response.json()['titulo'] == 'Indiana Jones'


def test_actualizar_detalle_pelicula_WHIH_MOCK(mock_response):
    datos_actualizados = {'titulo': 'Nuevo título', 'genero': 'Comedia'}
    response = requests.put(BASE_URL_API + '/1', json=datos_actualizados)
    assert response.status_code == 200
    assert response.json()['titulo'] == 'Nuevo título'


def test_eliminar_pelicula_WHIH_MOCK(mock_response):
    response = requests.delete(BASE_URL_API + '/1')
    assert response.status_code == 200


# PRUEBAS SIN MOCK, asegurarse de tener el servidor corriendo (python3 main.py).

def test_obtener_peliculas():
    response = requests.get(BASE_URL_API)
    assert response.status_code == 200


def test_agregar_y_eliminar_pelicula():
    nueva_pelicula = {'titulo': 'Pelicula de prueba', 'genero': 'Acción'}
    response = requests.post(BASE_URL_API, json=nueva_pelicula)
    assert response.status_code == 201
    assert response.json()['titulo'] == nueva_pelicula['titulo']
    assert response.json()['genero'] == nueva_pelicula['genero']


def test_eliminar_pelicula():
    response = requests.delete(BASE_URL_API + '/10')
    assert response.status_code == 200

    # TESTS QUE VALIDAN INFORMACION NO VALIDA.
    # Ejecutar este test en el entorno local que
    # sabemos que no existe una pelicula con id=50000.
    response = requests.delete(BASE_URL_API + '/50000')
    assert response.status_code == 404
    response = requests.delete(BASE_URL_API + '/-1')
    assert response.status_code == 404


def test_obtener_detalle_pelicula():
    response = requests.get(BASE_URL_API + '/1')
    assert response.status_code == 200

    # TESTS QUE VALIDAN INFORMACION NO VALIDA.
    # Ejecutar este test en el entorno local que
    # sabemos que no existe una pelicula con id=50000.
    response = requests.get(BASE_URL_API + '/50000')
    assert response.status_code == 404
    response = requests.get(BASE_URL_API + '/-1')
    assert response.status_code == 404


def test_actualizar_detalle_pelicula():
    datos_actualizados = {'titulo': 'Nuevo título', 'genero': 'Comedia'}
    response = requests.put(BASE_URL_API + '/1', json=datos_actualizados)
    assert response.status_code == 200
    assert response.json()['titulo'] == datos_actualizados['titulo']
    assert response.json()['genero'] == datos_actualizados['genero']
    assert response.json()['id'] == 1

    # TESTS QUE VALIDAN INFORMACION NO VALIDA.
    # Ejecutar este test en el entorno local que
    # sabemos que no existe una pelicula con id=50000.
    datos_actualizados = {'titulo': 'Nuevo título', 'genero': 'Comedia'}
    response = requests.put(BASE_URL_API + '/50000', json=datos_actualizados)
    assert response.status_code == 404
    response = requests.put(BASE_URL_API + '/-1', json=datos_actualizados)
    assert response.status_code == 404


def test_obtener_peliculas_por_genero():
    genero = "Aventura"
    response = requests.get(BASE_URL_API + '/genero/' + genero)
    assert response.status_code == 200
    assert len(response.json()) == 1

    # TESTS QUE VALIDAN INFORMACION NO VALIDA.
    # Ejecutar este test en el entorno local que
    # sabemos que no existe una pelicula con genero="genero_inexistente".
    genero = "genero_inexistente"
    response = requests.get(BASE_URL_API + '/genero/' + genero)
    assert response.status_code == 404


def test_obtener_peliculas_entitulo():
    texto = "The"
    response = requests.get(BASE_URL_API + '/entitulo/' + texto)
    assert response.status_code == 200
    assert len(response.json()) == 3

    texto_con_espacios = "The Dark"
    response = requests.get(BASE_URL_API + '/entitulo/' + texto_con_espacios)
    assert response.status_code == 200
    assert len(response.json()) == 1

    # TESTS QUE VALIDAN INFORMACION NO VALIDA.
    # Ejecutar este test en el entorno local que
    # sabemos que no existe una pelicula con texto="texto_inexistente".
    texto = "texto_inexistente"
    response = requests.get(BASE_URL_API + '/entitulo/' + texto)
    assert response.status_code == 404


def test_obtener_pelicula_random():
    response = requests.get(BASE_URL_API + '/random')
    assert response.status_code == 200
    assert response.json() is not None


def test_obtener_pelicula_random_por_genero():
    genero = "Acción"
    response = requests.get(BASE_URL_API + '/random/' + genero)
    assert response.status_code == 200
    assert response.json() is not None

    # TESTS QUE VALIDAN INFORMACION NO VALIDA.
    # Ejecutar este test en el entorno local que
    # sabemos que no existe una pelicula con genero="genero_inexistente".
    genero = "genero_inexistente"
    response = requests.get(BASE_URL_API + '/random/' + genero)
    assert response.status_code == 404


def test_obtener_pelicula_para_feriado_del_genero():
    genero = "Acción"
    response = requests.get(BASE_URL_API + '/proximoferiado/' + genero)
    assert response.status_code == 200
    assert response.json() is not None
    assert response.json()['pelicula'] is not None
    assert response.json()['proximo_feriado'] is not None

    # TESTS QUE VALIDAN INFORMACION NO VALIDA.
    # Ejecutar este test en el entorno local que
    # sabemos que no existe una pelicula con genero="genero_inexistente".
    genero = "genero_inexistente"
    response = requests.get(BASE_URL_API + '/proximoferiado/' + genero)
    assert response.status_code == 404


# TESTS PARA proximo_feriado.py

def test_obtener_proximo_feriado():
    next_holiday = pf.NextHoliday()
    next_holiday.fetch_holidays()
    response = next_holiday.get_holiday()
    assert response is not None
    assert response['motivo'] is not None
    assert response['tipo'] is not None
    assert response['dia'] is not None
    assert response['mes'] is not None
    assert response['info'] is not None
    assert response['id'] is not None


def test_obtener_proximo_feriado_tipo():
    tipos = ['inamovible', 'trasladable', 'nolaborable', 'puente']
    next_holiday = pf.NextHoliday()
    for tipo in tipos:
        next_holiday.fetch_holidays_del_tipo(tipo)
        response = next_holiday.get_holiday()
        assert response is not None
        assert response['motivo'] is not None
        assert response['tipo'] is not None
        assert response['dia'] is not None
        assert response['mes'] is not None
        assert response['info'] is not None
        assert response['id'] is not None
