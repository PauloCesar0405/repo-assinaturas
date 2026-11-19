#!/usr/bin/env python3
"""
Cadastro dos titulares das assinaturas. É a ÚNICA fonte de dados pessoais:
os geradores leem daqui, nada de constante espalhada dentro do código.

Para adicionar alguém, acrescente uma entrada e rode:
    python3 build.py <slug>

Campos:
  nome      como sai no card (Ubuntu Bold 50) - cabe até ~23 caracteres;
            mais longo encolhe o corpo até 44 antes de abortar
  cargo     como sai no card, em CAIXA ALTA   - cabe até ~24 caracteres
  tel       telefone como TEXTO na faixa de contatos
  whatsapp  só dígitos, com DDI, para montar o link wa.me
  email     endereço real; divide a linha 1 com o telefone, então é o campo
            mais apertado - com o telefone atual sobram ~191px, o que exclui
            padrões longos como nome.sobrenome@timeforte.com
  endereco  como sai na linha 2
  maps      link do Google Maps do endereço
  foto      arquivo em insumos/, PNG RGBA com fundo já removido
  crop      (x0, y0, x1, y1) na foto. Proporção ~1.283 (largura/altura) para
            encher o painel laranja sem sobrar nem vazar. Pode ultrapassar as
            bordas da imagem: o gerador preenche com transparência. Mais
            largo que 1.283, a sobra passa por baixo da diagonal (o painel
            recorta a foto) - para esconder cabelo ou ombro que encoste na
            borda direita da foto.
  espelhar  True inverte a foto na horizontal (para o olhar apontar ao nome)

Os geradores abortam se nome, cargo, e-mail ou endereço não couberem - nunca
publicam peça cortada.
"""

ENDERECO_SEDE = "R. Barão de Ipanema, 56/301 — Copacabana, Rio de Janeiro/RJ"
MAPS_SEDE = ("https://maps.google.com/?q=R.+Bar%C3%A3o+de+Ipanema,+56,"
             "+Copacabana,+Rio+de+Janeiro")

PESSOAS = {
    "rafael-serra": {
        "nome": "Rafael Serra",
        "cargo": "CEO",
        "tel": "+55 21 98124-6506",
        "whatsapp": "5521981246506",
        "email": "rafael@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "recorte-limpo.png",
        "crop": (132, 14, 545, 336),
        "espelhar": False,
    },
    "camila-melo": {
        "nome": "Camila Melo",
        "cargo": "GERENTE DE OPERAÇÕES",
        "tel": "+55 21 96725-1171",
        "whatsapp": "5521967251171",
        "email": "camila@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "camila-limpo.png",
        # recorte fornecido já sem fundo (327x359). É estreita para a proporção
        # do painel: em altura cheia precisaria de 461px de largura. O crop
        # abaixo estoura as bordas de propósito — o gerador preenche com
        # transparência, que vira o laranja do painel.
        "crop": (-18, 0, 382, 312),
        "espelhar": False,
    },
    "jose-martins": {
        "nome": "José Martins",
        "cargo": "PRESIDENTE E CVO",
        "tel": "+55 21 99955-6207",
        "whatsapp": "5521999556207",
        "email": "zemartins@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "jose-martins-limpo.png",
        # recorte fornecido já sem fundo (401x232). Pessoa centrada em x~189;
        # o crop desce até a borda inferior da foto (corte seco no ombro) e
        # deixa ~22px de respiro acima do cabelo.
        "crop": (55, 22, 324, 232),
        "espelhar": False,
    },
    "cassio-lopes": {
        "nome": "Cássio Lopes",
        "cargo": "DIRETOR DE EXPANSÃO",
        "tel": "+55 21 99181-3831",
        "whatsapp": "5521991813831",
        "email": "cassio@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "cassio-lopes-limpo.png",
        # recorte fornecido já sem fundo (447x558). Foto tem corpo de sobra:
        # o crop enquadra cabeça e ombros da metade de cima, com corte seco
        # no peito, e estoura ~20px nas laterais (viram laranja do painel).
        "crop": (-20, 12, 452, 380),
        "espelhar": False,
    },
    "claudio-calabria": {
        "nome": "Claudio Calabria",
        "cargo": "GERENTE DE PLANEJAMENTO",
        "tel": "+55 21 99150-1531",
        "whatsapp": "5521991501531",
        "email": "claudiocalabria@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "claudio-calabria-limpo.png",
        # recorte fornecido já sem fundo (545x458). Cabeça e ombros com corte
        # seco no peito, rosto centrado em x~275. O e-mail de 29 caracteres é
        # o 1º caso do encolhe-até-caber da linha 1 (ver gerar_contatos.py).
        "crop": (41, 0, 509, 365),
        "espelhar": False,
    },
    "thamerson-fortuna": {
        "nome": "Thamerson Fortuna",
        "cargo": "ANALISTA FINANCEIRO",
        "tel": "+55 21 96718-9010",
        "whatsapp": "5521967189010",
        "email": "thamerson@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "thamerson-fortuna-limpo.png",
        # foto TROCADA em 26/08/2026 (mesmo dia da publicação, ninguém tinha
        # instalado): a 1ª era um perfil de frame de vídeo, espelhado. A nova
        # é frontal, 430x581, já sem fundo; crop de cabeça e ombros com corte
        # seco no peito, estourando as laterais (viram laranja).
        "crop": (-27, -6, 461, 374),
        "espelhar": False,
    },
    "paulo-cesar": {
        "nome": "Paulo Cesar",
        "cargo": "ANALISTA DE TI",
        "tel": "+55 21 96748-2875",
        "whatsapp": "5521967482875",
        "email": "paulocesar@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "paulo-cesar-limpo.png",
        # 2ª foto (18/11/2026 12:11, mais aberta). O PNG do remove.bg vem em
        # resolução de "preview" (461x541) e deixou o card borrado; por isso o
        # recorte é rembg (receita acima) na original 1366x1600, limitado pela
        # silhueta do remove.bg (o rembg deixava luminária e cadeira), sem
        # brilho de luminária no cabelo, com as íris (azuladas pelo filtro de
        # luz azul da lente) de volta ao castanho, reduzido a 683x800. Nada
        # de contraste/nitidez artificiais, e NÃO estenda o casaco para abrir
        # o crop - os dois foram testados na 1ª foto e reprovados.
        "crop": (5, 167, 702, 710),
        "espelhar": False,
    },
    "wagner-queiroz": {
        "nome": "Wagner de Queiroz Junior",
        "cargo": "HEAD DESIGNER",
        "tel": "+55 21 98457-4494",
        "whatsapp": "5521984574494",
        "email": "wagner@tstorm.com.br",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "wagner-queiroz-limpo.png",
        # selfie de 18/11/2026 (original 959x1280). Recorte rembg na original
        # com o alpha limitado pelo do remove.bg (o rembg deixava blocos de
        # parede cinza no cabelo; o remove.bg acerta o cabelo) e a cor dos
        # fios re-estimada sem o cinza (pymatting). Um objeto preto com LED
        # colado no ombro direito foi cortado na linha do ombro. Reduzido a
        # 719x960. A selfie corta os ombros: o crop estoura as laterais.
        "crop": (-90, 120, 808, 820),
        "espelhar": False,
    },
    "fernanda-oliveira": {
        "nome": "Fernanda Oliveira",
        "cargo": "COORDENADORA DE RH",
        "tel": "+55 21 98498-2373",
        "whatsapp": "5521984982373",
        "email": "fernanda@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "fernanda-oliveira-limpo.png",
        # 2ª foto (18/11/2026 16:31, 760x666): a mesma selfie com o quadro
        # ampliado - as laterais (fim do cabelo, mão, ombro) parecem geradas
        # por IA. A 1ª, fechada, deixava cortes retos no cabelo em qualquer
        # crop. Recorte com o birefnet-portrait do rembg (o u2net não vê o
        # cabelo cacheado como pessoa), armação dos óculos tornada opaca e
        # cor dos cachos re-estimada sem o fundo (pymatting), sem redução.
        # Primeira assinatura direto em v2/ (nunca teve v1/).
        "crop": (-10, 15, 670, 545),
        "espelhar": False,
    },
    "natalia-herdy": {
        "nome": "Natália Herdy",
        "cargo": "COORDENADORA DE MARKETING",
        "tel": "+55 21 99375-5404",
        "whatsapp": "5521993755404",
        "email": "natalia@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "natalia-herdy-limpo.png",
        # foto de 18/11/2026 (original 4075x5434, parede branca), reduzida a
        # 1/4 (1018x1358) antes do recorte. birefnet-portrait: segurou a
        # camiseta creme contra a parede branca. Cor dos fios re-estimada
        # sem o branco da parede (pymatting). O cargo, com 25 caracteres,
        # cabe (507 de 594px) - o "~24" da tabela de limites é conservador.
        "crop": (-122, 255, 1033, 1155),
        "espelhar": False,
    },
    "henrique-gomes": {
        "nome": "Henrique Gomes",
        "cargo": "GESTOR DE PROJETO",
        "tel": "+55 21 98071-2522",
        "whatsapp": "5521980712522",
        "email": "henriquegones@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "henrique-gomes-limpo.png",
        # foto de 18/11/2026: PRINT de celular (1170x2532) de uma foto com
        # zoom, em evento - suave, camiseta preta em fundo escuro. Recorte só
        # da faixa y 250-1750 (tira a barra de status), com birefnet-portrait,
        # que separou a camiseta do fundo. Borda clara = o cabelo grisalho,
        # não halo. A foto corta os ombros: o crop estoura as laterais.
        "crop": (-332, 80, 1413, 1440),
        "espelhar": False,
    },
    "beatriz-leal": {
        "nome": "Beatriz Leal da Silva",
        "cargo": "SOCIAL MEDIA",
        "tel": "+55 21 99948-1634",
        "whatsapp": "5521999481634",
        "email": "beatrizleal@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "beatriz-leal-limpo.png",
        # foto de 18/11/2026: só veio o "-removebg-preview" (460x543), sem a
        # original. Exceção à regra do preview porque o crop (488px de largura)
        # não precisa de ampliação para o painel em 2x - conferido no zoom, sem
        # borrar. Borda limpa (luminância 87), uma ilha só, usado sem retoque.
        # A foto corta os ombros: o crop estoura as laterais.
        "crop": (-9, 125, 479, 505),
        "espelhar": False,
    },
    "ronaldo-spinelli": {
        "nome": "Ronaldo Leal Spinelli",
        "cargo": "COORDENADOR TÉCNICO",
        "tel": "+55 21 96409-0243",
        "whatsapp": "5521964090243",
        "email": "naldo@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "ronaldo-spinelli-limpo.png",
        # selfie de 18/11/2026 (original 2556x3408, parede branca), reduzida a
        # 1/3 (852x1136) antes do recorte. birefnet-portrait: segurou o cabelo
        # grisalho curto contra a parede branca; armação dos óculos opaca e cor
        # da borda re-estimada sem o branco (pymatting). Borda clara (lum 144)
        # = cabelo grisalho e pele, não halo.
        "crop": (18, 286, 865, 946),
        "espelhar": False,
    },
    "alessandra-moreira": {
        "nome": "Alessandra Carvalho Moreira",
        "cargo": "COORDENADORA DE LOGÍSTICA",
        "tel": "+55 21 96468-6330",
        "whatsapp": "5521964686330",
        "email": "alessandra@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "alessandra-moreira-limpo.png",
        # foto de 18/11/2026: só veio o "-removebg-preview" (433x577), sem a
        # original; serve pelo mesmo motivo da Beatriz (sem ampliação em 2x).
        # Só tirei 3 pixels soltos. Os cachos encostam na borda direita da
        # foto: o crop é mais largo que 1.283 de propósito, para essa borda
        # cair sob a diagonal (o painel recorta a foto) em vez de virar um
        # corte reto no cabelo. O nome, com 27 caracteres, é o 1º que encolhe
        # (1px a mais em 50 - ver gerar_card.py).
        "crop": (-120, 62, 433, 452),
        "espelhar": False,
    },
    "joao-mauricio": {
        # nome completo (João Mauricio Antunes Monteiro de Souza, 39 ch) não
        # cabe nem no piso de 44; a opção 1 da prévia mandada a ele
        "nome": "João Mauricio Monteiro",
        "cargo": "COORDENADOR DE EVENTOS",
        "tel": "+55 21 99826-2643",
        "whatsapp": "5521998262643",
        "email": "joaomauricio@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "joao-mauricio-limpo.png",
        # 3ª foto (19/11/2026, 1024x1536): a 2ª (painel de evento, com a
        # jaqueta de outra pessoa colada no ombro) ampliada até o corpo
        # inteiro - pelo tamanho e pelo nome do arquivo, por IA; o rosto é o
        # mesmo. A 1ª era de corpo inteiro num palco, inutilizável.
        # birefnet-portrait sem redução. Paulo pediu "do peito pra cima": o
        # crop pega os dois ombros inteiros e corta acima do bordado do peito.
        "crop": (93, 20, 940, 680),
        "espelhar": False,
    },
}


def pega(slug):
    """Devolve o dicionário da pessoa ou erra com a lista de slugs válidos."""
    if slug not in PESSOAS:
        raise SystemExit(
            f"ABORTADO: slug '{slug}' não está em pessoas.py.\n"
            f"  Conhecidos: {', '.join(sorted(PESSOAS))}"
        )
    return PESSOAS[slug]
