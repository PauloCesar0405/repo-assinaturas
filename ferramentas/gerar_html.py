#!/usr/bin/env python3
"""
Monta assinaturas-html/<slug>.html a partir de pessoas.py e das peças que já
estão em <marca.VERSAO>/pessoas/. Mede as fatias no disco - nada de largura digitada na
mão, que era a fonte dos erros (mapa com nome repetido, coords defasadas,
link de outra pessoa).

Uso:
    python3 gerar_html.py <slug>        # um
    python3 gerar_html.py --todos       # todos os de pessoas.py

Estrutura gerada: uma <table> de 4 blocos. Os contatos são 3 fatias, cada
uma no seu <a> - ver o porquê em gerar_contatos.py e no CLAUDE.md.

Toda rodada também reescreve o index.html da raiz: a página de instalação,
com todo mundo que tem .html, na ordem de pessoas.py.
"""
import html
import os
import sys

from PIL import Image

import marca
import pessoas

BASE = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(BASE)
PECAS = os.path.join(RAIZ, marca.VERSAO, "pessoas")
SAIDA = os.path.join(RAIZ, "assinaturas-html")
PAGES = "https://paulocesar0405.github.io/repo-assinaturas"
URL = f"{PAGES}/{marca.VERSAO}"
URL_FAIXA = f"{PAGES}/{'/'.join(marca.FAIXA)}"   # viva, fica em v1/ (ver marca.py)
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
    caminho = lambda n: os.path.join(PECAS, n)
    for n in (f"{slug}.png", f"{slug}-contatos-tel.png",
              f"{slug}-contatos-email.png", f"{slug}-contatos-end.png"):
        if not os.path.exists(caminho(n)):
            raise SystemExit(f"ABORTADO: falta {n} em {marca.VERSAO}/pessoas/. "
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

    <!-- FAIXA DE MARCAS (GIF animado; peca viva, troca no mesmo endereco) -->
    <tr>
      <td style="font-size: 0; line-height: 0;">
        {imagem(URL_FAIXA, 600, 38,
                "Escolas licenciadas Time Forte", SITE)}
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


def indice():
    """Reescreve o index.html da raiz: a pagina que o time abre para instalar
    a propria assinatura, e que tambem serve de verificacao do deploy. Sai do
    cadastro, na ordem de pessoas.py, e a previa de cada pessoa e a <table>
    do proprio .html dela - o que aparece aqui e exatamente o que vai ser
    copiado. Quem ainda nao tem .html gerado fica de fora."""
    hexa = lambda c: "#%02X%02X%02X" % c
    nomes, blocos, exemplo = [], [], None
    for slug, p in pessoas.PESSOAS.items():
        arq = os.path.join(SAIDA, f"{slug}.html")
        if not os.path.exists(arq):
            continue
        with open(arq, encoding="utf-8") as fh:
            tabela = fh.read().split("-->", 1)[1].strip()
        exemplo = exemplo or slug
        nome, cargo = html.escape(p["nome"]), html.escape(p["cargo"])
        nomes.append(f'          <li><a href="#{slug}">{nome}</a></li>')
        blocos.append(f"""
<article class="pessoa" id="{slug}">
  <div class="cabeca">
    <div><h3>{nome}</h3><span class="cargo">{cargo}</span></div>
    <a class="botao" href="assinaturas-html/{slug}.html" target="_blank" rel="noopener">Abrir minha assinatura &rarr;</a>
  </div>
  <div class="previa">
{tabela}
  </div>
  <a class="voltar" href="#como-instalar">&uarr; Passo a passo para instalar</a>
</article>""")

    # tutorial: CSS + HTML num arquivo a parte (ferramentas/tutorial.html); a
    # assinatura de exemplo das ilustracoes e a da 1a pessoa do cadastro
    with open(os.path.join(BASE, "tutorial.html"), encoding="utf-8") as fh:
        css_tut, tutorial = fh.read().split("<!-- ===CORPO=== -->")
    css_tut = css_tut.split("*/", 1)[1]   # o comentario do topo e para quem edita
    for marca_, valor in (("__NOMES__", "\n".join(nomes)),
                          ("__EX_CARD__", f"{URL}/pessoas/{exemplo}.png"),
                          ("__EX_CONT__", f"{URL}/pessoas/{exemplo}-contatos.png"),
                          ("__FAIXA__", URL_FAIXA),
                          ("__BARRA__", f"{URL}/comum/barra-chamada.png")):
        tutorial = tutorial.replace(marca_, valor)

    pagina = f"""<!doctype html>
<!-- GERADO por ferramentas/gerar_html.py a partir de pessoas.py - nao edite na mao. -->
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Assinaturas Time Forte</title>
<style>
  :root {{ --preto: {hexa(marca.PRETO)}; --laranja: {hexa(marca.LARANJA)};
           --laranja-escuro: {hexa(marca.LARANJA_ESCURO)}; --cinza: #6E6A69;
           --fundo: #F4F4F5; --linha: #E4E4E7; }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: var(--fundo); color: var(--preto);
          font: 16px/1.55 system-ui, -apple-system, "Segoe UI", Ubuntu, Roboto, sans-serif; }}
  main {{ max-width: 720px; margin: 0 auto; padding: 32px 16px 64px; }}
  header {{ border-left: 6px solid var(--laranja); padding-left: 16px; margin-bottom: 28px; }}
  h1 {{ font-size: 28px; line-height: 1.2; margin: 0 0 4px; }}
  header p {{ margin: 0; color: var(--cinza); }}
  h2 {{ font-size: 18px; margin: 0 0 12px; }}
  kbd {{ font: 13px/1 ui-monospace, Consolas, monospace; background: var(--fundo);
         border: 1px solid #D4D4D8; border-bottom-width: 2px; border-radius: 4px; padding: 2px 5px; }}
  .nomes {{ display: flex; flex-wrap: wrap; gap: 8px; list-style: none; margin: 0 0 20px; padding: 0; }}
  .nomes a {{ display: block; padding: 6px 14px; border-radius: 999px; background: #fff;
              border: 1px solid var(--linha); color: var(--preto); text-decoration: none; font-size: 14px; }}
  .nomes a:hover {{ border-color: var(--laranja); }}
  .pessoa {{ background: #fff; border: 1px solid var(--linha); border-radius: 12px;
             padding: 20px 24px; margin-bottom: 16px; scroll-margin-top: 16px; }}
  .pessoa:target {{ border-color: var(--laranja); box-shadow: 0 0 0 3px rgba(243, 109, 33, .25); }}
  .cabeca {{ display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between;
             gap: 12px; margin-bottom: 16px; }}
  .cabeca h3 {{ font-size: 18px; margin: 0; }}
  .cargo {{ color: var(--cinza); font-size: 12px; font-weight: 700; letter-spacing: .12em; }}
  .botao {{ display: inline-block; background: var(--laranja); color: var(--preto); font-weight: 700;
            text-decoration: none; padding: 10px 16px; border-radius: 8px; }}
  .botao:hover {{ background: var(--laranja-escuro); color: #fff; }}
  .previa {{ overflow-x: auto; }}
  .voltar {{ display: inline-block; margin-top: 12px; color: var(--cinza); font-size: 13px; }}
  footer {{ color: var(--cinza); font-size: 13px; margin-top: 32px; }}
  @media (max-width: 480px) {{ .pessoa {{ padding: 16px; }} h1 {{ font-size: 24px; }} }}
{css_tut.strip()}
</style>
</head>
<body>
<main>
<header>
  <h1>Assinaturas de e-mail</h1>
  <p>Time Forte Marketing Esportivo &middot; encontre seu nome e instale em 2 minutos.</p>
</header>

{tutorial.strip()}
{"".join(blocos)}

<footer>
  Versão atual das assinaturas: <b>{marca.VERSAO}</b>. Se você instalou antes de mudar a versão, apague a
  antiga e instale de novo; os e-mails já enviados continuam certos. Esta página também é a
  verificação do deploy: todas as assinaturas acima têm que aparecer inteiras, sem imagem
  quebrada, com a faixa de marcas animando. Gerada por <code>ferramentas/gerar_html.py</code>.
</footer>
</main>
</body>
</html>
"""
    alvo = os.path.join(RAIZ, "index.html")
    with open(alvo, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(pagina)
    print(f"index.html  {len(blocos)} assinaturas")


if __name__ == "__main__":
    args = sys.argv[1:]
    alvos = sorted(pessoas.PESSOAS) if "--todos" in args else args
    if not alvos:
        raise SystemExit("uso: gerar_html.py <slug> | --todos")
    for s in alvos:
        montar(s)
    # a pagina de instalacao lista todo mundo: refaz a cada rodada
    indice()
