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
com todo mundo que tem .html, na ordem de pessoas.py (molde em
pagina.html, pagina.css e pagina.js).
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
# logotipo do topo da pagina de instalacao, relativo a raiz do site
LOGO = "ferramentas/insumos/timeforte_aplicacao_preto.png"

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
    card = pessoas.card(slug)
    cont = pessoas.contatos(slug)
    for n in (card, f"{cont}-tel.png", f"{cont}-email.png", f"{cont}-end.png"):
        if not os.path.exists(caminho(n)):
            raise SystemExit(f"ABORTADO: falta {n} em {marca.VERSAO}/pessoas/. "
                             f"Rode antes: python3 build.py {slug}")

    cw, ch = medir(caminho(card))
    tw, th = medir(caminho(f"{cont}-tel.png"))
    ew, eh = medir(caminho(f"{cont}-email.png"))
    dw, dh = medir(caminho(f"{cont}-end.png"))

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
        {imagem(f"{URL}/pessoas/{card}", cw, ch,
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
                {imagem(f"{URL}/pessoas/{cont}-tel.png", tw, th,
                        f"Telefone e WhatsApp: {p['tel']}", wa)}
              </td>
              <td width="{ew}" style="font-size: 0; line-height: 0;">
                {imagem(f"{URL}/pessoas/{cont}-email.png", ew, eh,
                        f"E-mail: {p['email']}", f"mailto:{p['email']}")}
              </td>
            </tr>
            <tr>
              <td colspan="2" style="font-size: 0; line-height: 0;">
                {imagem(f"{URL}/pessoas/{cont}-end.png", dw, dh,
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
    a propria assinatura, e que tambem serve de verificacao do deploy
    (index.html#todas mostra todo mundo). Sai do cadastro, na ordem de
    pessoas.py, e a previa de cada pessoa e a <table> do proprio .html dela:
    o que aparece aqui e exatamente o que vai ser copiado, pelo botao Copiar
    ou pelo Ctrl+A/Ctrl+C na outra aba. O molde e pagina.html, com o estilo
    em pagina.css e o comportamento em pagina.js. Quem ainda nao tem .html
    gerado fica de fora."""
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
        # o avatar e o proprio card, ampliado em cima da foto (ver pagina.css)
        nomes.append(f'    <li><a class="nome" href="#{slug}"><span class="avatar"><img '
                     f'src="{URL}/pessoas/{pessoas.card(slug)}" alt=""></span>'
                     f'<span><b>{nome}</b><small>{cargo}</small></span></a></li>')
        blocos.append(f"""  <article class="pessoa" id="{slug}" data-nome="{nome}">
    <div class="cabeca"><h3>{nome}</h3><span class="cargo">{cargo}</span></div>
    <div class="previa"><div class="escala">
{tabela}
    </div></div>
    <div class="acoes">
      <button type="button" class="botao copiar">Copiar assinatura</button>
      <a class="botao sec" href="assinaturas-html/{slug}.html" target="_blank" rel="noopener">Abrir em outra aba</a>
    </div>
    <p class="retorno" role="status"></p>
  </article>""")

    def ler(nome):
        with open(os.path.join(BASE, nome), encoding="utf-8") as fh:
            return fh.read()

    # o comentario do topo de cada molde e para quem edita: fica de fora
    css = ler("pagina.css").split("*/", 1)[1].strip()
    js = ler("pagina.js").split("*/", 1)[1].strip()
    pagina = ler("pagina.html").split("-->", 1)[1].lstrip()
    cores = (f":root {{ --preto: {hexa(marca.PRETO)}; --laranja: {hexa(marca.LARANJA)}; "
             f"--laranja-escuro: {hexa(marca.LARANJA_ESCURO)}; }}")
    if not os.path.exists(os.path.join(RAIZ, *LOGO.split("/"))):
        raise SystemExit(f"ABORTADO: falta o logotipo do topo da pagina ({LOGO}).")
    for marcador, valor in (("__CSS__", f"{cores}\n{css}"),
                            ("__JS__", js),
                            ("__LOGO__", LOGO),
                            ("__NOMES__", "\n".join(nomes)),
                            ("__PESSOAS__", "\n".join(blocos)),
                            ("__EX_CARD__", f"{URL}/pessoas/{pessoas.card(exemplo)}"),
                            ("__EX_CONT__", f"{URL}/pessoas/{pessoas.contatos(exemplo)}.png"),
                            ("__FAIXA__", URL_FAIXA),
                            ("__BARRA__", f"{URL}/comum/barra-chamada.png"),
                            ("__VERSAO__", marca.VERSAO)):
        if marcador not in pagina:
            raise SystemExit(f"ABORTADO: pagina.html sem o marcador {marcador}.")
        pagina = pagina.replace(marcador, valor)

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
