#!/usr/bin/env python3
"""
Monta assinaturas-html/<slug>.html a partir de pessoas.py e das peças que já
estão em v1/pessoas/. Mede as fatias no disco - nada de largura digitada na
mão, que era a fonte dos erros (mapa com nome repetido, coords defasadas,
link de outra pessoa).

Uso:
    python3 gerar_html.py <slug>        # um
    python3 gerar_html.py --todos       # todos os de pessoas.py

Estrutura gerada: uma <table> de 4 blocos. Os contatos são 3 fatias, cada
uma no seu <a> - ver o porquê em gerar_contatos.py e no CLAUDE.md.
"""
import html
import os
import sys

from PIL import Image

import pessoas

BASE = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(BASE)
V1 = os.path.join(RAIZ, "v1", "pessoas")
SAIDA = os.path.join(RAIZ, "assinaturas-html")
URL = "https://paulocesar0405.github.io/repo-assinaturas/v1"
SITE = "https://www.timeforte.com"

for _f in (sys.stdout, sys.stderr):
    try:
        _f.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

ESTILO_IMG = ("display: block; border: 0; outline: none; font-family: Arial, "
              "Helvetica, sans-serif; font-size: 12px; line-height: 15px; color: #201E1E;")


def medir(arq):
    """Dimensões EXIBIDAS (as peças são renderizadas em 2x, menos o GIF)."""
    with Image.open(arq) as im:
        e = 1 if arq.endswith(".gif") else 2
        if im.width % e or im.height % e:
            raise SystemExit(f"ABORTADO: {os.path.basename(arq)} tem lado ímpar "
                             f"({im.width}x{im.height}) e não fecha em 1x.")
        return im.width // e, im.height // e


def imagem(src, w, h, alt, href, bloco=True):
    disp = "display: block;" if bloco else "display: inline-block; vertical-align: top;"
    estilo = ESTILO_IMG.replace("display: block;", disp)
    if bloco:
        estilo += " max-width: 600px;"
    return (f'<a href="{href}" style="text-decoration: none; border: 0;"><img\n'
            f'           src="{src}"\n'
            f'           alt="{html.escape(alt, quote=True)}"\n'
            f'           width="{w}" height="{h}" border="0"\n'
            f'           style="{estilo}"></a>')


def montar(slug):
    p = pessoas.pega(slug)
    caminho = lambda n: os.path.join(V1, n)
    for n in (f"{slug}.png", f"{slug}-contatos-tel.png",
              f"{slug}-contatos-email.png", f"{slug}-contatos-end.png"):
        if not os.path.exists(caminho(n)):
            raise SystemExit(f"ABORTADO: falta {n} em v1/pessoas/. "
                             f"Rode antes: python3 build.py {slug}")

    cw, ch = medir(caminho(f"{slug}.png"))
    tw, th = medir(caminho(f"{slug}-contatos-tel.png"))
    ew, eh = medir(caminho(f"{slug}-contatos-email.png"))
    dw, dh = medir(caminho(f"{slug}-contatos-end.png"))

    if tw + ew != 600:
        raise SystemExit(f"ABORTADO: as fatias da linha 1 somam {tw + ew}, não 600. "
                         "A assinatura sairia desalinhada.")
    if th != eh:
        raise SystemExit(f"ABORTADO: as fatias da linha 1 têm alturas diferentes "
                         f"({th} e {eh}).")

    wa = f"https://wa.me/{p['whatsapp']}"
    corpo = f"""<!--
  ASSINATURA DE E-MAIL - TIME FORTE MARKETING ESPORTIVO
  {p['nome']}, {p['cargo']}

  GERADO por ferramentas/gerar_html.py - nao edite na mao. Para mudar algo,
  edite pessoas.py (dados) ou o gerador, e rode:
      python3 build.py {slug} && python3 gerar_html.py {slug}

  Contatos sao IMAGEM fatiada, cada fatia no seu <a>. Texto HTML encolhia no
  celular e o dark mode clareava o fundo; <map> nao sobrevive ao copiar-colar
  para o editor de assinatura do Gmail. Ver CLAUDE.md.
-->
<table cellpadding="0" cellspacing="0" border="0" role="presentation" width="600"
       style="max-width: 600px; font-family: Arial, sans-serif; border-collapse: collapse;">
  <tbody>

    <!-- CARD -->
    <tr>
      <td style="font-size: 0; line-height: 0;">
        {imagem(f"{URL}/pessoas/{slug}.png", cw, ch,
                f"{p['nome']}, {p['cargo']} - Time Forte Marketing Esportivo", SITE)}
      </td>
    </tr>

    <!-- CONTATOS (imagem fatiada; uma fatia = um link) -->
    <tr>
      <td style="font-size: 0; line-height: 0;">
        <table cellpadding="0" cellspacing="0" border="0" role="presentation" width="600"
               style="max-width: 600px; border-collapse: collapse;">
          <tbody>
            <tr>
              <td width="{tw}" style="font-size: 0; line-height: 0;">
                {imagem(f"{URL}/pessoas/{slug}-contatos-tel.png", tw, th,
                        f"Telefone e WhatsApp: {p['tel']}", wa)}
              </td>
              <td width="{ew}" style="font-size: 0; line-height: 0;">
                {imagem(f"{URL}/pessoas/{slug}-contatos-email.png", ew, eh,
                        f"E-mail: {p['email']}", f"mailto:{p['email']}")}
              </td>
            </tr>
            <tr>
              <td colspan="2" style="font-size: 0; line-height: 0;">
                {imagem(f"{URL}/pessoas/{slug}-contatos-end.png", dw, dh,
                        f"Endereco: {p['endereco']}", p['maps'])}
              </td>
            </tr>
          </tbody>
        </table>
      </td>
    </tr>

    <!-- FAIXA DE MARCAS (GIF animado) -->
    <tr>
      <td style="font-size: 0; line-height: 0;">
        {imagem(f"{URL}/comum/faixa-marcas.gif", 600, 38,
                "Escolas licenciadas: Flamengo, Chelsea, Real Madrid, Inter, "
                "Sport e Escola de Esportes Flamengo", SITE)}
      </td>
    </tr>

    <!-- RESPIRO -->
    <tr><td height="8" style="height: 8px; font-size: 0; line-height: 0;">&nbsp;</td></tr>

    <!-- BARRA DO SITE -->
    <tr>
      <td style="font-size: 0; line-height: 0;">
        {imagem(f"{URL}/comum/barra-chamada.png", 600, 36, "www.timeforte.com", SITE)}
      </td>
    </tr>

  </tbody>
</table>
"""
    os.makedirs(SAIDA, exist_ok=True)
    alvo = os.path.join(SAIDA, f"{slug}.html")
    with open(alvo, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(corpo)
    print(f"{slug}.html  card {cw}x{ch}  fatias {tw}+{ew}={tw+ew} x{th}  end {dw}x{dh}")


if __name__ == "__main__":
    args = sys.argv[1:]
    alvos = sorted(pessoas.PESSOAS) if "--todos" in args else args
    if not alvos:
        raise SystemExit("uso: gerar_html.py <slug> | --todos")
    for s in alvos:
        montar(s)
