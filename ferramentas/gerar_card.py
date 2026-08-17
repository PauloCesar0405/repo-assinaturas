#!/usr/bin/env python3
"""
Assinatura em card escuro - Time Forte (versao compacta, sem padrao de fundo).

Pecas (empilhadas pelo HTML, lendo-se como um card unico):
  card-topo.png       foto, nome, cargo (2x, estatico)          600x145
  [contatos]          IMAGEM + mapa de cliques (ver gerar_contatos.py) 600x48
  faixa-marcas.gif    Time Forte fixo + marcas deslizando (1x)  600x38
  barra-chamada.png   site em Audiowide (2x)                    600x36

Os tamanhos acima sao os EXIBIDOS; os PNGs sao renderizados em 2x. Os
contatos NAO sao texto HTML - texto encolhia no celular e o dark mode
clareava o fundo. Nao reintroduza (ver CLAUDE.md, "Historico de decisoes").

Manual: 1.9 PRETO #201E1E | LARANJA #F58634  -  1.10 Audiowide + Ubuntu
"""
import math
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFont

LARANJA = (245, 134, 52)
PRETO = (32, 30, 30)
BRANCO = (255, 255, 255)

W, HG = 1200, 290          # card 2x (exibido 600x145)
CARD_TOP = 6
RAIO, BORDA = 18, 4
X = 500

# dados do titular (ao clonar para outra pessoa, troque aqui)
NOME = "Rafael Serra"
CARGO = "CEO"

UP = os.path.join(BASE, "insumos") + os.sep
UBUNTU_B, UBUNTU_R = "Ubuntu-Bold.ttf", "Ubuntu-Regular.ttf"
AUDIOWIDE = "Audiowide-Regular.ttf"

MARCAS = [
    ("flamengo__1_.webp", False),
    ("chelseathebluesacademybrasil.webp", True),
    ("realmadrid.webp", False),
    ("inter.webp", False),
    ("sport.webp", False),
    ("eeflamengo.webp", False),
]


def fonte(arq, tam):
    return ImageFont.truetype(os.path.join(BASE, "fontes", arq), tam)


def texto_espacado(d, xy, txt, fnt, cor, tracking=0):
    x, y = xy
    for ch in txt:
        d.text((x, y), ch, font=fnt, fill=cor)
        x += d.textlength(ch, font=fnt) + tracking
    return x


def largura_espacada(d, txt, fnt, tracking=0):
    return sum(d.textlength(c, font=fnt) + tracking for c in txt) - tracking


def abrir_marca(nome, tirar_preto=False):
    im = Image.open(UP + nome).convert("RGBA")
    if tirar_preto:
        a = np.array(im)
        a[:, :, 3] = np.where(a[:, :, :3].max(axis=2) < 14, 0, a[:, :, 3])
        im = Image.fromarray(a)
    a = np.array(im)
    ys, xs = np.where(a[:, :, 3] > 20)
    return im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


def encaixar(im, mw, mh):
    e = min(mw / im.width, mh / im.height)
    return im.resize((max(1, round(im.width * e)), max(1, round(im.height * e))), Image.LANCZOS)


# ------------------------------------------------------------------ card 2x
def card_topo():
    """Nova abordagem para a foto: painel laranja em gradiente ocupando a
    esquerda do card, com a borda direita inclinada nos 14.7 graus do
    logotipo (medidos no glifo I). A foto vive DENTRO do painel, cortada
    seca nas bordas - sem fades - como um card de atleta."""
    tela = Image.new("RGBA", (W, HG), (255, 255, 255, 255))
    d = ImageDraw.Draw(tela)

    d.rounded_rectangle((0, CARD_TOP, W - 1, HG + 40), radius=RAIO,
                        fill=PRETO + (255,), outline=LARANJA + (255,), width=BORDA)

    # ---- painel laranja inclinado
    ANG = 14.7
    P_TOP, P_BASE = CARD_TOP + 4, HG - 14
    X_TOPO = 424
    desl = math.tan(math.radians(ANG)) * (P_BASE - P_TOP)
    mask = Image.new("L", (W, HG), 0)
    dm = ImageDraw.Draw(mask)
    dm.rounded_rectangle((4, P_TOP, 300, P_BASE), radius=14, fill=255)
    dm.polygon([(150, P_TOP), (X_TOPO, P_TOP),
                (round(X_TOPO - desl), P_BASE), (150, P_BASE)], fill=255)

    g0, g1 = np.array(LARANJA, np.float32), np.array((211, 102, 32), np.float32)
    t = np.linspace(0, 1, HG)[:, None, None]
    grad = np.tile((g0 * (1 - t) + g1 * t), (1, W, 1))
    painel = Image.fromarray(grad.astype(np.uint8)).convert("RGBA")
    painel.putalpha(mask)
    tela.alpha_composite(painel)

    # ---- foto: preenche o painel de ponta a ponta, cortes secos
    foto = Image.open(os.path.join(BASE, "insumos", "recorte-limpo.png")).convert("RGBA").crop((132, 14, 545, 336))
    ESC = (P_BASE - P_TOP) / foto.height
    foto = foto.resize((round(foto.width * ESC), round(foto.height * ESC)), Image.LANCZOS)
    tela.alpha_composite(foto, (26, P_TOP))

    d = ImageDraw.Draw(tela)
    f_nome, f_cargo = fonte(UBUNTU_B, 50), fonte(UBUNTU_B, 21)

    # estouro de largura: nome composto ou cargo longo sairiam por cima da
    # borda laranja. Aborta em vez de publicar um card cortado - depois de
    # publicado, em v1/, so se conserta criando v2/.
    limite = W - BORDA - 8
    for rotulo, fim in (
        ("nome", X + d.textlength(NOME, font=f_nome)),
        ("cargo", X + largura_espacada(d, CARGO, f_cargo, 7)),
    ):
        if fim > limite:
            sys.exit(
                f"ABORTADO: o {rotulo} nao cabe no card "
                f"({round(fim / 2)}px de {round(limite / 2)}px uteis).\n"
                "  Encurte o texto ou reduza o corpo da fonte antes de gerar."
            )

    d.text((X, 92), NOME, font=f_nome, fill=BRANCO + (255,))
    texto_espacado(d, (X, 162), CARGO, f_cargo, LARANJA + (255,), 7)
    d.rectangle((X, 212, X + 56, 217), fill=LARANJA + (255,))

    alvo = os.path.join(BASE, "card-topo.png")
    tela.convert("RGB").save(alvo, optimize=True)
    print(f"card-topo.png        {W}x{HG} (exibido {W//2}x{HG//2}), "
          f"{os.path.getsize(alvo)/1024:.0f} KB")


# ------------------------------------------------------- faixa deslizante 1x
def faixa_marcas(alt_logo=20, gap=32, passo=5, dur_ms=90, cores=32):
    WB, HB = 600, 38
    R2 = 9

    pecas = [encaixar(abrir_marca(n, p), 170, alt_logo) for n, p in MARCAS]
    S = sum(p.width + gap for p in pecas)
    fita = Image.new("RGBA", (S, alt_logo), (0, 0, 0, 0))
    x = gap // 2
    for p in pecas:
        fita.alpha_composite(p, (x, (alt_logo - p.height) // 2))
        x += p.width + gap

    base = Image.new("RGB", (WB, HB), BRANCO)
    d = ImageDraw.Draw(base)
    d.rounded_rectangle((0, -30, WB - 1, HB - 1), radius=R2,
                        fill=PRETO, outline=LARANJA, width=2)
    tf = encaixar(abrir_marca("timeforte_monocromatico_laranja.png"), 200, 20)
    base.paste(tf, (18, (HB - tf.height) // 2 - 1), tf)
    div_x = 18 + tf.width + 16
    d.line((div_x, 9, div_x, HB - 10), fill=LARANJA, width=1)

    jan_x0, jan_x1 = div_x + 16, WB - 12
    m = np.zeros((HB, WB), np.float32)
    m[:, jan_x0:jan_x1] = 1
    FADE = 15
    m[:, jan_x0:jan_x0 + FADE] *= np.linspace(0, 1, FADE)[None, :]
    m[:, jan_x1 - FADE:jan_x1] *= np.linspace(1, 0, FADE)[None, :]
    janela = Image.fromarray((m * 255).astype(np.uint8))

    N = max(2, round(S / passo))
    y = (HB - alt_logo) // 2
    frames = []
    for i in range(N):
        off = round(i * S / N) % S
        f = base.copy()
        camada = Image.new("RGBA", (WB, HB), (0, 0, 0, 0))
        for k in range(-1, WB // S + 2):
            camada.alpha_composite(fita, (jan_x0 - off + k * S, y))
        f.paste(camada, (0, 0), ImageChops.multiply(camada.getchannel("A"), janela))
        frames.append(f)

    tira = Image.new("RGB", (WB, HB * len(frames)))
    for i, f in enumerate(frames):
        tira.paste(f, (0, i * HB))
    pal = tira.quantize(colors=cores, method=Image.MEDIANCUT)
    fp = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in frames]

    for xy, alvo in (((300, 3), PRETO), ((0, 19), LARANJA), ((WB - 1, HB - 1), BRANCO)):
        idx = fp[0].getpixel(xy)
        for f in fp:
            pp = f.getpalette()
            pp[3 * idx:3 * idx + 3] = list(alvo)
            f.putpalette(pp)

    alvo = os.path.join(BASE, "faixa-marcas.gif")
    fp[0].save(alvo, save_all=True, append_images=fp[1:],
               duration=[dur_ms] * len(fp), loop=0, optimize=True, disposal=1)

    chk = fp[0].convert("RGB")
    print(f"faixa-marcas.gif     {WB}x{HB}, {len(fp)} frames, "
          f"{1000*passo/dur_ms:.0f} px/s, "
          f"{os.path.getsize(alvo)/1024:.0f} KB  "
          f"[fundo={chk.getpixel((300, 3))} borda={chk.getpixel((0, 21))} "
          f"canto={chk.getpixel((WB - 1, HB - 1))}]")


# ------------------------------------------------------------------ barra 2x
def barra():
    HB = 72
    im = Image.new("RGB", (W, HB), BRANCO)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, W - 1, HB - 1), radius=RAIO, fill=LARANJA)

    f2 = fonte(AUDIOWIDE, 27)
    l2 = "WWW.TIMEFORTE.COM"
    bb = d.textbbox((0, 0), "W", font=f2)
    y2 = (HB - (bb[3] - bb[1])) // 2 - bb[1]
    x2 = (W - largura_espacada(d, l2, f2, 2.0)) / 2
    texto_espacado(d, (x2, y2), l2, f2, PRETO, 2.0)

    alvo = os.path.join(BASE, "barra-chamada.png")
    im.save(alvo, optimize=True)
    print(f"barra-chamada.png    {W}x{HB} (exibido {W//2}x{HB//2}), "
          f"{os.path.getsize(alvo)/1024:.0f} KB")


if __name__ == "__main__":
    card_topo()
    faixa_marcas()
    barra()
