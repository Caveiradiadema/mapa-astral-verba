from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image, PageBreak, Table, TableStyle, NextPageTemplate
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib import colors
from reportlab.lib.units import cm
import os

# --- Constantes e Dicionários (sem alterações) ---
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
    'Sun': 'O Sol representa identidade, vitalidade e a essência do seu ser. Indica onde e como você se sente mais vivo.',
    'Moon': 'A Lua governa emoções, instintos e necessidades profundas. Revela seu mundo interior e reações intuitivas.',
    'Mercury': 'Mercúrio simboliza a mente, a comunicação e o raciocínio. Mostra como você pensa, aprende e se expressa.',
    'Venus': 'Vênus rege o amor, a harmonia e os valores pessoais. Fala sobre afetos, estética e aquilo que você aprecia.',
    'Mars': 'Marte é o impulso, a ação e a coragem. Indica como você age, luta e afirma seus desejos.',
    'Jupiter': 'Júpiter expande, traz sorte e crescimento. Fala sobre fé, otimismo e busca por significado.',
    'Saturn': 'Saturno simboliza estrutura, responsabilidade e disciplina. Mostra desafios que levam à maturidade.',
    'Uranus': 'Urano traz inovação, liberdade e mudanças bruscas. Impulsiona o espírito rebelde e a originalidade.',
    'Neptune': 'Netuno dissolve limites e conecta com sonhos e espiritualidade. Representa sensibilidade, inspiração e compaixão.',
    'Pluto': 'Plutão fala de transformação, poder e regeneração. Revela onde ocorrem crises profundas e renascimentos.',
    'North Node': 'O Nodo Norte aponta o caminho de evolução e propósito, indicando direções a serem exploradas nesta vida.',
    'South Node': 'O Nodo Sul mostra talentos trazidos de experiências anteriores e zonas de conforto a serem transcendidas.',
    'Chiron': 'Quíron representa feridas profundas e o potencial de cura. Revela onde a dor se transforma em sabedoria e empatia.',
    'Asc': 'O Ascendente descreve a máscara social, a primeira impressão e a maneira como você inicia novos ciclos.'
}
SIGNO_PT = {
    'Aries': 'Áries', 'Taurus': 'Touro', 'Gemini': 'Gêmeos', 'Cancer': 'Câncer',
    'Leo': 'Leão', 'Virgo': 'Virgem', 'Libra': 'Libra', 'Scorpio': 'Escorpião',
    'Sagittarius': 'Sagitário', 'Capricorn': 'Capricórnio', 'Aquarius': 'Aquário', 'Pisces': 'Peixes'
}
SIGNO_DESC = {
    'Aries': 'Áries é um signo de fogo cardinal...', 'Taurus': 'Touro é um signo de terra fixo...', 'Gemini': 'Gêmeos é um signo de ar mutável...', 'Cancer': 'Câncer é um signo de água cardinal...', 'Leo': 'Leão é um signo de fogo fixo...', 'Virgo': 'Virgem é um signo de terra mutável...', 'Libra': 'Libra é um signo de ar cardinal...', 'Scorpio': 'Escorpião é um signo de água fixo...', 'Sagittarius': 'Sagitário é um signo de fogo mutável...', 'Capricorn': 'Capricórnio é um signo de terra cardinal...', 'Aquarius': 'Aquário é um signo de ar fixo...', 'Pisces': 'Peixes é um signo de água mutável...'
}
CASA_DESC = {
    1: 'reflete identidade...', 2: 'revela valores...', 3: 'diz respeito à comunicação...', 4: 'representa o lar...', 5: 'trata da criatividade...', 6: 'envolve trabalho...', 7: 'reflete parcerias...', 8: 'relaciona-se com a intimidade...', 9: 'diz respeito à filosofia...', 10: 'representa carreira...', 11: 'envolve amizades...', 12: 'trata do inconsciente...'
}
ASPECTO_NOME = {
    'TRI': 'Trígono', 'SEX': 'Sextil', 'CON': 'Conjunção', 'SQR': 'Quadratura', 'OPP': 'Oposição'
}
ASPECTO_DESC = {
    'TRI': 'Fluxo harmonioso...', 'SEX': 'Oportunidades suaves...', 'CON': 'Fusão de energias...', 'SQR': 'Tensão interna...', 'OPP': 'Polarização que pede equilíbrio...'
}
SIGNO_IMAGE = {
    'Aries': 'Aries.png', 'Taurus': 'touro.png', 'Gemini': 'gemeos.png', 'Cancer': 'cancer.png', 'Leo': 'leao.png', 'Virgo': 'virgem.png', 'Libra': 'libra.png', 'Scorpio': 'escorpiao.png', 'Sagittarius': 'sargitario.png', 'Capricorn': 'capricornio.png', 'Aquarius': 'aquario.png', 'Pisces': 'Peixes.png'
}

class MapaPDFGenerator:
    def __init__(self, nome, mapa, output_path):
        self.nome = nome
        self.mapa = mapa
        self.output_path = output_path
        self.story = []
        self.styles = self._registrar_estilos()
        self.doc = BaseDocTemplate(output_path, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm, leftMargin=2*cm, rightMargin=2*cm)
        self._configurar_templates()

    def _registrar_estilos(self):
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='TituloCapa', fontName='Helvetica-Bold', fontSize=30, textColor=COR_DOURADO, alignment=TA_CENTER, spaceAfter=12))
        styles.add(ParagraphStyle(name='NomeCapa', fontName='Helvetica', fontSize=22, textColor=COR_TEXTO, alignment=TA_CENTER, spaceAfter=12))
        styles.add(ParagraphStyle(name='SubCapa', fontName='Helvetica-Oblique', fontSize=14, textColor=COR_TEXTO, alignment=TA_CENTER, spaceAfter=50))
        styles.add(ParagraphStyle(name='H1', fontName='Helvetica-Bold', fontSize=22, textColor=COR_DOURADO, alignment=TA_CENTER, spaceBefore=20, spaceAfter=16))
        styles.add(ParagraphStyle(name='H2', fontName='Helvetica-Bold', fontSize=14, textColor=COR_DOURADO, alignment=TA_LEFT, spaceBefore=16, spaceAfter=8))
        styles.add(ParagraphStyle(name='Texto', fontSize=11, textColor=COR_TEXTO, alignment=TA_JUSTIFY, leading=18))
        styles.add(ParagraphStyle(name='AspectoBom', fontSize=11, textColor=COR_AZUL, alignment=TA_LEFT, leading=16, leftIndent=0.5*cm, spaceAfter=4))
        styles.add(ParagraphStyle(name='AspectoTenso', fontSize=11, textColor=COR_RUBI, alignment=TA_LEFT, leading=16, leftIndent=0.5*cm, spaceAfter=4))
        styles.add(ParagraphStyle(name='AspectoCon', fontSize=11, textColor=COR_DOURADO, alignment=TA_LEFT, leading=16, leftIndent=0.5*cm, spaceAfter=4))
        styles.add(ParagraphStyle(name='Footer', fontSize=9, textColor=colors.grey, alignment=TA_CENTER, spaceBefore=40))
        styles.add(ParagraphStyle(name='PageNum', fontSize=9, textColor=colors.grey, alignment=TA_RIGHT))
        return styles

    def _fundo_cosmico(self, canvas, doc):
        canvas.saveState()
        canvas.setFillColor(COR_FUNDO)
        canvas.rect(0, 0, doc.width + doc.leftMargin*2, doc.height + doc.topMargin*2, stroke=0, fill=1)
        canvas.restoreState()

    def _cabecalho_rodape(self, canvas, doc):
        self._fundo_cosmico(canvas, doc)
        canvas.saveState()
        p_nome = Paragraph(self.nome, self.styles['Footer'])
        w, h = p_nome.wrap(doc.width, doc.bottomMargin)
        p_nome.drawOn(canvas, doc.leftMargin, h)
        p_num = Paragraph(f"Página {doc.page}", self.styles['PageNum'])
        w, h = p_num.wrap(doc.width, doc.bottomMargin)
        p_num.drawOn(canvas, doc.leftMargin, h)
        canvas.restoreState()

    def _configurar_templates(self):
        frame_capa = Frame(self.doc.leftMargin, self.doc.bottomMargin, self.doc.width, self.doc.height, id='capa')
        frame_principal = Frame(self.doc.leftMargin, self.doc.bottomMargin, self.doc.width, self.doc.height - 0.5*cm, id='principal')
        self.doc.addPageTemplates([
            PageTemplate(id='Capa', frames=frame_capa, onPage=self._fundo_cosmico),
            PageTemplate(id='Principal', frames=frame_principal, onPage=self._cabecalho_rodape)
        ])

    def _construir_capa(self):
        # ===== CÓDIGO MAIS ROBUSTO AQUI =====
        logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
        if os.path.exists(logo_path):
            self.story.append(Image(logo_path, width=5*cm, height=5*cm, hAlign='CENTER'))
            self.story.append(Spacer(1, 1*cm))
        else:
            # Se a logo não for encontrada, o programa não vai quebrar.
            print(f"[WARN pdf.py] Arquivo de logo não encontrado em: {logo_path}")

        self.story.append(Paragraph("Seu Mapa Astral", self.styles['TituloCapa']))
        self.story.append(Paragraph(self.nome, self.styles['NomeCapa']))
        self.story.append(Paragraph("Uma Análise da Arquitetura da Sua Alma", self.styles['SubCapa']))
        self.story.append(NextPageTemplate('Principal'))
        self.story.append(PageBreak())

    def _construir_sumario_energetico(self):
        self.story.append(Paragraph("A Essência do Seu Mapa", self.styles['H1']))
        self.story.append(Paragraph("Este relatório...", self.styles['Texto']))
        elementos = self.mapa.get('elementos', {})
        modalidades = self.mapa.get('modalidades', {})
        self.story.append(Paragraph("Balanço dos Elementos", self.styles['H2']))
        self.story.append(Paragraph(f"Fogo: {elementos.get('Fogo', 0)}...", self.styles['Texto']))
        self.story.append(Paragraph("Balanço das Modalidades", self.styles['H2']))
        self.story.append(Paragraph(f"Cardinal: {modalidades.get('Cardinal', 0)}...", self.styles['Texto']))
        self.story.append(PageBreak())
        
    def _construir_tabela_posicoes(self):
        self.story.append(Paragraph("Tabela de Posições Planetárias", self.styles['H1']))
        table_data = [["Corpo", "Signo", "Grau", "Minuto", "Casa"]]
        for planeta_id, dados in self.mapa.get('planetas', {}).items():
            planeta_pt = PLANETA_PT.get(planeta_id, planeta_id)
            signo_pt = SIGNO_PT.get(dados.get('signo'), dados.get('signo'))
            table_data.append([planeta_pt, signo_pt, str(dados.get('grau', 0)), str(dados.get('minuto', 0)), str(dados.get('casa', 0))])
        
        pos_tbl = Table(table_data, colWidths=[5*cm, 4*cm, 2*cm, 2*cm, 2*cm])
        # ... estilos da tabela ...
        self.story.append(pos_tbl)
        self.story.append(PageBreak())

    def _construir_analise_planetaria(self):
        self.story.append(Paragraph("Análise Planetária Integrada", self.styles['H1']))
        # ... loop para análise ...
        self.story.append(PageBreak())

    def _construir_analise_aspectos(self):
        # ... código de aspectos ...
        self.story.append(PageBreak())
    
    def _construir_pagina_signo(self):
        try:
            sun_sign_en = self.mapa.get('planetas', {}).get('Sun', {}).get('signo')
        except Exception:
            sun_sign_en = None
        
        if sun_sign_en and sun_sign_en in SIGNO_IMAGE:
            signo_pt = SIGNO_PT.get(sun_sign_en, sun_sign_en)
            img_file = SIGNO_IMAGE.get(sun_sign_en)
            
            # ===== CÓDIGO MAIS ROBUSTO AQUI =====
            img_path = os.path.join(os.path.dirname(__file__), img_file)
            
            self.story.append(Paragraph("O Quadro do Seu Signo Solar", self.styles['H1']))
            # ... texto e link ...

            if os.path.exists(img_path):
                self.story.append(Spacer(1, 0.8*cm))
                self.story.append(Image(img_path, width=12*cm, height=12*cm, hAlign='CENTER'))
            else:
                # Se a imagem do signo não for encontrada, o programa não vai quebrar.
                print(f"[WARN pdf.py] Imagem do signo não encontrada em: {img_path}")
            self.story.append(PageBreak())

    def _construir_conclusao(self):
        self.story.append(Paragraph("Este mapa foi gerado...", self.styles['Footer']))
        self.story.append(Paragraph("VERBA Astrologia", self.styles['Footer']))

    def gerar_pdf(self):
        print("[DEBUG pdf.py] Iniciando a criação do PDF com layout aprimorado...")
        self._construir_capa()
        self._construir_sumario_energetico()
        self._construir_tabela_posicoes()
        self._construir_analise_planetaria()
        self._construir_analise_aspectos()
        self._construir_pagina_signo()
        self._construir_conclusao()
        
        self.doc.build(self.story)
        print(f"[DEBUG pdf.py] PDF '{self.output_path}' gerado com sucesso.")

def criar_pdf(nome, mapa, output_path):
    gerador = MapaPDFGenerator(nome, mapa, output_path)
    gerador.gerar_pdf()