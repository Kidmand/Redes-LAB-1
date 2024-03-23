import requests
from datetime import date


def get_url(year):
    """ Devuelve la URL correspondiente a la API para obtener los feriados del año 'year'. """
    return f"https://nolaborables.com.ar/api/v2/feriados/{year}"


months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
          'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
days = ['Lunes', 'Martes', 'Miércoles',
        'Jueves', 'Viernes', 'Sábado', 'Domingo']
tipos = ['inamovible', 'trasladable', 'nolaborable', 'puente']


def day_of_week(day, month, year):
    """ Devuelve el día de la semana correspondiente a la fecha 'day'/'month'/'year'."""
    return days[date(year, month, day).weekday()]


class NextHoliday:
    def __init__(self):
        self.loading = True
        self.year = date.today().year
        self.holiday = None

    def set_next(self, holidays, tipo=None):
        """ Establece el próximo feriado."""
        now = date.today()
        today = {
            'day': now.day,
            'month': now.month
        }

        if tipo:
            holiday = next(
                (h for h in holidays
                 if (h['tipo'] == tipo) and (
                     (h['mes'] == today['month'] and h['dia'] > today['day'])
                     or (h['mes'] > today['month'])
                 )),
                holidays[0]
            )
        else:
            holiday = next(
                (h for h in holidays
                 if (h['mes'] == today['month'] and h['dia'] > today['day']) or h['mes'] > today['month']),
                holidays[0]
            )

        self.holiday = holiday

    # Metodos de fetch de feriados.

    def _fetch_all_holidays_(self):  # Este método es privado.
        response = requests.get(get_url(self.year))
        return response.json()

    def fetch_holidays(self):
        """ Realiza la solicitud HTTP a la API para obtener los feriados del año actual."""
        self.loading = True
        data = self._fetch_all_holidays_()
        self.set_next(data)
        self.loading = False

    def fetch_holidays_del_tipo(self, tipo):
        """ Realiza la solicitud HTTP a la API para obtener los feriados 'tipo' del año actual."""
        self.loading = True
        data = self._fetch_all_holidays_()
        if tipo not in tipos:
            print("Tipo de feriado inválido.")
            self.holiday = data[0]
            self.loading = False
            return
        self.set_next(data, tipo)
        self.loading = False

    # Metodos de retorno de la información del próximo feriado.

    def get_holiday(self):
        """ 
        Devuelve la información del próximo feriado.
        {
            "motivo": String,
            "tipo": String,
            "info": String,
            "dia": Int,
            "mes": Int,
            "id": String
        }
        """
        if not self.loading:
            return self.holiday
        else:
            print("No se ha cargado la información de los feriados.")
            return None

    def render(self):
        """ Imprime la información sobre el próximo feriado. """
        if self.loading:
            print("Buscando...")
        else:
            print("Próximo feriado")
            print(self.holiday['motivo'])
            print("Fecha:")
            print(day_of_week(self.holiday['dia'],
                  self.holiday['mes'], self.year))
            print(self.holiday['dia'])
            print(months[self.holiday['mes'] - 1])
            print("Tipo:")
            print(self.holiday['tipo'])
