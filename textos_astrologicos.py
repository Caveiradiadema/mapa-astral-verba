# textos_astrologicos.py  –  banco de textos em PT-BR
# ==================================================

# ───── INTRO & METÁFORA ──────────────────────────────────────────
INTRO_METAFORA = (
    "Seu mapa astral é uma fotografia do céu no exato momento em que você nasceu. "
    "Ele não dita o destino; revela potenciais, talentos e desafios — a verdadeira arquitetura da sua alma."
)

COMO_LER = (
    "Pense no seu mapa como um Teatro da Vida:<br/><br/>"
    "• <b>Planetas</b> = Atores (partes da personalidade)<br/>"
    "• <b>Signos</b>   = Figurinos (como os atores se expressam)<br/>"
    "• <b>Casas</b>    = Palcos (as áreas da vida onde a ação acontece)<br/>"
    "• <b>Aspectos</b> = O Roteiro (as conversas e interações entre os atores)"
)

# ───── BIG THREE (Sol / Lua / Asc) ─────────────────────────────
TEXTO_SOL = {
    "Gêmeos": "Com Sol em Gêmeos, sua identidade central é curiosa, comunicativa e versátil. Sua energia vital floresce quando você aprende, ensina, troca ideias e se conecta com pessoas e ambientes diversos. Você é um eterno aprendiz com uma mente ágil e adaptável.",
    # Adicione aqui os textos para os outros 11 signos solares
    "Áries": "Com Sol em Áries, sua identidade é marcada pela coragem, pioneirismo e uma imensa energia para começar projetos. Sua força vital se renova com desafios e ação.",
    "Touro": "Com Sol em Touro, sua essência busca segurança, estabilidade e o prazer das coisas boas da vida. Sua força vem da sua determinação e lealdade.",
}
TEXTO_LUA = {
    "Virgem":  "Sua Lua em Virgem revela que você encontra segurança emocional na ordem, na rotina e no sentimento de ser útil. Você processa suas emoções de forma analítica e prática, e se sente nutrido ao cuidar dos detalhes do dia a dia e ajudar os outros de maneira concreta.",
    # Adicione aqui os textos para as outras 11 posições da Lua
}
TEXTO_ASC = {
    "Câncer":  "Com Ascendente em Câncer, você se apresenta ao mundo de uma forma sensível, protetora e um tanto reservada. A primeira impressão que você causa é a de alguém cuidadoso e com forte intuição. Sua jornada envolve aprender a nutrir a si mesmo e aos outros, e a lidar com sua profunda sensibilidade.",
    # Adicione aqui os textos para os outros 11 ascendentes
}

# ───── TEXTOS DOS ASPECTOS ──────────────────────────────────
# A chave é "ID_PLANETA1-ID_PLANETA2-tipo_em_ingles"
# Ex: "Sun-Mars-square"
TEXTOS_ASPECTOS = {
    "Sun-Mars-square": "Essa quadratura cria uma tensão dinâmica entre sua identidade (Sol) e sua forma de agir (Marte). Pode haver uma tendência a ser impaciente ou competitivo. O desafio é aprender a canalizar sua imensa energia e assertividade de forma construtiva, sem entrar em conflitos desnecessários.",
    "Sun-Jupiter-square": "Aqui, sua identidade (Sol) entra em conflito com seu desejo de expansão (Júpiter). Isso pode levar a um excesso de otimismo, promessas exageradas ou uma busca incessante por 'mais'. O crescimento vem ao encontrar um equilíbrio saudável entre a autoconfiança e a realidade prática.",
    "Moon-Saturn-conjunction": "Suas emoções (Lua) se fundem com o princípio da estrutura e da responsabilidade (Saturno). Você pode ser emocionalmente reservado e levar seus sentimentos muito a sério. Essa posição confere grande maturidade emocional e resiliência, embora possa indicar uma certa dificuldade em simplesmente relaxar e se permitir sentir.",
    "Moon-Uranus-sextile": "Suas emoções (Lua) e sua necessidade de originalidade (Urano) colaboram harmoniosamente. Isso te dá uma intuição rápida e uma mente aberta a novas ideias e pessoas. Você se sente bem em ambientes que permitem liberdade emocional e não tem medo de ser diferente.",
    "Moon-Neptune-square": "Há uma tensão entre suas necessidades emocionais (Lua) e sua sensibilidade espiritual ou artística (Netuno). Você pode ser extremamente empático, a ponto de absorver as emoções alheias, ou ter dificuldade em separar a realidade da fantasia. Aprender a colocar limites emocionais saudáveis é fundamental.",
    "Venus-Jupiter-sextile": "Seu poder de atração (Vênus) e sua capacidade de expansão (Júpiter) trabalham em harmonia. Isso confere generosidade, otimismo nos relacionamentos e um gosto pelo belo e pelo prazer. É um aspecto que atrai sorte e boas oportunidades sociais e afetivas.",
    "Saturn-Uranus-sextile": "A estrutura (Saturno) e a inovação (Urano) trabalham juntas aqui. Você tem a capacidade única de criar mudanças práticas e duradouras. Sabe reformar o antigo sem destruir suas bases, unindo tradição e progresso de forma genial.",
    "Saturn-Neptune-square": "Uma tensão entre a realidade (Saturno) e o sonho (Netuno). Pode haver medos ou inseguranças que minam sua confiança. O desafio é aprender a construir seus sonhos no mundo real, dando forma prática à sua inspiração sem se perder em desilusões.",
    "Neptune-Pluto-sextile": "Um aspecto geracional que conecta a espiritualidade (Netuno) com o poder de transformação (Plutão). Em nível pessoal, isso te dá uma capacidade intuitiva de perceber as correntes ocultas da sociedade e de usar essa percepção para promover curas e mudanças profundas."
}