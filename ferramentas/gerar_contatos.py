#!/usr/bin/env python3
"""
Gera a faixa de contatos como IMAGEM (o unico pedaco de texto que sobrava na
assinatura e que encolhia no celular). Vira PNG 2x, imune ao dark mode.

Layout: telefone  •  e-mail   (linha 1, dentro do card escuro, coluna a 250)
        endereco                (linha 2)

POR QUE FATIAS, e nao um <map>:
  A primeira versao era uma imagem unica + <map>/<area>. Funciona ao abrir o
  HTML no navegador, mas NAO sobrevive a instalacao: o fluxo e "abrir no
  Chrome, Ctrl+A/Ctrl+C, colar no editor de assinatura do Gmail", e o <map>
  se perde nesse caminho - a <img> chega com usemap apontando para um mapa
  que nao existe mais, e nenhuma regiao fica clicavel. Alem disso o Gmail
  reescala a imagem da assinatura, o que desalinha coordenadas de <area>.
  Fatia + <a> em volta e o que ja funciona no card e na barra: sobrevive ao
  copiar-colar, ao Gmail, ao Outlook e ao celular - inclusive onde <map> e
  ignorado.

Saidas em v1/pessoas/ (todas 2x):
  <slug>-contatos.png        faixa inteira (compatibilidade; nao usada no HTML novo)
  <slug>-contatos-tel.png    linha 1, esquerda  -> WhatsApp
  <slug>-contatos-email.png  linha 1, direita   -> mailto
  <slug>-contatos-end.png    linha 2, inteira   -> Google Maps

O corte vertical cai no vazio preto entre o telefone e o bullet, e o corte
horizontal no vazio entre as duas linhas - nenhuma letra e cortada. A altura
total e forcada a PAR para que a imagem exibida em 1x tenha altura inteira:
altura fracionaria (48,5px) e o que produzia a faixa branca de meio pixel
entre os contatos e a faixa de marcas.

Uso:
    python3 gerar_contatos.py [slug] [--forcar]

Sem --forcar, arquivo que ja existe em v1/ e PULADO, nunca sobrescrito
(regra 1 do CLAUDE.md: e-mails ja enviados apontam para essas URLs).
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
PESSOAS = os.path.join(BASE, "..", "v1", "pessoas")
LARANJA = (245, 134, 52)
PRETO = (32, 30, 30)
BRANCO = (255, 255, 255)
CINZA = (176, 171, 169)

WD = 600            # largura exibida
ESC = 2             # render em 2x
W = WD * ESC
PADL = 250 * ESC    # coluna alinhada ao nome do card
PADR = 20 * ESC

SLUG = "rafael-serra"   # sobrescrito por argv[1]; nomeia as pecas
TEL = "+55 21 98124-6506"
EMAIL = "rafael@timeforte.com"
END = "R. Barão de Ipanema, 56/301 — Copacabana, Rio de Janeiro/RJ"


def fonte(arq, tam):
    return ImageFont.truetype(os.path.join(BASE, "fontes", arq), tam)


def par(v):
    """Arredonda para cima ate um numero par: em 2x, so largura/altura par
    resulta em dimensao inteira na imagem exibida."""
    v = int(v)
    return v + (v % 2)


def main():
    slug, forcar = SLUG, False
    for arg in sys.argv[1:]:
        if arg == "--forcar":
            forcar = True
        else:
            slug = arg

    f1 = fonte("Ubuntu-Regular.ttf", 14 * ESC)
    f2 = fonte("Ubuntu-Regular.ttf", 11 * ESC)

    pad_top, gap12, pad_bot = 8 * ESC, 4 * ESC, 8 * ESC
    h1 = f1.getbbox("Xg")[3]
    h2 = f2.getbbox("Xg")[3]
    H = par(pad_top + h1 + gap12 + h2 + pad_bot)

    im = Image.new("RGB", (W, H), PRETO)
    d = ImageDraw.Draw(im)
    # filetes laterais laranja, continuando a moldura do card
    d.rectangle((0, 0, 2 * ESC - 1, H), fill=LARANJA)
    d.rectangle((W - 2 * ESC, 0, W - 1, H), fill=LARANJA)

    # ---- linha 1: telefone  •  e-mail
    y1 = pad_top
    x = PADL
    d.text((x, y1), TEL, font=f1, fill=BRANCO)
    x_tel_fim = x + d.textlength(TEL, font=f1)
    x_bullet = x_tel_fim + 6 * ESC
    d.text((x_bullet, y1), "•", font=f1, fill=LARANJA)
    x_email = x_bullet + d.textlength("•", font=f1) + 6 * ESC
    d.text((x_email, y1), EMAIL, font=f1, fill=BRANCO)
    x_email_fim = x_email + d.textlength(EMAIL, font=f1)

    # ---- linha 2: endereco
    y2 = y1 + h1 + gap12
    d.text((PADL, y2), END, font=f2, fill=CINZA)
    x_end_fim = PADL + d.textlength(END, font=f2)

    # ---- estouro de largura: e-mail/endereco longos sairiam por cima do
    # filete laranja. Aborta em vez de publicar uma peca cortada (em v1/ isso
    # so se conserta criando v2/).
    limite = W - PADR
    for rotulo, fim in (("e-mail", x_email_fim), ("endereco", x_end_fim)):
        if fim > limite:
            sys.exit(
                f"ABORTADO: o {rotulo} nao cabe na faixa "
                f"({round(fim / ESC)}px de {round(limite / ESC)}px uteis).\n"
                "  Encurte o texto ou reduza o corpo da fonte antes de gerar."
            )

    # ---- cortes, ambos em area preta vazia (nenhuma letra e cortada)
    corte_x = par((x_tel_fim + x_bullet) / 2)   # entre o telefone e o bullet
    corte_y = par(y1 + h1 + gap12 / 2)          # entre as duas linhas

    pecas = {
        f"{slug}-contatos.png":       im,
        f"{slug}-contatos-tel.png":   im.crop((0, 0, corte_x, corte_y)),
        f"{slug}-contatos-email.png": im.crop((corte_x, 0, W, corte_y)),
        f"{slug}-contatos-end.png":   im.crop((0, corte_y, W, H)),
    }

    salvos, pulados = {}, []
    for nome, peca in pecas.items():
        alvo = os.path.join(PESSOAS, nome)
        if os.path.exists(alvo) and not forcar:
            pulados.append(nome)
            continue
        peca.save(alvo, optimize=True)
        salvos[nome] = [peca.width // ESC, peca.height // ESC]

    if pulados:
        print(
            "AVISO: peca(s) ja existente(s) em v1/ NAO foram sobrescritas "
            f"(regra 1): {', '.join(pulados)}",
            file=sys.stderr,
        )

    # dimensoes EXIBIDAS de cada fatia, para montar o HTML
    print(json.dumps({
        "salvos": salvos,
        "pulados": pulados,
        "faixa": [WD, H // ESC],
    }))


if __name__ == "__main__":
    main()
