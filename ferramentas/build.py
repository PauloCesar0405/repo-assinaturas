#!/usr/bin/env python3
"""
build.py — regera TODAS as pecas servidas da assinatura a partir dos insumos.

Roda os dois geradores e copia a saida para os lugares certos de v1/:
  gerar_card.py     -> card-topo.png, faixa-marcas.gif, barra-chamada.png
  gerar_contatos.py -> <SLUG>-contatos.png

Uso:
    cd ferramentas
    python3 build.py [--forcar]

Sem --forcar, o build RECUSA sobrescrever qualquer peca que ja exista em v1/
(regra 1 do CLAUDE.md: v1/ e imutavel depois de publicado). Isso protege as
pecas compartilhadas de v1/comum/, que valem para as ~30 assinaturas.

Depois: git add -A && git commit -m "rebuild" && git push origin master
"""
import os
import shutil
import subprocess
import sys

FER = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(FER)
COMUM = os.path.join(RAIZ, "v1", "comum")
PESSOAS = os.path.join(RAIZ, "v1", "pessoas")

# quem esta gerando hoje. Ao clonar para outra pessoa, mude aqui e nos
# textos dentro de gerar_card.py / gerar_contatos.py.
SLUG = "rafael-serra"


def rodar(script, *args):
    print(f"  → {script} {' '.join(args)}".rstrip())
    r = subprocess.run([sys.executable, script, *args], cwd=FER,
                       capture_output=True, text=True)
    if r.returncode:
        print(r.stdout, r.stderr, file=sys.stderr)
        sys.exit(f"FALHOU: {script}")
    print("   ", r.stdout.strip().replace("\n", "\n    "))


def mover(origem, destino):
    """Move para v1/ recusando sobrescrita: peca publicada e imutavel (regra 1
    do CLAUDE.md). Rode com --forcar enquanto a peca ainda nao foi publicada."""
    if os.path.exists(destino) and "--forcar" not in sys.argv:
        sys.exit(
            f"ABORTADO: {os.path.relpath(destino, RAIZ)} ja existe.\n"
            "  v1/ e imutavel depois de publicado - e-mails ja enviados apontam\n"
            "  para essa URL. Arte nova entra como v2/ (nova pasta).\n"
            "  Se a peca ainda NAO foi publicada, repita com: python3 build.py --forcar"
        )
    shutil.move(os.path.join(FER, origem), destino)


def main():
    os.makedirs(COMUM, exist_ok=True)
    os.makedirs(PESSOAS, exist_ok=True)

    print("1/2  card + faixa + barra")
    rodar("gerar_card.py")
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
