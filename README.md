# Assinaturas de e-mail — Time Forte

Assinaturas de e-mail corporativas, servidas por GitHub Pages a partir
deste repositório. Titulares: Rafael Serra (CEO) e Camila Melo
(Coordenadora de Operações). Os dados de cada pessoa ficam em
`ferramentas/pessoas.py`; as peças e o HTML são gerados a partir dali.

**→ Leia o `CLAUDE.md` para entender o projeto inteiro.** Este README é o
resumo operacional.

## Deploy

- Ao vivo: https://paulocesar0405.github.io/repo-assinaturas/
- Branch de publicação: **`master`**
- Verificação: abra `index.html` publicado; as 6 imagens devem aparecer,
  a faixa de marcas animando.

## Uso rápido

Instalar a assinatura de alguém → abra `assinaturas-html/<pessoa>.html` no
Chrome, `Ctrl+A`/`Ctrl+C`, cole no editor de assinatura do Gmail.
Detalhes por cliente em `docs/como-instalar.md`.

Regenerar as imagens (após editar os geradores):

```bash
pip install -r requirements.txt
cd ferramentas && python3 build.py
git add -A && git commit -m "rebuild" && git push origin master
```

## Regras de ouro

- **`v1/` é imutável** depois de publicado (e-mails enviados apontam para
  essas URLs para sempre). Arte nova entra como `v2/`.
- Repositório **público** — só material de assinatura.
- Push sempre para **`master`**.

Detalhes completos, anatomia, mapa de cliques e como adicionar pessoas:
**`CLAUDE.md`**.
