from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from geopy.geocoders import Nominatim
from datetime import datetime

def gerar_mapa(data_nasc, hora_nasc, cidade, estado):
    try:
        geolocator = Nominatim(user_agent="mapa_astral_verba")
        location = geolocator.geocode(f"{cidade}, {estado}, Brasil")
        if not location:
            return None

        dt = Datetime(
            data_nasc,
            hora_nasc,
            'America/Sao_Paulo'
        )
        pos = GeoPos(str(location.latitude), str(location.longitude))
        chart = Chart(dt, pos)

        mapa = {}
        for obj in ['SUN', 'MOON', 'ASC', 'MER', 'VEN', 'MAR', 'JUP', 'SAT']:
            planeta = chart.get(obj)
            mapa[obj] = f"{planeta.sign} ({int(planeta.lon)}°)"

        return mapa
    except Exception as e:
        print("Erro:", e)
        return None