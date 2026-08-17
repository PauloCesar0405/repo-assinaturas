#!/usr/bin/env python3
"""
build.py — regera TODAS as pecas servidas da assinatura a partir dos insumos.

Roda os dois geradores e copia a saida para os lugares certos de v1/:
  gerar_card.py     -> card-topo.png, faixa-marcas.gif, barra-chamada.png
  gerar_contatos.py -> <SLUG>-contatos.png

Uso:
    cd ferramentas
    python3 build.py <slug> [--forcar] [--forcar-comum]

O slug tem que existir em pessoas.py, que e onde moram TODOS os dados
pessoais (nome, cargo, telefone, e-mail, foto, recorte). Sem slug, gera
rafael-serra.

Peca que ja existe em v1/ e PULADA, nunca sobrescrita (regra 1 do CLAUDE.md:
v1/ e imutavel depois de publicado). E por isso que gerar a segunda pessoa
nao mexe nas pecas compartilhadas de v1/comum/.

--forcar libera sobrescrever as pecas DA PESSOA (use so enquanto ninguem
instalou a assinatura dela). As de v1/comum/ exigem --forcar-comum a parte,
porque troca-las mexe na assinatura de todo mundo que ja instalou.

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


def mover(origem, destino, compartilhada=False):
    """Move para v1/ NUNCA sobrescrevendo por acidente: peca publicada e
    imutavel (regra 1 do CLAUDE.md - e-mails ja enviados apontam para essa
    URL). Peca que ja existe e PULADA com aviso, nao sobrescrita nem tratada
    como erro: as de v1/comum/ sao compartilhadas pelas ~30 assinaturas e ja
    estao la quando se gera a segunda pessoa.

    --forcar libera SO as pecas da pessoa. As compartilhadas exigem
    --forcar-comum, que e deliberadamente chato de digitar: como o gerador
    nao e reproduzivel byte a byte (metricas de fonte mudam entre versoes do
    Pillow), regerar a faixa ou a barra troca a arte dentro da assinatura de
    TODO MUNDO que ja instalou. Se a arte mudou de proposito, o certo e
    publicar em v2/, nao forcar."""
    org = os.path.join(FER, origem)
    liberado = ("--forcar-comum" in sys.argv) if compartilhada else ("--forcar" in sys.argv)
    if os.path.exists(destino) and not liberado:
        motivo = "compartilhada, precisa de --forcar-comum" if compartilhada else "ja existe em v1/"
        print(f"    PULADA ({motivo}): {os.path.relpath(destino, RAIZ)}")
        os.remove(org)
        return
    aviso = "  SOBRESCREVENDO" if os.path.exists(destino) else ""
    shutil.move(org, destino)
    print(f"    -> {os.path.relpath(destino, RAIZ)}{aviso}")


def main():
    os.makedirs(COMUM, exist_ok=True)
    os.makedirs(PESSOAS, exist_ok=True)

    print(f"gerando '{SLUG}'")
    print("1/2  card + faixa + barra")
    rodar("gerar_card.py", SLUG)
    mover("card-topo.png", os.path.join(PESSOAS, f"{SLUG}.png"))
    mover("faixa-marcas.gif", os.path.join(COMUM, "faixa-marcas.gif"), compartilhada=True)
    mover("barra-chamada.png", os.path.join(COMUM, "barra-chamada.png"), compartilhada=True)

    print("2/2  faixa de contatos")
    # o SLUG vai por argumento: gerar_contatos.py escreve direto em
    # v1/pessoas/<slug>-contatos.png (e aborta se o arquivo ja existir).
    rodar("gerar_contatos.py", SLUG, *[a for a in sys.argv[1:] if a == "--forcar"])

    print("\nOK. Pecas atualizadas em v1/. Agora:")
    print("  git add -A && git commit -m 'rebuild' && git push origin master")


if __name__ == "__main__":
    main()
