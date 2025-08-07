# astrologia.py – cálculo do mapa astral (versão final corrigida)
# =============================================================
import os, pytz, traceback
from datetime import datetime
from geopy.geocoders import Nominatim
import swisseph as swe

# ─── 1. EPHEMERIS ───────────────────────────────────────────────
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
EPHE_PATH = os.path.join(BASE_DIR, "sweph", "ephe")
os.environ["SE_EPHE_PATH"]      = EPHE_PATH
os.environ["FLATLIB_EPHE_PATH"] = EPHE_PATH
swe.set_ephe_path(EPHE_PATH)
print(f"[INFO] EPHE_PATH configurado: {EPHE_PATH}")

# ─── 2. FLATLIB E CONFIGURAÇÕES ────────────────────────────────
from flatlib.chart    import Chart
from flatlib.datetime import Datetime
from flatlib.geopos   import GeoPos
from flatlib          import const, aspects

# Corpos celestes que a biblioteca precisa calcular (sem o Ascendente)
CORPOS_PARA_CALCULO = [
    const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS,
    const.JUPITER, const.SATURN, const.URANUS, const.NEPTUNE, const.PLUTO,
    const.NORTH_NODE, const.CHIRON
]

# Pontos que usaremos para análise de aspectos (incluindo o Ascendente)
PONTOS_PARA_ASPECTOS = CORPOS_PARA_CALCULO + [const.ASC]

# ângulos numéricos para buscar aspectos
ANGULOS = [0, 60, 90, 120, 180]

# --- DICIONÁRIOS DE TRADUÇÃO ---
ID_PARA_PT = {
    const.SUN: "Sol", const.MOON: "Lua", const.MERCURY: "Mercúrio",
    const.VENUS: "Vênus", const.MARS: "Marte", const.JUPITER: "Júpiter",
    const.SATURN: "Saturno", const.URANUS: "Urano", const.NEPTUNE: "Netuno",
    const.PLUTO: "Plutão", const.NORTH_NODE: "Nodo Norte", const.CHIRON: "Quíron",
    const.ASC: "Ascendente"
}

# Dicionário para traduzir o nome do aspecto (em inglês, minúsculo) para português
TIPO_ASPECTO_PT = {
    "conjunction": "Conjunção", "sextile": "Sextil", "square": "Quadratura",
    "trine": "Trígono", "opposition": "Oposição"
}

# Dicionário reverso para converter ângulo em nome
ANGULO_PARA_NOME_EN = {
    0: "conjunction", 60: "sextile", 90: "square",
    120: "trine", 180: "opposition"
}

SIGNO_PT = {
    'Aries':'Áries','Taurus':'Touro','Gemini':'Gêmeos','Cancer':'Câncer',
    'Leo':'Leão','Virgo':'Virgem','Libra':'Libra','Scorpio':'Escorpião',
    'Sagittarius':'Sagitário','Capricorn':'Capricórnio','Aquarius':'Aquário',
    'Pisces':'Peixes'
}

# helpers de formatação
fmt_data = lambda d: d if "/" in d else f"{d[:2]}/{d[2:4]}/{d[4:]}"
fmt_hora = lambda h: h if ":" in h else f"{h[:2]}:{h[2:]}"
_casa    = lambda b: b.house.id if hasattr(b, 'house') and b.house is not None else 0

# ─── 3. FUNÇÃO PRINCIPAL ───────────────────────────────────────
def gerar_mapa_astral(nome:str, data:str, hora:str, cidade:str, estado:str):
    # --- CORREÇÃO APLICADA AQUI: O bloco try/except agora envolve toda a função ---
    try:
        geo = Nominatim(user_agent="verba-astrologia-v4").geocode(f"{cidade}, {estado}, Brasil")
        if not geo: raise ValueError("Localização não encontrada.")
        lat, lon = float(geo.latitude), float(geo.longitude)

        dt_local = pytz.timezone("America/Sao_Paulo").localize(
            datetime.strptime(f"{fmt_data(data)} {fmt_hora(hora)}", "%d/%m/%Y %H:%M")
        )
        dt_utc = dt_local.astimezone(pytz.utc)

        chart = Chart(
            Datetime(dt_utc.strftime("%Y/%m/%d"), dt_utc.strftime("%H:%M"), "+00:00"),
            GeoPos(lat, lon),
            IDs=CORPOS_PARA_CALCULO,
            hsys=const.HOUSES_PLACIDUS
        )

        objetos_mapa = {}
        for pid in PONTOS_PARA_ASPECTOS:
            obj = chart.get(pid)
            objetos_mapa[pid] = {
                "id": pid, "nome_pt": ID_PARA_PT.get(pid, pid),
                "signo_pt": SIGNO_PT.get(obj.sign, obj.sign),
                "grau_completo": obj.lon, "grau": int(obj.lon),
                "minuto": int((obj.lon - int(obj.lon)) * 60), "casa": _casa(obj)
            }

        aspectos_exp = []
        for i, p1_id in enumerate(PONTOS_PARA_ASPECTOS):
            for p2_id in PONTOS_PARA_ASPECTOS[i + 1:]:
                orbe_max = 5 if p1_id in [const.SUN, const.MOON] or p2_id in [const.SUN, const.MOON] else 3
                aspecto = aspects.getAspect(chart.get(p1_id), chart.get(p2_id), ANGULOS)
                
                if aspecto and abs(aspecto.orb) <= orbe_max:
                    tipo_en_lower = ""
                    if isinstance(aspecto.type, str):
                        tipo_en_lower = aspecto.type.lower()
                    elif isinstance(aspecto.type, int):
                        tipo_en_lower = ANGULO_PARA_NOME_EN.get(aspecto.type, "")

                    if not tipo_en_lower: continue

                    aspectos_exp.append({
                        "p1_id": p1_id, "p2_id": p2_id,
                        "p1_nome": ID_PARA_PT.get(p1_id, p1_id),
                        "p2_nome": ID_PARA_PT.get(p2_id, p2_id),
                        "tipo_en": tipo_en_lower,
                        "tipo_pt": TIPO_ASPECTO_PT.get(tipo_en_lower, tipo_en_lower.capitalize()),
                        "orbe": round(aspecto.orb, 2)
                    })
        
        return {
            "nome": nome, "data": fmt_data(data), "hora": fmt_hora(hora),
            "cidade": cidade, "estado": estado,
            "objetos": objetos_mapa,
            "aspectos": aspectos_exp
        }

    except Exception as e:
        print(f"[ERRO FATAL em gerar_mapa_astral] {e}")
        traceback.print_exc()
        return None