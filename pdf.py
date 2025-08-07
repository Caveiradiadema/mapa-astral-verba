# pdf.py – gerador de PDF com foco em design e clareza para leigos
# =======================================================================
import os
import time
import unicodedata
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Frame, PageTemplate, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from flatlib import const

# Importe os textos que você irá escrever
from textos_astrologicos import (
    INTRO_METAFORA, COMO_LER, TEXTO_SOL, TEXTO_LUA, TEXTO_ASC,
    TEXTOS_ASPECTOS
)

# --- CONFIGURAÇÃO DE DESIGN ---
COR_FUNDO = colors.HexColor("#0D1B2A")
COR_TITULO_OURO = colors.HexColor("#D4AF37")
COR_SUBTITULO_AZUL = colors.HexColor("#89CFF0")
COR_TEXTO_BRANCO = colors.HexColor("#E2E8F0")
COR_LEGENDA_CINZA = colors.HexColor("#A0AEC0")

# --- ESTILOS DE TEXTO ---
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CapaTitulo", fontSize=32, leading=40, textColor=COR_TITULO_OURO, alignment=TA_CENTER, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="CapaSubtitulo", fontSize=18, leading=22, textColor=COR_TEXTO_BRANCO, alignment=TA_CENTER, fontName="Helvetica-Oblique"))
styles.add(ParagraphStyle(name="TituloCapitulo", fontSize=20, leading=24, textColor=COR_TITULO_OURO, alignment=TA_LEFT, spaceAfter=12, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="SubtituloPlaneta", fontSize=16, leading=20, textColor=COR_SUBTITULO_AZUL, alignment=TA_LEFT, spaceBefore=10, spaceAfter=4, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="CorpoTexto", fontSize=12, leading=18, textColor=COR_TEXTO_BRANCO, alignment=TA_JUSTIFY, spaceAfter=10))
styles.add(ParagraphStyle(name="Legenda", fontSize=9, leading=12, textColor=COR_LEGENDA_CINZA, alignment=TA_LEFT, spaceAfter=12))
styles.add(ParagraphStyle(name="Link", fontSize=12, leading=18, textColor=COR_SUBTITULO_AZUL, alignment=TA_CENTER, spaceAfter=10))


# --- FUNÇÕES AUXILIARES ---
def background_page(canvas, doc):
    """Desenha o fundo azul escuro em todas as páginas."""
    canvas.saveState()
    canvas.setFillColor(COR_FUNDO)
    canvas.rect(0, 0, doc.width + 2 * doc.leftMargin, doc.height + 2 * doc.bottomMargin, fill=1, stroke=0)
    canvas.restoreState()

def normalizar_nome_signo(nome_signo):
    """Converte 'Áries' para 'aries', 'Gêmeos' para 'gemeos', etc."""
    if nome_signo == "Sagitário":
        return "sargitario" # Mantendo o nome do seu arquivo
    nfkd_form = unicodedata.normalize('NFKD', nome_signo)
    nome_sem_acentos = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    return nome_sem_acentos.lower()

# --- FUNÇÃO PRINCIPAL DE CRIAÇÃO DO PDF ---
def criar_pdf(mapa: dict) -> str:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PDF_DIR = os.path.join(BASE_DIR, "pdfs")
    STATIC_DIR = os.path.join(BASE_DIR, "static")
    os.makedirs(PDF_DIR, exist_ok=True)

    filename = f"mapa_{mapa['nome'].replace(' ', '_')}_{int(time.time())}.pdf"
    path_pdf = os.path.join(PDF_DIR, filename)

    doc = SimpleDocTemplate(path_pdf, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    
    story = []
    objetos = mapa["objetos"]

    # --- PÁGINA 1: CAPA ---
    logo_path = os.path.join(STATIC_DIR, "logo.png")
    if os.path.exists(logo_path):
        story.append(Image(logo_path, width=5*cm, height=5*cm, hAlign='CENTER'))
        story.append(Spacer(1, 1 * cm))
    else:
        story.append(Spacer(1, 6 * cm))

    story.append(Paragraph("Seu Mapa Astral", styles["CapaTitulo"]))
    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph(mapa["nome"], styles["CapaSubtitulo"]))
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph(f"{mapa['data']} | {mapa['hora']} | {mapa['cidade']}-{mapa['estado']}", styles["CapaSubtitulo"]))
    story.append(PageBreak())

    # --- PÁGINA 2: INTRODUÇÃO ---
    story.append(Paragraph("A Arquitetura da Sua Alma", styles["TituloCapitulo"]))
    story.append(Paragraph(INTRO_METAFORA, styles["CorpoTexto"]))
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph(COMO_LER, styles["CorpoTexto"]))
    story.append(PageBreak())

    # --- PÁGINA 3: OS PILARES (BIG 3) ---
    story.append(Paragraph("Os Pilares da Sua Identidade", styles["TituloCapitulo"]))
    
    sol = objetos[const.SUN]
    story.append(Paragraph(f"O Sol em {sol['signo_pt']}", styles["SubtituloPlaneta"]))
    if sol['casa'] > 0: story.append(Paragraph(f"Na Casa {sol['casa']}", styles["Legenda"]))
    story.append(Paragraph(TEXTO_SOL.get(sol['signo_pt'], "O Sol representa sua identidade, sua essência e a força vital que te impulsiona pela vida."), styles["CorpoTexto"]))

    lua = objetos[const.MOON]
    story.append(Paragraph(f"A Lua em {lua['signo_pt']}", styles["SubtituloPlaneta"]))
    if lua['casa'] > 0: story.append(Paragraph(f"Na Casa {lua['casa']}", styles["Legenda"]))
    story.append(Paragraph(TEXTO_LUA.get(lua['signo_pt'], "A Lua governa seu mundo emocional, suas necessidades instintivas e o que te traz segurança e conforto."), styles["CorpoTexto"]))

    asc = objetos[const.ASC]
    story.append(Paragraph(f"O Ascendente em {asc['signo_pt']}", styles["SubtituloPlaneta"]))
    story.append(Paragraph(TEXTO_ASC.get(asc['signo_pt'], "O Ascendente é a sua 'máscara' social, a primeira impressão que você causa e a energia que você está aprendendo a expressar no mundo."), styles["CorpoTexto"]))
    story.append(PageBreak())

    # --- PÁGINA 4: ASPECTOS PRINCIPAIS ---
    story.append(Paragraph("A Trama da Sua Vida: Diálogos Internos", styles["TituloCapitulo"]))
    story.append(Paragraph("Aspectos são as 'conversas' entre os planetas. Alguns diálogos são fluidos e fáceis (Trígonos, Sextis), outros são tensos e exigem esforço e crescimento (Quadraturas, Oposições).", styles["CorpoTexto"]))

    for asp in mapa["aspectos"]:
        key = f"{asp['p1_id']}-{asp['p2_id']}-{asp['tipo_en']}"
        texto_explicativo = TEXTOS_ASPECTOS.get(key, TEXTOS_ASPECTOS.get(f"{asp['p2_id']}-{asp['p1_id']}-{asp['tipo_en']}", "Cada aspecto em seu mapa tece uma parte única da sua personalidade."))
        
        story.append(Paragraph(f"{asp['p1_nome']} em {asp['tipo_pt']} com {asp['p2_nome']}", styles["SubtituloPlaneta"]))
        story.append(Paragraph(f"Orbe: {asp['orbe']}°", styles["Legenda"]))
        story.append(Paragraph(texto_explicativo, styles["CorpoTexto"]))
    story.append(PageBreak())

    # --- PÁGINA FINAL: IMAGEM E LINK ---
    story.append(Paragraph("Seu Quadro Solar", styles["TituloCapitulo"]))
    
    signo_solar_nome_pt = sol['signo_pt']
    signo_solar_norm = normalizar_nome_signo(signo_solar_nome_pt)
    
    imagem_path = os.path.join(STATIC_DIR, f"{signo_solar_norm}.png")
    
    if os.path.exists(imagem_path):
        story.append(Image(imagem_path, width=15*cm, height=15*cm, hAlign='CENTER'))
        story.append(Spacer(1, 1*cm))
    
    link_url = f"https://caveiradiadema.github.io/verba-site/{signo_solar_norm}.html"
    texto_link = f'<a href="{link_url}" color="{COR_SUBTITULO_AZUL}"><u>Clique aqui para ver seu quadro de {signo_solar_nome_pt} em nosso site!</u></a>'
    story.append(Paragraph(texto_link, styles["Link"]))

    story.append(Spacer(1, 1.5*cm))
    story.append(Paragraph("Gerado por VERBA Astrologia ©", styles["Legenda"]))

    # --- CORREÇÃO APLICADA AQUI ---
    # Removemos o PageTemplate e usamos os argumentos onFirstPage/onLaterPages
    # no método build() para uma aplicação mais confiável do fundo.
    doc.build(story, onFirstPage=background_page, onLaterPages=background_page)
    
    print(f"[INFO pdf] Criado com sucesso: {path_pdf}")
    return os.path.relpath(path_pdf, BASE_DIR)