from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.units import cm
from PIL import Image as PILImage
import os

# Cores e estilos
COR_FUNDO = colors.HexColor("#0D1B2A")
COR_TEXTO = colors.HexColor("#F0EAD6")
COR_DOURADO = colors.HexColor("#CBB26A")
COR_AZUL = colors.HexColor("#89CFF0")
COR_RUBI = colors.HexColor("#C44536")
COR_LINHA = colors.HexColor("#13294B")

PLANETA_PT = {
    'Sun': 'Sol', 'Moon': 'Lua', 'Mercury': 'Mercúrio', 'Venus': 'Vênus',
    'Mars': 'Marte', 'Jupiter': 'Júpiter', 'Saturn': 'Saturno',
    'Uranus': 'Urano', 'Neptune': 'Netuno', 'Pluto': 'Plutão',
    'North Node': 'Nodo Norte', 'South Node': 'Nodo Sul', 'Chiron': 'Quíron',
    'Asc': 'Ascendente'
}

PLANETA_DESC = {
    'Sun': 'O Sol representa identidade, vitalidade e a essência do seu ser.',
    'Moon': 'A Lua governa emoções, instintos e necessidades profundas.',
    'Mercury': 'Mercúrio simboliza a mente, a comunicação e o raciocínio.',
    'Venus': 'Vênus rege o amor, a harmonia e os valores pessoais.',
    'Mars': 'Marte é o impulso, a ação e a coragem.',
    'Jupiter': 'Júpiter expande, traz sorte e crescimento.',
    'Saturn': 'Saturno simboliza estrutura, responsabilidade e disciplina.',
    'Uranus': 'Urano traz inovação, liberdade e mudanças bruscas.',
    'Neptune': 'Netuno dissolve limites e conecta com sonhos e espiritualidade.',
    'Pluto': 'Plutão fala de transformação, poder e regeneração.',
    'North Node': 'O Nodo Norte aponta o caminho de evolução e propósito.',
    'South Node': 'O Nodo Sul mostra talentos trazidos de experiências anteriores.',
    'Chiron': 'Quíron representa feridas profundas e o potencial de cura.',
    'Asc': 'O Ascendente descreve a máscara social e a primeira impressão.'
}

SIGNO_PT = {
    'Aries': 'Áries', 'Taurus': 'Touro', 'Gemini': 'Gêmeos', 'Cancer': 'Câncer',
    'Leo': 'Leão', 'Virgo': 'Virgem', 'Libra': 'Libra', 'Scorpio': 'Escorpião',
    'Sagittarius': 'Sagitário', 'Capricorn': 'Capricórnio', 'Aquarius': 'Aquário', 'Pisces': 'Peixes'
}

SIGNO_DESC = {
    'Aries': 'Áries é um signo de fogo cardinal associado à iniciativa e coragem.',
    'Taurus': 'Touro é um signo de terra fixo, ligado à estabilidade e sensualidade.',
    'Gemini': 'Gêmeos é um signo de ar mutável, marcado pela curiosidade e comunicação.',
    'Cancer': 'Câncer é um signo de água cardinal, que preza o cuidado e sensibilidade.',
    'Leo': 'Leão é um signo de fogo fixo, relacionado à criatividade e generosidade.',
    'Virgo': 'Virgem é um signo de terra mutável, detalhista e dedicado ao serviço.',
    'Libra': 'Libra é um signo de ar cardinal que busca equilíbrio e justiça.',
    'Scorpio': 'Escorpião é um signo de água fixo, intenso e transformador.',
    'Sagittarius': 'Sagitário é um signo de fogo mutável, filosófico e otimista.',
    'Capricorn': 'Capricórnio é um signo de terra cardinal, ambicioso e disciplinado.',
    'Aquarius': 'Aquário é um signo de ar fixo, inovador e independente.',
    'Pisces': 'Peixes é um signo de água mutável, compassivo e imaginativo.'
}

CASA_DESC = {
    1: 'reflete identidade, temperamento e a forma como você se apresenta.',
    2: 'revela valores, recursos materiais e autoestima.',
    3: 'diz respeito à comunicação e aprendizado básico.',
    4: 'representa o lar, a família e as bases emocionais.',
    5: 'trata da criatividade, romances e expressão do prazer.',
    6: 'envolve trabalho, saúde e rotina.',
    7: 'reflete parcerias e relacionamentos.',
    8: 'relaciona-se com intimidade e transformações.',
    9: 'diz respeito à filosofia, viagens e fé.',
    10: 'representa carreira, reputação e vocação.',
    11: 'envolve amizades, grupos e coletividade.',
    12: 'trata do inconsciente, espiritualidade e processos de cura.'
}

ASPECTO_NOME = {
    'TRI': 'Trígono', 'SEX': 'Sextil', 'CON': 'Conjunção', 'SQR': 'Quadratura', 'OPP': 'Oposição'
}

ASPECTO_DESC = {
    'TRI': 'Fluxo harmonioso e talentos naturais.',
    'SEX': 'Oportunidades suaves que requerem iniciativa.',
    'CON': 'Fusão de energias com intensidade.',
    'SQR': 'Tensão que exige esforço para transformar.',
    'OPP': 'Polarização que pede equilíbrio entre extremos.'
}

SIGNO_IMAGE = {
    'Aries': 'Aries.png',
    'Taurus': 'touro.png',
    'Gemini': 'gemeos.png',
    'Cancer': 'cancer.png',
    'Leo': 'leao.png',
    'Virgo': 'virgem.png',
    'Libra': 'libra.png',
    'Scorpio': 'escorpiao.png',
    'Sagittarius': 'sargitario.png',
    'Capricorn': 'capricornio.png',
    'Aquarius': 'aquario.png',
    'Pisces': 'Peixes.png'
}

def interpretar_planeta(planeta_id, dados):
    planeta_pt = PLANETA_PT.get(planeta_id, planeta_id)
    signo_en = dados.get('signo')
    signo_pt = SIGNO_PT.get(signo_en, signo_en)
    casa = dados.get('casa', 0)
    desc_planeta = PLANETA_DESC.get(planeta_id, '')
    desc_signo = SIGNO_DESC.get(signo_en, '')
    desc_casa = CASA_DESC.get(casa, '')
    texto = (
        f"<b>{planeta_pt} em {signo_pt} na Casa {casa}</b>: "
        f"{desc_planeta} Em {signo_pt}, {desc_signo} Na Casa {casa}, {desc_casa}"
    )
    return texto

def interpretar_aspecto(asp):
    p1_pt = PLANETA_PT.get(asp.get('planeta1'), asp.get('planeta1'))
    p2_pt = PLANETA_PT.get(asp.get('planeta2'), asp.get('planeta2'))
    code = asp.get('aspecto')
    nome = ASPECTO_NOME.get(code, code)
    desc = ASPECTO_DESC.get(code, '')
    return f"<b>{p1_pt} {nome} {p2_pt}</b>: {desc}"

def criar_pdf(nome, mapa, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            topMargin=2*cm, bottomMargin=2*cm,
                            leftMargin=2*cm, rightMargin=2*cm)
    story = []
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Texto', fontSize=11, textColor=COR_TEXTO,
                              alignment=TA_JUSTIFY, leading=16))

    story.append(Paragraph(f"Mapa Astral de {nome}", styles['Title']))
    story.append(PageBreak())

    for planeta_id, dados in mapa.get('planetas', {}).items():
        story.append(Paragraph(interpretar_planeta(planeta_id, dados), styles['Texto']))
        story.append(Spacer(1, 0.5*cm))

    aspectos = mapa.get('aspectos', [])
    if aspectos:
        story.append(PageBreak())
        story.append(Paragraph("Aspectos entre os Planetas", styles['Title']))
        for asp in aspectos:
            story.append(Paragraph(interpretar_aspecto(asp), styles['Texto']))
            story.append(Spacer(1, 0.3*cm))

    sun_sign = mapa.get('planetas', {}).get('Sun', {}).get('signo')
    if sun_sign and sun_sign in SIGNO_IMAGE:
        img_file = SIGNO_IMAGE.get(sun_sign)
        img_path = os.path.join(os.path.dirname(__file__), img_file)
        if os.path.exists(img_path):
            story.append(PageBreak())
            story.append(Paragraph("Quadro do seu signo solar", styles['Title']))

            # Calcula altura proporcional com base em largura
            with PILImage.open(img_path) as pil_img:
                aspect_ratio = pil_img.height / pil_img.width
                largura = 12 * cm
                altura = largura * aspect_ratio

            story.append(Image(img_path, width=largura, height=altura, hAlign='CENTER'))

    doc.build(story)
