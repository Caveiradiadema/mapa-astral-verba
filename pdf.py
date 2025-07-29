from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib import colors
from reportlab.lib.units import cm
import os

# Paleta cósmica: define cores para o fundo, texto e destaques conforme o tema
# sugerido pelo usuário.
COR_FUNDO = colors.HexColor("#0D1B2A")    # azul-noite profundo para o fundo
COR_TEXTO = colors.HexColor("#F0EAD6")    # branco-giz para o corpo do texto
COR_DOURADO = colors.HexColor("#CBB26A")  # dourado antigo para títulos e adornos
COR_AZUL = colors.HexColor("#89CFF0")     # azul celeste para aspectos harmoniosos
COR_RUBI = colors.HexColor("#C44536")     # vermelho rubi para aspectos tensos

# Cor de fundo para linhas de tabelas (um azul mais suave para melhor contraste)
COR_LINHA = colors.HexColor("#13294B")  # azul escuro para linhas de tabelas

# Traduções de nomes de planetas e pontos astrológicos para português.
PLANETA_PT = {
    'Sun': 'Sol', 'Moon': 'Lua', 'Mercury': 'Mercúrio', 'Venus': 'Vênus',
    'Mars': 'Marte', 'Jupiter': 'Júpiter', 'Saturn': 'Saturno',
    'Uranus': 'Urano', 'Neptune': 'Netuno', 'Pluto': 'Plutão',
    'North Node': 'Nodo Norte', 'South Node': 'Nodo Sul', 'Chiron': 'Quíron',
    'Asc': 'Ascendente'
}

# Descrições gerais de cada planeta/ponto astrológico
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

# Tradução de signos (inglês → português) e suas características
SIGNO_PT = {
    'Aries': 'Áries', 'Taurus': 'Touro', 'Gemini': 'Gêmeos', 'Cancer': 'Câncer',
    'Leo': 'Leão', 'Virgo': 'Virgem', 'Libra': 'Libra', 'Scorpio': 'Escorpião',
    'Sagittarius': 'Sagitário', 'Capricorn': 'Capricórnio', 'Aquarius': 'Aquário', 'Pisces': 'Peixes'
}

SIGNO_DESC = {
    'Aries': 'Áries é um signo de fogo cardinal associado à iniciativa, coragem e impulso pioneiro. É direto, competitivo e apaixonado.',
    'Taurus': 'Touro é um signo de terra fixo, ligado à estabilidade, sensualidade e segurança material. É perseverante e aprecia conforto.',
    'Gemini': 'Gêmeos é um signo de ar mutável, marcado pela curiosidade, comunicação e versatilidade. Valoriza o aprendizado e a troca de ideias.',
    'Cancer': 'Câncer é um signo de água cardinal, que preza o cuidado, a sensibilidade e o vínculo emocional. Focado em família e raízes.',
    'Leo': 'Leão é um signo de fogo fixo, relacionado à criatividade, generosidade e orgulho. Busca brilhar e expressar autenticidade.',
    'Virgo': 'Virgem é um signo de terra mutável, detalhista, organizado e dedicado ao serviço. Prioriza a análise e a eficiência.',
    'Libra': 'Libra é um signo de ar cardinal que busca equilíbrio, beleza e justiça. Valoriza relações harmoniosas e cooperação.',
    'Scorpio': 'Escorpião é um signo de água fixo, intenso, misterioso e transformador. Focado em profundidade emocional e poder.',
    'Sagittarius': 'Sagitário é um signo de fogo mutável, filosófico, otimista e explorador. Ama aventuras, viagens e liberdade.',
    'Capricorn': 'Capricórnio é um signo de terra cardinal, ambicioso, disciplinado e pragmático. Orientado para realizações e status.',
    'Aquarius': 'Aquário é um signo de ar fixo, inovador, humanitário e independente. Favorece o progresso e as ideias originais.',
    'Pisces': 'Peixes é um signo de água mutável, compassivo, imaginativo e sensível. Inclinado à espiritualidade e empatia.'
}

# Descrições das casas astrológicas (1–12). Usadas para narrativas integradas.
CASA_DESC = {
    1: 'reflete identidade, temperamento e a forma como você se apresenta ao mundo.',
    2: 'revela valores, recursos materiais e autoestima. Relaciona-se com segurança e conforto.',
    3: 'diz respeito à comunicação, ao aprendizado básico e à relação com irmãos e vizinhos.',
    4: 'representa o lar, a família e as bases emocionais. Fala de raízes e privacidade.',
    5: 'trata da criatividade, dos romances, dos filhos e da expressão do prazer.',
    6: 'envolve trabalho cotidiano, saúde e serviço. Demonstra hábitos e rotinas.',
    7: 'reflete parcerias e relacionamentos significativos, tanto pessoais quanto profissionais.',
    8: 'relaciona-se com a intimidade, recursos compartilhados, sexualidade e transformações.',
    9: 'diz respeito à filosofia, às viagens longas, à fé e ao conhecimento superior.',
    10: 'representa carreira, reputação e vocação. Indica ambições e reconhecimento público.',
    11: 'envolve amizades, grupos, ideais e o senso de coletividade.',
    12: 'trata do inconsciente, do isolamento e da espiritualidade. Envolve finais e processos de cura.'
}

# Nome completo e descrição dos principais aspectos utilizados
ASPECTO_NOME = {
    'TRI': 'Trígono', 'SEX': 'Sextil', 'CON': 'Conjunção', 'SQR': 'Quadratura', 'OPP': 'Oposição'
}

ASPECTO_DESC = {
    'TRI': 'Fluxo harmonioso e talentos naturais; favorece cooperação espontânea.',
    'SEX': 'Oportunidades suaves e facilidades que requerem alguma iniciativa.',
    'CON': 'Fusão de energias: intensifica tanto os dons quanto os desafios.',
    'SQR': 'Tensão interna e desafios; exige esforço consciente para transformar conflitos.',
    'OPP': 'Polarização que pede equilíbrio entre extremos, promovendo integração das diferenças.'
}

# Mapeia cada signo em inglês para o arquivo de imagem correspondente fornecido pelo usuário.
# Esses nomes são sensíveis a maiúsculas e minúsculas e devem corresponder aos arquivos existentes.
SIGNO_IMAGE = {
    'Aries': 'Aries.png',
    'Taurus': 'touro.png',
    'Gemini': 'gemeos.png',
    'Cancer': 'cancer.png',
    'Leo': 'leao.png',
    'Virgo': 'virgem.png',
    'Libra': 'libra.png',
    'Scorpio': 'escorpiao.png',
    'Sagittarius': 'sargitario.png',  # conforme nome do arquivo enviado
    'Capricorn': 'capricornio.png',
    'Aquarius': 'aquario.png',
    'Pisces': 'Peixes.png'
}

def interpretar_planeta(planeta_id, dados):
    """Gera uma narrativa integrada para um planeta dado o seu signo e casa."""
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
    """Retorna uma descrição textual de um aspecto entre dois corpos."""
    p1_pt = PLANETA_PT.get(asp.get('planeta1'), asp.get('planeta1'))
    p2_pt = PLANETA_PT.get(asp.get('planeta2'), asp.get('planeta2'))
    code = asp.get('aspecto')
    nome = ASPECTO_NOME.get(code, code)
    desc = ASPECTO_DESC.get(code, '')
    return f"<b>{p1_pt} {nome} {p2_pt}</b>: {desc}"

def criar_pdf(nome, mapa, output_path):
    """
    Gera um PDF estilizado contendo um mapa astral completo.

    O relatório inclui:
      • Capa com logo e título.
      • Sumário energético (elementos e modalidades).
      • Análise integrada para cada planeta/ponto astrológico.
      • Seção de aspectos (harmoniosos, desafiadores e fusão).
      • Página final com link e imagem do quadro do signo solar do usuário.

    Parâmetros:
      nome: nome do usuário a ser exibido na capa.
      mapa: dicionário retornado por gerar_mapa(), contendo planetas, aspectos, elementos e modalidades.
      output_path: caminho do arquivo PDF a ser gerado.
    """
    print("[DEBUG pdf.py] Iniciando criação do PDF...")
    print(f"[DEBUG pdf.py] Dados do mapa recebidos: {mapa}")

    # Configura o documento com margens generosas para uma apresentação elegante
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        topMargin=2*cm, bottomMargin=2*cm,
        leftMargin=2*cm, rightMargin=2*cm
    )
    story = []

    # Estilos
    styles = getSampleStyleSheet()
    # Capa
    styles.add(ParagraphStyle(
        name='TituloCapa', fontName='Helvetica-Bold', fontSize=30,
        textColor=COR_DOURADO, alignment=TA_CENTER, spaceAfter=12
    ))
    styles.add(ParagraphStyle(
        name='NomeCapa', fontName='Helvetica', fontSize=22,
        textColor=COR_TEXTO, alignment=TA_CENTER, spaceAfter=12
    ))
    styles.add(ParagraphStyle(
        name='SubCapa', fontName='Helvetica-Oblique', fontSize=14,
        textColor=COR_TEXTO, alignment=TA_CENTER, spaceAfter=50
    ))
    # Cabeçalhos e textos
    styles.add(ParagraphStyle(
        name='H1', fontName='Helvetica-Bold', fontSize=22,
        textColor=COR_DOURADO, alignment=TA_CENTER,
        spaceBefore=24, spaceAfter=16
    ))
    styles.add(ParagraphStyle(
        name='H2', fontName='Helvetica-Bold', fontSize=14,
        textColor=COR_DOURADO, alignment=TA_LEFT,
        spaceBefore=16, spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        name='Texto', fontSize=11, textColor=COR_TEXTO,
        alignment=TA_JUSTIFY, leading=16
    ))
    # Estilos para aspectos
    styles.add(ParagraphStyle(
        name='AspectoBom', fontSize=11, textColor=COR_AZUL,
        alignment=TA_LEFT, leading=14, leftIndent=0.4*cm
    ))
    styles.add(ParagraphStyle(
        name='AspectoTenso', fontSize=11, textColor=COR_RUBI,
        alignment=TA_LEFT, leading=14, leftIndent=0.4*cm
    ))
    styles.add(ParagraphStyle(
        name='AspectoCon', fontSize=11, textColor=COR_DOURADO,
        alignment=TA_LEFT, leading=14, leftIndent=0.4*cm
    ))
    # Rodapé
    styles.add(ParagraphStyle(
        name='Footer', fontSize=9, textColor=colors.grey,
        alignment=TA_CENTER, spaceBefore=40
    ))

    # Fundo para todas as páginas
    def background(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(COR_FUNDO)
        canvas.rect(0, 0, doc.width + doc.leftMargin*2, doc.height + doc.topMargin*2, stroke=0, fill=1)
        canvas.restoreState()

    # --------------------- Capa ------------------------
    # Carrega a logo a partir do mesmo diretório deste arquivo. Isso evita
    # problemas de caminho quando o script é executado de outro diretório.
    logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
    if os.path.exists(logo_path):
        story.append(Image(logo_path, width=5*cm, height=5*cm, hAlign='CENTER'))
        story.append(Spacer(1, 1*cm))
    story.append(Paragraph("Seu Mapa Astral", styles['TituloCapa']))
    story.append(Paragraph(nome, styles['NomeCapa']))
    story.append(Paragraph("Uma Análise da Arquitetura da Sua Alma", styles['SubCapa']))
    story.append(PageBreak())

    # ------------------ Sumário Energético --------------------
    story.append(Paragraph("A Essência do Seu Mapa", styles['H1']))
    story.append(Paragraph(
        "Este relatório apresenta uma interpretação simbólica e profunda do seu mapa astral."
        " A seguir, uma visão do equilíbrio dos quatro elementos e das três modalidades:",
        styles['Texto']
    ))
    story.append(Spacer(1, 0.8*cm))
    elementos = mapa.get('elementos', {})
    modalidades = mapa.get('modalidades', {})
    # Elementos
    story.append(Paragraph("Balanço dos Elementos", styles['H2']))
    story.append(Paragraph(
        f"Fogo: {elementos.get('Fogo', 0)} | Terra: {elementos.get('Terra', 0)} | "
        f"Ar: {elementos.get('Ar', 0)} | Água: {elementos.get('Agua', 0)}",
        styles['Texto']
    ))
    story.append(Spacer(1, 0.4*cm))
    # Modalidades
    story.append(Paragraph("Balanço das Modalidades", styles['H2']))
    story.append(Paragraph(
        f"Cardinal: {modalidades.get('Cardinal', 0)} | Fixo: {modalidades.get('Fixo', 0)} | Mutável: {modalidades.get('Mutavel', 0)}",
        styles['Texto']
    ))
    story.append(PageBreak())

    # ----------------- Tabela de Posições Planetárias --------------------
    story.append(Paragraph("Tabela de Posições Planetárias", styles['H1']))
    # Construção da tabela de posições: cabeçalho e linhas para cada planeta/ponto
    table_data = [["Corpo", "Signo", "Grau", "Minuto", "Casa"]]
    for planeta_id, dados in mapa.get('planetas', {}).items():
        planeta_pt = PLANETA_PT.get(planeta_id, planeta_id)
        signo_pt = SIGNO_PT.get(dados.get('signo'), dados.get('signo'))
        grau = dados.get('grau', 0)
        minuto = dados.get('minuto', 0)
        casa = dados.get('casa', 0)
        table_data.append([
            planeta_pt, signo_pt, str(grau), str(minuto), str(casa)
        ])
    # Estiliza a tabela: largura das colunas e cores do cabeçalho e linhas
    pos_tbl = Table(table_data, colWidths=[5*cm, 4*cm, 2*cm, 2*cm, 2*cm])
    pos_tbl.setStyle(TableStyle([
        # Cabeçalho com fundo dourado e texto escuro
        ('BACKGROUND', (0, 0), (-1, 0), COR_DOURADO),
        ('TEXTCOLOR', (0, 0), (-1, 0), COR_FUNDO),
        # Linhas de dados com fundo azul escuro e texto claro
        ('BACKGROUND', (0, 1), (-1, -1), COR_LINHA),
        ('TEXTCOLOR', (0, 1), (-1, -1), COR_TEXTO),
        # Alinhamento central para todas as células
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        # Grelha interna e borda externa com dourado
        ('INNERGRID', (0, 0), (-1, -1), 0.25, COR_DOURADO),
        ('BOX', (0, 0), (-1, -1), 0.25, COR_DOURADO),
    ]))
    story.append(pos_tbl)
    story.append(PageBreak())

    # ----------------- Análise Planetária Integrada --------------------
    story.append(Paragraph("Análise Planetária Integrada", styles['H1']))
    for planeta_id, dados in mapa.get('planetas', {}).items():
        story.append(Paragraph(interpretar_planeta(planeta_id, dados), styles['Texto']))
        story.append(Spacer(1, 0.6*cm))
    story.append(PageBreak())

    # ------------------ Seção de Aspectos ---------------------
    aspectos = mapa.get('aspectos', [])
    if aspectos:
        story.append(Paragraph("A Dança dos Planetas: Aspectos", styles['H1']))
        # Tabela (aspectarium) mostrando todos os aspectos
        aspect_table_data = [["Planeta 1", "Aspecto", "Planeta 2"]]
        for asp in aspectos:
            p1_pt = PLANETA_PT.get(asp.get('planeta1'), asp.get('planeta1'))
            p2_pt = PLANETA_PT.get(asp.get('planeta2'), asp.get('planeta2'))
            asp_name = ASPECTO_NOME.get(asp.get('aspecto'), asp.get('aspecto'))
            aspect_table_data.append([p1_pt, asp_name, p2_pt])
        aspect_tbl = Table(aspect_table_data, colWidths=[5*cm, 3*cm, 5*cm])
        aspect_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), COR_DOURADO),
            ('TEXTCOLOR', (0, 0), (-1, 0), COR_FUNDO),
            ('BACKGROUND', (0, 1), (-1, -1), COR_LINHA),
            ('TEXTCOLOR', (0, 1), (-1, -1), COR_TEXTO),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, COR_DOURADO),
            ('BOX', (0, 0), (-1, -1), 0.25, COR_DOURADO),
        ]))
        story.append(aspect_tbl)
        story.append(Spacer(1, 0.6*cm))
        # Agora apresentamos os aspectos categorizados com interpretações
        harmoniosos, desafiadores, fusoes = [], [], []
        for asp in aspectos:
            if asp.get('aspecto') in ['TRI', 'SEX']:
                harmoniosos.append(asp)
            elif asp.get('aspecto') in ['SQR', 'OPP']:
                desafiadores.append(asp)
            else:
                fusoes.append(asp)
        if harmoniosos:
            story.append(Paragraph("Aspectos Harmoniosos", styles['H2']))
            for asp in harmoniosos:
                story.append(Paragraph(interpretar_aspecto(asp), styles['AspectoBom']))
            story.append(Spacer(1, 0.4*cm))
        if desafiadores:
            story.append(Paragraph("Aspectos Desafiadores", styles['H2']))
            for asp in desafiadores:
                story.append(Paragraph(interpretar_aspecto(asp), styles['AspectoTenso']))
            story.append(Spacer(1, 0.4*cm))
        if fusoes:
            story.append(Paragraph("Aspectos de Fusão", styles['H2']))
            for asp in fusoes:
                story.append(Paragraph(interpretar_aspecto(asp), styles['AspectoCon']))
            story.append(Spacer(1, 0.4*cm))
        story.append(PageBreak())

    # ------------------ Página do Signo Solar ---------------------
    # Recupera o signo solar do mapa
    try:
        sun_data = mapa.get('planetas', {}).get('Sun', {})
        sun_sign_en = sun_data.get('signo')
    except Exception:
        sun_sign_en = None
    if sun_sign_en and sun_sign_en in SIGNO_IMAGE:
        signo_pt = SIGNO_PT.get(sun_sign_en, sun_sign_en)
        img_file = SIGNO_IMAGE.get(sun_sign_en)
        # Caminho absoluto para a imagem do signo
        img_path = os.path.join(os.path.dirname(__file__), img_file)
        # Construir slug para link (nome do arquivo sem extensão em minúsculas)
        slug = os.path.splitext(img_file)[0].lower()
        link = f"https://caveiradiadema.github.io/verba-site/{slug}.html"
        # Título da seção
        story.append(Paragraph("O Quadro do Seu Signo Solar", styles['H1']))
        # Frase introdutória sobre o quadro
        story.append(Paragraph(
            f"Visite nosso site para adquirir o quadro de <b>{signo_pt}</b>:",
            styles['Texto']
        ))
        # Link em um parágrafo separado, para melhor legibilidade
        story.append(Paragraph(
            f"<link href='{link}' color='{COR_AZUL.hexval()}'><u>{link}</u></link>",
            styles['Texto']
        ))
        # Adiciona a imagem se existir
        if os.path.exists(img_path):
            story.append(Spacer(1, 0.6*cm))
            story.append(Image(img_path, width=10*cm, height=10*cm, hAlign='CENTER'))
        story.append(PageBreak())

    # ------------------ Conclusão e Rodapé ----------------------
    story.append(Paragraph(
        "Este mapa foi gerado com as bibliotecas flatlib, geopy e reportlab."
        " As interpretações aqui apresentadas são gerais e destinam-se a servir como guia de autoconhecimento.",
        styles['Footer']
    ))
    story.append(Paragraph("VERBA Astrologia", styles['Footer']))

    # Gera o PDF com o fundo aplicado em todas as páginas
    print("[DEBUG pdf.py] Gerando o arquivo PDF...")
    doc.build(story, onFirstPage=background, onLaterPages=background)
    print("[DEBUG pdf.py] PDF gerado com sucesso.")