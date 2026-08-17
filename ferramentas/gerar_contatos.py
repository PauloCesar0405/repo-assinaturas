#!/usr/bin/env python3
"""
Gera a faixa de contatos como IMAGEM (o unico pedaco de texto que sobrava na
assinatura e que encolhia no celular). Vira PNG 2x, imune ao dark mode, e
devolve as coordenadas de cada trecho para o mapa de cliques do HTML.

Layout: telefone  •  e-mail   (linha 1, dentro do card escuro, coluna a 250)
        endereco                (linha 2)

Destinos do mapa (definidos pelo usuario):
  telefone  -> WhatsApp
  e-mail    -> mailto
  endereco  -> Google Maps
  resto     -> site

Uso:
    python3 gerar_contatos.py [slug] [--forcar]

O slug nomeia a saida: v1/pessoas/<slug>-contatos.png. Se o arquivo ja
existir, o script ABORTA - peca publicada em v1/ e imutavel (regra 1 do
CLAUDE.md). Use --forcar so quando o arquivo ainda nao tiver sido publicado.
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
LARANJA = (245, 134, 52)
PRETO = (32, 30, 30)
BRANCO = (255, 255, 255)
CINZA = (176, 171, 169)

WD = 600            # largura exibida
ESC = 2             # render em 2x
W = WD * ESC
PADL = 250 * ESC    # coluna alinhada ao nome do card
PADR = 20 * ESC

SLUG = "rafael-serra"   # sobrescrito por argv[1]; nomeia <slug>-contatos.png
TEL = "+55 21 98124-6506"
EMAIL = "rafael@timeforte.com"
END = "R. Bar\u00e3o de Ipanema, 56/301 \u2014 Copacabana, Rio de Janeiro/RJ"


def fonte(arq, tam):
    return ImageFont.truetype(os.path.join(BASE, "fontes", arq), tam)


def main():
    slug, forcar = SLUG, False
    for arg in sys.argv[1:]:
        if arg == "--forcar":
            forcar = True
        else:
            slug = arg

    saida = os.path.join(BASE, "..", "v1", "pessoas", f"{slug}-contatos.png")
    if os.path.exists(saida) and not forcar:
        sys.exit(
            f"ABORTADO: {os.path.normpath(saida)} ja existe.\n"
            "  Peca em v1/ e imutavel depois de publicada (regra 1 do CLAUDE.md):\n"
            "  e-mails ja enviados apontam para essa URL. Arte nova entra como v2/.\n"
            "  Se este arquivo ainda NAO foi publicado, repita com --forcar."
        )

    f1 = fonte("Ubuntu-Regular.ttf", 14 * ESC)
    f2 = fonte("Ubuntu-Regular.ttf", 11 * ESC)

    pad_top, gap12, pad_bot = 8 * ESC, 4 * ESC, 8 * ESC
    h1 = f1.getbbox("Xg")[3]
    h2 = f2.getbbox("Xg")[3]
    H = pad_top + h1 + gap12 + h2 + pad_bot

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
    d.text((x_bullet, y1), "\u2022", font=f1, fill=LARANJA)
    x_email = x_bullet + d.textlength("\u2022", font=f1) + 6 * ESC
    d.text((x_email, y1), EMAIL, font=f1, fill=BRANCO)
    x_email_fim = x_email + d.textlength(EMAIL, font=f1)

    # ---- linha 2: endereco
    y2 = y1 + h1 + gap12
    d.text((PADL, y2), END, font=f2, fill=CINZA)
    x_end_fim = PADL + d.textlength(END, font=f2)

    # ---- estouro de largura: nome/e-mail longos sairiam por cima do filete
    # laranja e o mapa de cliques ganharia coords fora da imagem. Aborta em vez
    # de publicar uma peca cortada (em v1/ isso so se conserta criando v2/).
    limite = W - PADR
    for rotulo, fim in (("e-mail", x_email_fim), ("endereco", x_end_fim)):
        if fim > limite:
            sys.exit(
                f"ABORTADO: o {rotulo} nao cabe na faixa "
                f"({round(fim / ESC)}px de {round(limite / ESC)}px uteis).\n"
                "  Encurte o texto ou reduza o corpo da fonte antes de gerar."
            )

    im.save(saida, optimize=True)

    # ---- coordenadas do mapa, em px EXIBIDOS (divide por ESC)
    def cx(v):
        return round(v / ESC)

    coords = {
        "telefone": [cx(PADL) - 2, cx(y1) - 2, cx(x_tel_fim) + 2, cx(y1 + h1) + 2],
        "email":    [cx(x_email) - 2, cx(y1) - 2, cx(x_email_fim) + 2, cx(y1 + h1) + 2],
        "endereco": [cx(PADL) - 2, cx(y2) - 2, cx(x_end_fim) + 2, cx(y2 + h2) + 2],
        "wd": WD, "h": cx(H),
    }
    print(json.dumps(coords))


if __name__ == "__main__":
    main()
