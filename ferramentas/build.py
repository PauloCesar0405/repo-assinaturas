#!/usr/bin/env python3
"""
build.py — regera TODAS as pecas servidas da assinatura a partir dos insumos.

Roda os dois geradores e copia a saida para a pasta da versao atual
(marca.VERSAO, hoje v2/) - menos a faixa de marcas, que e viva e mora em
v1/comum/ (ver marca.py):
  gerar_card.py     -> card-topo.png, faixa-marcas.gif, barra-chamada.png
  gerar_contatos.py -> <SLUG>-contatos.png

Uso:
    cd ferramentas
    python3 build.py <slug> [--forcar] [--forcar-comum] [--atualizar-faixa]

O slug tem que existir em pessoas.py, que e onde moram TODOS os dados
pessoais (nome, cargo, telefone, e-mail, foto, recorte). Sem slug, gera
rafael-serra.

Peca que ja existe na versao e PULADA, nunca sobrescrita (regra 1 do
CLAUDE.md: versao publicada e imutavel). E por isso que gerar a segunda
pessoa nao mexe nas pecas compartilhadas de <versao>/comum/.

--forcar libera sobrescrever as pecas DA PESSOA (use so enquanto ninguem
instalou a assinatura dela). As de <versao>/comum/ exigem --forcar-comum a
parte, porque troca-las mexe na assinatura de todo mundo que ja instalou.

--atualizar-faixa troca SO a faixa de marcas, no mesmo endereco. Ela e a
unica peca viva (excecao da regra 1) e todas as versoes apontam para ela:
e assim que uma marca nova chega a todas as assinaturas ja instaladas, sem
ninguem reinstalar. Para
incluir ou tirar marca, edite MARCAS em gerar_card.py e rode:
    python3 build.py --atualizar-faixa

Depois: git add -A && git commit -m "rebuild" && git push origin master
"""
import os
import shutil
import subprocess
import sys

import marca

# o console do Windows abre em cp1252 e engasga com acento e com setas;
# os nomes/cargos das pessoas tem acento, entao forca UTF-8 na saida.
for fluxo in (sys.stdout, sys.stderr):
    try:
        fluxo.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

FER = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(FER)
COMUM = os.path.join(RAIZ, marca.VERSAO, "comum")
PESSOAS = os.path.join(RAIZ, marca.VERSAO, "pessoas")
FAIXA = os.path.join(RAIZ, *marca.FAIXA)

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


def mover(origem, destino, compartilhada=False, flag="--forcar-comum"):
    """Move para a versao NUNCA sobrescrevendo por acidente: peca publicada e
    imutavel (regra 1 do CLAUDE.md - e-mails ja enviados apontam para essa
    URL). Peca que ja existe e PULADA com aviso, nao sobrescrita nem tratada
    como erro: as de comum/ sao compartilhadas pelas ~30 assinaturas e ja
    estao la quando se gera a segunda pessoa.

    --forcar libera SO as pecas da pessoa. As compartilhadas exigem
    --forcar-comum, que e deliberadamente chato de digitar: como o gerador
    nao e reproduzivel byte a byte (metricas de fonte mudam entre versoes do
    Pillow), regerar a faixa ou a barra troca a arte dentro da assinatura de
    TODO MUNDO que ja instalou. Se a arte mudou de proposito, o certo e
    publicar numa versao nova (marca.VERSAO), nao forcar.

    A excecao e a faixa de marcas, liberada pela propria flag
    (--atualizar-faixa): trocar a arte de todo mundo e justamente o objetivo
    dela."""
    org = os.path.join(FER, origem)
    liberado = (flag in sys.argv) if compartilhada else ("--forcar" in sys.argv)
    if os.path.exists(destino) and not liberado:
        motivo = f"compartilhada, precisa de {flag}" if compartilhada else f"ja existe em {marca.VERSAO}/"
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
    mover("faixa-marcas.gif", FAIXA, compartilhada=True, flag="--atualizar-faixa")
    mover("barra-chamada.png", os.path.join(COMUM, "barra-chamada.png"), compartilhada=True)

    print("2/2  faixa de contatos")
    # o SLUG vai por argumento: gerar_contatos.py escreve direto em
    # <versao>/pessoas/<slug>-contatos*.png (e pula o que ja existir).
    rodar("gerar_contatos.py", SLUG, *[a for a in sys.argv[1:] if a == "--forcar"])

    print(f"\nOK. Pecas atualizadas em {marca.VERSAO}/. Agora:")
    print("  git add -A && git commit -m 'rebuild' && git push origin master")


if __name__ == "__main__":
    main()
