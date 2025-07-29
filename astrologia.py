"""
Este módulo fornece utilitários para gerar um mapa astral completo usando a
biblioteca flatlib. Foi ajustado para:

  • Definir corretamente o caminho das efemérides do Swiss Ephemeris, usando
    uma abordagem robusta que considera o diretório deste próprio arquivo.
  • Configurar as variáveis de ambiente `SE_EPHE_PATH` e `FLATLIB_EPHE_PATH`
    antes de importar quaisquer componentes do flatlib para garantir que a
    Swiss Ephemeris encontre seus arquivos `.se1`.
  • Calcular a casa astrológica de cada corpo celeste usando
    `chart.houses.getObjectHouse()` (quando disponível), atribuindo casa 0
    apenas aos objetos que realmente não ocupam uma casa (por exemplo,
    nodos e Quíron em algumas configurações).
  • Remover o Ascendente da lista de objetos calculados e tratá‑lo
    separadamente, visto que é um ângulo e não um planeta.
  • Extrair aspectos astrológicos utilizando a função `aspects.getAspects`
    para todos os corpos relevantes, filtrando apenas os aspectos principais.

Os dados retornados incluem uma lista de planetas com seus signos, graus,
minutos e casa, uma lista de aspectos, além de contagens de elementos e
modalidades para compor um balanço energético do mapa.
"""

import os
import datetime
import pytz
from geopy.geocoders import Nominatim

# ---------------------------------------------------------------------------
# Configuração do caminho das efemérides
#
# O caminho absoluto para o diretório de efemérides é calculado a partir do
# diretório onde este arquivo reside. Isso evita dependência do diretório de
# trabalho atual e garante que os arquivos `.se1` sejam encontrados em
# qualquer ambiente (por exemplo, ao rodar via Flask).
module_dir = os.path.dirname(os.path.abspath(__file__))
EPHE_PATH = os.path.join(module_dir, 'sweph', 'ephe')

# Define variáveis de ambiente para Swiss Ephemeris
os.environ['SE_EPHE_PATH'] = EPHE_PATH
os.environ['FLATLIB_EPHE_PATH'] = EPHE_PATH

# Importa swisseph e define explicitamente o caminho
try:
    import swisseph as swe
    swe.set_ephe_path(EPHE_PATH)
except Exception as e:
    print(f"[WARN astrologia.py] Não foi possível configurar swe.set_ephe_path: {e}")

print(f"[INFO astrologia.py] Caminho das efemérides definido para: {EPHE_PATH}")

# Somente agora importamos componentes do flatlib. Isso garante que o caminho
# de efemérides já esteja configurado antes de qualquer uso interno.
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const, aspects


# Removemos o bloco que redefinia EPHE_PATH a partir de os.getcwd(). O caminho
# das efemérides já é definido acima com base no diretório deste arquivo, o
# que é mais confiável para aplicações web.


# Lista de corpos astrológicos a serem considerados no mapa. O Ascendente (const.ASC)
# é tratado separadamente, pois é um ângulo. Incluímos planetas pessoais,
# geracionais, nodos e Quíron.
OBJETOS = [
    const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS,
    const.JUPITER, const.SATURN, const.URANUS, const.NEPTUNE, const.PLUTO,
    const.NORTH_NODE, const.SOUTH_NODE, const.CHIRON
]

# Aspectos principais a serem considerados na análise. Usaremos estes códigos
# para filtrar os resultados retornados por `aspects.getAspects()`.
ASPECTOS_RELEVANTES = ['CON', 'OPP', 'TRI', 'SEX', 'SQR']

def formatar_data(data):
    """Garante que a data esteja no formato DD/MM/YYYY."""
    if "/" in data:
        return data
    return f"{data[:2]}/{data[2:4]}/{data[4:]}"

def formatar_hora(hora):
    """Garante que a hora esteja no formato HH:MM."""
    if ":" in hora:
        return hora
    return f"{hora[:2]}:{hora[2:]}"

def gerar_mapa(data_nasc, hora_nasc, cidade, estado):
    """
    Gera o mapa astral completo a partir dos dados de nascimento.
    """
    try:
        print("[DEBUG astrologia] Formatando data e hora...")
        data_nasc = formatar_data(data_nasc)
        hora_nasc = formatar_hora(hora_nasc)

        print("[DEBUG astrologia] Buscando localização geográfica...")
        geolocator = Nominatim(user_agent="verba_mapa_astral")
        location = geolocator.geocode(f"{cidade}, {estado}, Brasil")
        if not location:
            raise ValueError("Localização não encontrada.")
        print(f"[DEBUG astrologia] Localização encontrada: {location.latitude}, {location.longitude}")

        print("[DEBUG astrologia] Montando datetime local e UTC...")
        data_dt = datetime.datetime.strptime(data_nasc, "%d/%m/%Y")
        hora_dt = datetime.datetime.strptime(hora_nasc, "%H:%M").time()
        
        local_tz = pytz.timezone("America/Sao_Paulo")
        dt_local = local_tz.localize(datetime.datetime.combine(data_dt, hora_dt))
        dt_utc = dt_local.astimezone(pytz.utc)

        dt = Datetime(dt_utc.strftime("%Y/%m/%d"), dt_utc.strftime("%H:%M"))
        pos = GeoPos(location.latitude, location.longitude)

        print("[DEBUG astrologia] Criando chart astral com flatlib...")
        chart = Chart(dt, pos, hsys=const.HOUSES_PLACIDUS, IDs=OBJETOS)

        # Extrai cúspides das casas diretamente do flatlib. Para cada casa 1..12,
        # usamos chart.get(const.HOUSE{i}) para obter a longitude da cúspide.
        cusps = []
        try:
            for i in range(1, 13):
                house_obj = chart.get(getattr(const, f'HOUSE{i}'))
                # house_obj.lon é uma string ou número representando a longitude em graus
                cusp_lon = float(house_obj.lon) % 360.0
                cusps.append(cusp_lon)
        except Exception as e:
            cusps = None
            print(f"[WARN astrologia] Falha ao obter cúspides das casas com flatlib: {e}")

        mapa = {
            'planetas': {}, 'aspectos': [],
            'elementos': {'Fogo': 0, 'Terra': 0, 'Ar': 0, 'Agua': 0},
            'modalidades': {'Cardinal': 0, 'Fixo': 0, 'Mutavel': 0},
            'casas': {},
            'angulos': {},
            'transitos': [],
            'stelliums': {'signos': [], 'casas': []},
            'hemisferios': {},
            'quadrantes': {}
        }

        # --- Coleta de dados dos corpos astrológicos ---
        for obj_id in OBJETOS:
            planeta = chart.get(obj_id)
            signo = planeta.sign
            # Calcula grau e minuto a partir da longitude
            try:
                lon_float = float(planeta.lon)
                grau = int(lon_float)
                minuto = int((lon_float - grau) * 60)
            except Exception as e:
                print(f"[ERRO LON] planeta={obj_id}, planeta.lon={planeta.lon!r}, tipo={type(planeta.lon)}, erro={e}")
                grau, minuto = 0, 0
            # Determina a casa astrológica manualmente usando cúspides calculadas por swisseph.
            casa = 0
            if cusps:
                try:
                    lon_pl = float(planeta.lon) % 360.0
                    # Percorre as 12 casas; cusps é uma lista indexada de 0 a 11 para casas 1 a 12
                    for i in range(1, 13):
                        start = cusps[i - 1]
                        end = cusps[i] if i < 12 else cusps[0] + 360
                        # Ajusta wrap se necessário
                        if start > end:
                            end += 360
                        # Ajusta longitude do planeta para comparar no mesmo ciclo
                        lon_adj = lon_pl if lon_pl >= start else lon_pl + 360
                        if start <= lon_adj < end:
                            casa = i
                            break
                except Exception as e:
                    print(f"[WARN casa] Falha ao determinar casa para {obj_id}: {e}")
            # Fallback: se não foi possível determinar a casa, mantém 0
            mapa['planetas'][obj_id] = {
                'signo': signo,
                'grau': grau,
                'minuto': minuto,
                'casa': casa
            }
            # Contagem de elementos
            if signo in ['Aries', 'Leo', 'Sagittarius']:
                mapa['elementos']['Fogo'] += 1
            elif signo in ['Taurus', 'Virgo', 'Capricorn']:
                mapa['elementos']['Terra'] += 1
            elif signo in ['Gemini', 'Libra', 'Aquarius']:
                mapa['elementos']['Ar'] += 1
            elif signo in ['Cancer', 'Scorpio', 'Pisces']:
                mapa['elementos']['Agua'] += 1
            # Contagem de modalidades
            if signo in ['Aries', 'Cancer', 'Libra', 'Capricorn']:
                mapa['modalidades']['Cardinal'] += 1
            elif signo in ['Taurus', 'Leo', 'Scorpio', 'Aquarius']:
                mapa['modalidades']['Fixo'] += 1
            elif signo in ['Gemini', 'Virgo', 'Sagittarius', 'Pisces']:
                mapa['modalidades']['Mutavel'] += 1

        # Adiciona o Ascendente manualmente (Casa 1)
        try:
            asc = chart.get(const.ASC)
            mapa['planetas']['Asc'] = {
                'signo': asc.sign,
                'grau': int(float(asc.lon)),
                'minuto': int((float(asc.lon) - int(float(asc.lon))) * 60),
                'casa': 1
            }
        except Exception:
            asc = None
            pass

        # --- Calcula signos nas cúspides das casas ---
        if cusps:
            for i in range(1, 13):
                try:
                    house_obj = chart.get(getattr(const, f'HOUSE{i}'))
                    sign = house_obj.sign
                    # signlon indica graus dentro do signo (0-30)
                    signlon = float(house_obj.signlon)
                    mapa['casas'][i] = {
                        'signo': sign,
                        'grau': int(signlon)
                    }
                except Exception:
                    pass

        # --- Calcula ângulos cardeais (Asc, Desc, MC, IC) ---
        # Utilizamos a lista de signos para determinar o signo pelos graus
        SIGNS_EN = [
            'Aries','Taurus','Gemini','Cancer','Leo','Virgo',
            'Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'
        ]
        # Função para determinar a casa a partir de uma longitude e cusps
        def _get_house_from_lon(lon_val, cusps_list):
            if not cusps_list:
                return 0
            for idx in range(1, 13):
                start = cusps_list[idx - 1]
                end = cusps_list[idx % 12] if idx < 12 else cusps_list[0] + 360
                # Ajuste wrap
                if start > end:
                    end += 360
                lon_adj = lon_val if lon_val >= start else lon_val + 360
                if start <= lon_adj < end:
                    return idx
            return 0

        # Ascendente já adicionado acima
        try:
            if asc:
                asc_sign = asc.sign
                asc_deg = int(float(asc.lon))
                mapa['angulos']['Asc'] = {
                    'signo': asc_sign,
                    'grau': asc_deg,
                    'casa': 1
                }
                # Descendente está a 180 graus do Asc
                desc_lon = (float(asc.lon) + 180.0) % 360.0
                desc_sign = SIGNS_EN[int(desc_lon // 30)]
                desc_house = _get_house_from_lon(desc_lon, cusps)
                mapa['angulos']['Desc'] = {
                    'signo': desc_sign,
                    'grau': int(desc_lon),
                    'casa': desc_house
                }
                # Meio do Céu (MC)
                mc = chart.get(const.MC)
                mc_lon = float(mc.lon) % 360.0
                mc_sign = mc.sign
                mc_house = _get_house_from_lon(mc_lon, cusps)
                mapa['angulos']['MC'] = {
                    'signo': mc_sign,
                    'grau': int(mc_lon),
                    'casa': mc_house
                }
                # Fundo do Céu (IC) é oposto ao MC
                ic_lon = (mc_lon + 180.0) % 360.0
                ic_sign = SIGNS_EN[int(ic_lon // 30)]
                ic_house = _get_house_from_lon(ic_lon, cusps)
                mapa['angulos']['IC'] = {
                    'signo': ic_sign,
                    'grau': int(ic_lon),
                    'casa': ic_house
                }
        except Exception as e:
            print(f"[WARN angulos] Falha ao calcular ângulos cardeais: {e}")
        # --- Cálculo de aspectos ---
        print("[DEBUG astrologia] Calculando aspectos entre objetos...")
        # Definições de ângulos e orbes para aspectos principais
        ASPECTS_DEF = {
            'CON': (0.0, 8.0),   # conjunção
            'OPP': (180.0, 8.0), # oposição
            'TRI': (120.0, 7.0), # trígono
            'SEX': (60.0, 6.0),  # sextil
            'SQR': (90.0, 7.0)   # quadratura
        }
        # Calcula aspectos manualmente entre todos os pares de corpos
        for i in range(len(OBJETOS)):
            for j in range(i + 1, len(OBJETOS)):
                p1 = chart.get(OBJETOS[i])
                p2 = chart.get(OBJETOS[j])
                try:
                    lon1 = float(p1.lon) % 360.0
                    lon2 = float(p2.lon) % 360.0
                except Exception as e:
                    print(f"[ERRO ASPECTO] Falha ao obter longitude de {OBJETOS[i]} ou {OBJETOS[j]}: {e}")
                    continue
                # diferença absoluta
                diff = abs(lon1 - lon2)
                # reduz para intervalo [0,180]
                if diff > 180.0:
                    diff = 360.0 - diff
                # verifica cada tipo de aspecto
                for code, (angle, orb) in ASPECTS_DEF.items():
                    if abs(diff - angle) <= orb:
                        mapa['aspectos'].append({
                            'planeta1': OBJETOS[i],
                            'planeta2': OBJETOS[j],
                            'aspecto': code
                        })
                        break

        print("[DEBUG astrologia] Mapa astral final gerado com sucesso.")
        return mapa

    except Exception as e:
        print(f"[ERRO ao gerar mapa] {repr(e)}")
        return None