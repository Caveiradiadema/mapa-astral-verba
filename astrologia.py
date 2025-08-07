"""
Este módulo fornece utilitários para gerar um mapa astral completo usando a
biblioteca flatlib. Foi ajustado para:

  • Definir corretamente o caminho das efemérides do Swiss Ephemeris, usando
    uma abordagem robusta que considera o diretório deste próprio arquivo.
  • Configurar as variáveis de ambiente `SE_EPHE_PATH` e `FLATLIB_EPHE_PATH`
    antes de importar quaisquer componentes do flatlib.
  • Calcular a casa astrológica de cada corpo celeste de forma confiável
    acessando a propriedade 'house' do objeto do planeta, calculada pela
    própria flatlib, eliminando a necessidade de cálculos manuais complexos.
  • Tratar o Ascendente separadamente, pois é um ângulo fundamental.
  • Extrair aspectos astrológicos principais para todos os corpos relevantes,
    garantindo que os tipos de dados sejam tratados corretamente para evitar erros.

Os dados retornados incluem uma lista de planetas com seus signos, graus,
minutos e casa, uma lista de aspectos, além de contagens de elementos e
modalidades para compor um balanço energético do mapa.
"""

import os
import datetime
import pytz
from geopy.geocoders import Nominatim

# ---------------------------------------------------------------------------
# Configuração robusta do caminho das efemérides (Swiss Ephemeris)
# ---------------------------------------------------------------------------
# O caminho é calculado a partir do diretório onde este arquivo reside,
# garantindo que funcione de forma consistente em qualquer ambiente.
try:
    module_dir = os.path.dirname(os.path.abspath(__file__))
    EPHE_PATH = os.path.join(module_dir, 'sweph', 'ephe')

    # Define as variáveis de ambiente ANTES de importar flatlib.
    os.environ['SE_EPHE_PATH'] = EPHE_PATH
    os.environ['FLATLIB_EPHE_PATH'] = EPHE_PATH

    # Importa e configura o swisseph explicitamente
    import swisseph as swe
    swe.set_ephe_path(EPHE_PATH)

    print(f"[INFO astrologia.py] Caminho das efemérides definido para: {EPHE_PATH}")

except Exception as e:
    print(f"[CRÍTICO astrologia.py] Falha ao configurar as efemérides: {e}")
    # Se as efemérides não puderem ser configuradas, o módulo não pode funcionar.
    swe = None

# Somente agora importamos flatlib, que usará as configurações acima.
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const, aspects

# ---------------------------------------------------------------------------
# Constantes e Listas
# ---------------------------------------------------------------------------
# Lista de corpos astrológicos a serem considerados no mapa.
OBJETOS = [
    const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS,
    const.JUPITER, const.SATURN, const.URANUS, const.NEPTUNE, const.PLUTO,
    const.NORTH_NODE, const.SOUTH_NODE, const.CHIRON
]

# Aspectos principais a serem considerados na análise.
ASPECTOS_RELEVANTES = ['CON', 'OPP', 'TRI', 'SEX', 'SQR']

# --- Funções Utilitárias ---

def formatar_data(data):
    """Garante que a data esteja no formato DD/MM/YYYY."""
    if "/" in data: return data
    return f"{data[:2]}/{data[2:4]}/{data[4:]}"

def formatar_hora(hora):
    """Garante que a hora esteja no formato HH:MM."""
    if ":" in hora: return hora
    return f"{hora[:2]}/{hora[2:]}"

# --- Função Principal ---

def gerar_mapa(data_nasc, hora_nasc, cidade, estado):
    """
    Gera o mapa astral completo a partir dos dados de nascimento.
    """
    try:
        # 1. Preparação dos Dados de Entrada
        print("[DEBUG astrologia] Formatando data, hora e localização...")
        data_nasc_fmt = formatar_data(data_nasc)
        hora_nasc_fmt = formatar_hora(hora_nasc)

        geolocator = Nominatim(user_agent="verba_mapa_astral")
        location = geolocator.geocode(f"{cidade}, {estado}, Brasil")
        if not location:
            raise ValueError("Localização não encontrada.")
        print(f"[DEBUG astrologia] Localização encontrada: {location.latitude}, {location.longitude}")

        # 2. Conversão de Data/Hora para UTC
        print("[DEBUG astrologia] Montando datetime local e convertendo para UTC...")
        local_tz = pytz.timezone("America/Sao_Paulo")
        dt_local = local_tz.localize(datetime.datetime.strptime(f"{data_nasc_fmt} {hora_nasc_fmt}", "%d/%m/%Y %H:%M"))
        dt_utc = dt_local.astimezone(pytz.utc)

        # 3. Criação do Mapa Astral com Flatlib
        print("[DEBUG astrologia] Criando chart astral com flatlib...")
        dt = Datetime(dt_utc.strftime("%Y/%m/%d"), dt_utc.strftime("%H:%M"))
        pos = GeoPos(location.latitude, location.longitude)
        chart = Chart(dt, pos, hsys=const.HOUSES_PLACIDUS, IDs=OBJETOS)

        # 4. Extração de Dados do Mapa
        mapa = {
            'planetas': {}, 'aspectos': [],
            'elementos': {'Fogo': 0, 'Terra': 0, 'Ar': 0, 'Agua': 0},
            'modalidades': {'Cardinal': 0, 'Fixo': 0, 'Mutavel': 0}
        }

        # --- Posições dos Planetas e Contagem de Elementos/Modalidades ---
        for obj_id in OBJETOS:
            planeta = chart.get(obj_id)
            signo = planeta.sign

            # Garante que a longitude seja um número para os cálculos
            lon_float = float(planeta.lon)
            grau = int(lon_float)
            minuto = int((lon_float - grau) * 60)
            
            # ===== CORREÇÃO PRINCIPAL =====
            # Acessa a casa diretamente do objeto calculado pela flatlib.
            # Este método é simples, direto e confiável.
            try:
                casa = planeta.house.id
            except AttributeError:
                # Objetos como Nodos podem não ter uma casa definida pela biblioteca.
                casa = 0

            mapa['planetas'][obj_id] = {
                'signo': signo, 'grau': grau, 'minuto': minuto, 'casa': casa
            }

            # Contagem de elementos e modalidades de forma eficiente
            if planeta.id not in [const.NORTH_NODE, const.SOUTH_NODE]: # Nodos não contam para o balanço
                signo_info = const.ZODIAC_INFO[signo]
                if 'element' in signo_info:
                    mapa['elementos'][signo_info['element']] += 1
                if 'quality' in signo_info:
                    mapa['modalidades'][signo_info['quality']] += 1

        # --- Adiciona o Ascendente manualmente ---
        asc = chart.get(const.ASC)
        asc_lon_float = float(asc.lon)
        mapa['planetas']['Asc'] = {
            'signo': asc.sign,
            'grau': int(asc_lon_float),
            'minuto': int((asc_lon_float - int(asc_lon_float)) * 60),
            'casa': 1  # O Ascendente é sempre a cúspide da casa 1
        }
        
        # --- Cálculo de Aspectos ---
        print("[DEBUG astrologia] Calculando aspectos entre objetos...")
        for i in range(len(OBJETOS)):
            for j in range(i + 1, len(OBJETOS)):
                p1_id = OBJETOS[i]
                p2_id = OBJETOS[j]
                p1 = chart.get(p1_id)
                p2 = chart.get(p2_id)
                
                try:
                    # Usa a função da flatlib para obter o aspecto entre dois planetas
                    aspecto = aspects.getAspect(p1, p2, ASPECTOS_RELEVANTES)
                    if aspecto:
                        mapa['aspectos'].append({
                            'planeta1': p1_id,
                            'planeta2': p2_id,
                            'aspecto': aspecto.type,
                            'orb': round(aspecto.orb, 2)
                        })
                except Exception as e:
                    # Este log ajuda a identificar problemas específicos de aspecto, se houver
                    print(f"[ERRO ASPECTO] Falha ao calcular aspecto entre {p1_id} e {p2_id}: {e}")

        print("[DEBUG astrologia] Mapa astral final gerado com sucesso.")
        return mapa

    except Exception as e:
        print(f"[ERRO GERAL ao gerar mapa] {repr(e)}")
        # Em caso de qualquer erro, retorna None para ser tratado pelo chamador.
        return None