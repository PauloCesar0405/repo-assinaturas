#!/usr/bin/env python3
"""
Cadastro dos titulares das assinaturas. É a ÚNICA fonte de dados pessoais:
os geradores leem daqui, nada de constante espalhada dentro do código.

Para adicionar alguém, acrescente uma entrada e rode:
    python3 build.py <slug>

Campos:
  nome      como sai no card (Ubuntu Bold 50) - cabe até ~23 caracteres
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
            bordas da imagem: o gerador preenche com transparência.
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
}


def pega(slug):
    """Devolve o dicionário da pessoa ou erra com a lista de slugs válidos."""
    if slug not in PESSOAS:
        raise SystemExit(
            f"ABORTADO: slug '{slug}' não está em pessoas.py.\n"
            f"  Conhecidos: {', '.join(sorted(PESSOAS))}"
        )
    return PESSOAS[slug]
