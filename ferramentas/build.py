#!/usr/bin/env python3
"""
build.py — regera TODAS as pecas servidas da assinatura a partir dos insumos.

Roda os dois geradores e copia a saida para os lugares certos de v1/:
  gerar_card.py     -> card-topo.png, faixa-marcas.gif, barra-chamada.png
  gerar_contatos.py -> <SLUG>-contatos.png

Uso:
    cd ferramentas
    python3 build.py <slug> [--forcar]

O slug tem que existir em pessoas.py, que e onde moram TODOS os dados
pessoais (nome, cargo, telefone, e-mail, foto, recorte). Sem slug, gera
rafael-serra.

Peca que ja existe em v1/ e PULADA, nunca sobrescrita (regra 1 do CLAUDE.md:
v1/ e imutavel depois de publicado). E por isso que gerar a segunda pessoa
nao mexe nas pecas compartilhadas de v1/comum/.

Depois: git add -A && git commit -m "rebuild" && git push origin master
"""
import os
import shutil
import subprocess
import sys

# o console do Windows abre em cp1252 e engasga com acento e com setas;
# os nomes/cargos das pessoas tem acento, entao forca UTF-8 na saida.
for fluxo in (sys.stdout, sys.stderr):
    try:
        fluxo.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

FER = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(FER)
COMUM = os.path.join(RAIZ, "v1", "comum")
PESSOAS = os.path.join(RAIZ, "v1", "pessoas")

# quem esta gerando: primeiro argumento, ou o default. Os dados da pessoa
# vivem em pessoas.py - nao ha texto pessoal dentro dos geradores.
SLUG = next((a for a in sys.argv[1:] if not a.startswith("-")), "rafael-serra")


def rodar(script, *args):
    print(f"  -> {script} {' '.join(args)}".rstrip())
    r = subprocess.run([sys.executable, script, *args], cwd=FER,
                       capture_output=True, text=True)
    if r.returncode:
        print(r.stdout, r.stderr, file=sys.stderr)
        sys.exit(f"FALHOU: {script}")
    print("   ", r.stdout.strip().replace("\n", "\n    "))


def mover(origem, destino):
    """Move para v1/ NUNCA sobrescrevendo: peca publicada e imutavel (regra 1
    do CLAUDE.md - e-mails ja enviados apontam para essa URL). Peca que ja
    existe e PULADA com aviso, nao sobrescrita nem tratada como erro: as pecas
    de v1/comum/ sao compartilhadas pelas ~30 assinaturas e ja estao la quando
    se gera a segunda pessoa. Para regerar de proposito, use --forcar (e, se a
    arte mudou de verdade, o certo e publicar em v2/, nao forcar)."""
    org = os.path.join(FER, origem)
    if os.path.exists(destino) and "--forcar" not in sys.argv:
        print(f"    PULADA (ja existe em v1/): {os.path.relpath(destino, RAIZ)}")
        os.remove(org)
        return
    shutil.move(org, destino)
    print(f"    -> {os.path.relpath(destino, RAIZ)}")


def main():
    os.makedirs(COMUM, exist_ok=True)
    os.makedirs(PESSOAS, exist_ok=True)

    print(f"gerando '{SLUG}'")
    print("1/2  card + faixa + barra")
    rodar("gerar_card.py", SLUG)
    mover("card-topo.png", os.path.join(PESSOAS, f"{SLUG}.png"))
    mover("faixa-marcas.gif", os.path.join(COMUM, "faixa-marcas.gif"))
    mover("barra-chamada.png", os.path.join(COMUM, "barra-chamada.png"))

    print("2/2  faixa de contatos")
    # o SLUG vai por argumento: gerar_contatos.py escreve direto em
    # v1/pessoas/<slug>-contatos.png (e aborta se o arquivo ja existir).
    rodar("gerar_contatos.py", SLUG, *[a for a in sys.argv[1:] if a == "--forcar"])

    print("\nOK. Pecas atualizadas em v1/. Agora:")
    print("  git add -A && git commit -m 'rebuild' && git push origin master")


if __name__ == "__main__":
    main()
