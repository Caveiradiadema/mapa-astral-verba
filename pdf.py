from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.units import cm
from PIL import Image as PILImage
import os

# Cores
COR_TEXTO = colors.HexColor("#F0EAD6")

# Dicionários (PLANETA_PT, PLANETA_DESC etc...) — [mantenha os seus atuais aqui]

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
    try:
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
                with PILImage.open(img_path) as pil_img:
                    aspect_ratio = pil_img.height / pil_img.width
                    largura = 12 * cm
                    altura = largura * aspect_ratio
                story.append(Image(img_path, width=largura, height=altura, hAlign='CENTER'))

        doc.build(story)

    except Exception as e:
        print("[ERRO PDF]", e)
        raise
