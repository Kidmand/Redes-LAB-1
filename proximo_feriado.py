import requests
from datetime import date


def get_url(year):
    """ Devuelve la URL correspondiente a la API para obtener los feriados del año 'year'. """
    return f"https://nolaborables.com.ar/api/v2/feriados/{year}"


months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
          'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
days = ['Lunes', 'Martes', 'Miércoles',
        'Jueves', 'Viernes', 'Sábado', 'Domingo']


def day_of_week(day, month, year):
    """ Devuelve el día de la semana correspondiente a la fecha 'day'/'month'/'year'."""
    return days[date(year, month, day).weekday()]


class NextHoliday:
    def __init__(self):
        self.loading = True
        self.year = date.today().year
        self.holiday = None

    def set_next(self, holidays):
        """ Establece el próximo feriado."""
        now = date.today()
        today = {
            'day': now.day,
            'month': now.month
        }

        holiday = next(
            (h for h in holidays if h['mes'] == today['month']
             and h['dia'] > today['day'] or h['mes'] > today['month']),
            holidays[0]
        )

        self.holiday = holiday

    def fetch_holidays(self):
        """ Realiza la solicitud HTTP a la API para obtener los feriados del año actual."""
        self.loading = True
        response = requests.get(get_url(self.year))
        data = response.json()
        self.set_next(data)
        self.loading = False

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

    # ----------------------------------------------------------------
    def proximo_feriado_del_tipo(self, type):
        """ Devuelve el próximo feriado 'tipo'."""
        return self.holiday[type]

    def fetch_holidays_del_tipo(self, type):
        """ Realiza la solicitud HTTP a la API para obtener los feriados 'tipo' del año actual."""
        self.loading = True
        response = requests.get(get_url(self.year))
        data = response.json()
        self.set_next_tipo(data, type)
        self.loading = False

    def set_next_tipo(self, holidays, type):
        """ Establece el próximo feriado 'tipo'."""
        now = date.today()
        today = {
            'day': now.day,
            'month': now.month
        }

        holiday = next(
            (h for h in holidays if h['tipo'] == type and h['mes'] == today['month']
             and h['dia'] > today['day'] or h['mes'] > today['month']),
            holidays[0]
        )

        self.loading = False
        self.holiday = holiday


next_holiday = NextHoliday()
next_holiday.fetch_holidays()
next_holiday.render()

# next_holiday_del_tipo = NextHoliday()
next_holiday.fetch_holidays_del_tipo('puente')
next_holiday.render()
