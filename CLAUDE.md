# CLAUDE.md — Assinaturas de e-mail Time Forte

Contexto para o Claude Code (e para humanos) trabalharem neste repositório.
Leia isto inteiro antes de editar qualquer coisa.

## O que é este projeto

Assinaturas de e-mail em HTML para a Time Forte Marketing Esportivo. A
assinatura é montada com **imagens hospedadas neste próprio repositório**
(via GitHub Pages) mais um pouco de HTML. O primeiro titular é o CEO,
Rafael Serra; a estrutura foi pensada para escalar até ~30 pessoas do time.

**Deploy ao vivo:** https://paulocesar0405.github.io/repo-assinaturas/
(conta do Paulo Cesar, TI da Time Forte). Branch de publicação: **`master`**.

## Anatomia da assinatura (de cima para baixo)

A assinatura é uma pilha de 4 blocos, cada um uma imagem, montados por uma
`<table>` no HTML:

1. **card** (`v1/pessoas/<slug>.png`, 600×145) — foto do CEO num painel
   laranja inclinado a 14,7° (o ângulo do itálico do logotipo), nome e
   cargo à direita. Link: site.
2. **contatos** (`v1/pessoas/<slug>-contatos-{tel,email,end}.png`, 600×49
   somadas) — telefone, e-mail e endereço. É **imagem** (não texto) de
   propósito: texto HTML encolhia no celular e o dark mode clareava o
   fundo (a "faixa branca"). São **3 fatias**, cada uma dentro do próprio
   `<a>` — ver abaixo. Links: WhatsApp, `mailto:`, Maps.
3. **faixa de marcas** (`v1/comum/faixa-marcas.gif`, 600×38) — logotipo
   Time Forte fixo à esquerda + marcas licenciadas (Flamengo, Chelsea,
   Real Madrid, Inter, Sport, Escola de Esportes Flamengo) **deslizando**
   em loop. É o único elemento animado. Link: site.
4. **barra** (`v1/comum/barra-chamada.png`, 600×36) — WWW.TIMEFORTE.COM em
   Audiowide. Link: site.

`comum/` = igual para todos. `pessoas/` = específico de cada titular.

## Cliques nos contatos (fatias, não `<map>`)

A faixa de contatos é imagem, então os cliques vêm de **3 fatias**, cada
uma numa célula de uma `<table>` aninhada, cada uma dentro do seu `<a>`:

| Fatia                      | Tamanho | Abre                             |
|----------------------------|---------|----------------------------------|
| `<slug>-contatos-tel.png`  | 375×26  | WhatsApp (`wa.me/5521981246506`) |
| `<slug>-contatos-email.png`| 225×26  | `mailto:`                        |
| `<slug>-contatos-end.png`  | 600×23  | Google Maps                      |

Os tamanhos são **por pessoa** (dependem da largura do telefone e do
e-mail renderizados); `gerar_contatos.py` imprime um JSON com eles ao
rodar. Os cortes caem no vazio preto entre o telefone e o bullet e entre
as duas linhas — nenhuma letra é cortada.

**Por que não `<map>` (não reintroduza).** A primeira versão era imagem
única + `<map>`/`<area>`. Isso funciona ao abrir o `.html` no navegador,
e por isso passou nos testes — mas **não sobrevive à instalação**. O
fluxo real é `Ctrl+A`/`Ctrl+C` na página renderizada e colar no editor de
assinatura do Gmail, e o `<map>` se perde nesse caminho: a `<img>` chega
com um `usemap` apontando para um mapa que não existe mais e **nada fica
clicável** — telefone não abre o WhatsApp, e-mail não abre o compositor,
endereço não abre o Maps. O Gmail ainda reescala a imagem da assinatura,
o que desalinharia as coordenadas de `<area>` mesmo que o mapa chegasse
inteiro.

Fatia + `<a>` é o mesmo mecanismo do card e da barra, que sempre
funcionaram. Vantagem extra: **agora o toque funciona no celular também**
— a limitação antiga ("alguns apps ignoram `<map>`") deixou de existir,
porque não há mais `<map>`.

Custo aceito: a área preta vazia à esquerda do telefone entra na fatia do
telefone, então clicar ali abre o WhatsApp em vez do site. O site continua
linkado no card, na faixa de marcas e na barra.

## Estrutura de pastas

```
v1/                        ← ativos servidos pelo Pages. IMUTÁVEL (ver Regras)
  comum/                   ← faixa-marcas.gif, barra-chamada.png
  pessoas/                 ← <slug>.png, <slug>-contatos.png
assinaturas-html/          ← um .html por pessoa, URLs já preenchidas
ferramentas/               ← a "fábrica"
  build.py                 ← regenera TODAS as peças de v1/
  gerar_card.py            ← card + faixa + barra
  gerar_contatos.py        ← faixa de contatos, fatiada (+ dimensões p/ o HTML)
  fontes/                  ← Ubuntu (Bold/Regular) + Audiowide; o texto de
                             cada licença vive ao lado do .ttf (UFL 1.0 e
                             SIL OFL 1.1 exigem isso na redistribuição)
  insumos/                 ← logos-fonte, foto do CEO sem fundo (recorte-limpo.png)
docs/como-instalar.md      ← guia de instalação no Gmail/Outlook
index.html                 ← página de verificação do deploy
CLAUDE.md                  ← este arquivo
```

## Como regenerar as peças

Requer Python 3.10+ e as libs de `requirements.txt`
(`pip install -r requirements.txt`). Então:

```bash
cd ferramentas
python3 build.py
```

Isso reescreve os 4 arquivos em `v1/`. Publicar = commit + push:

```bash
git add -A
git commit -m "rebuild"
git push origin master
```

O Pages atualiza em ~1–10 min (cache). Verifique abrindo `index.html`
publicado ou as URLs diretas das imagens.

## Marca (Manual Time Forte)

- **Cores:** PRETO `#201E1E`, LARANJA `#F58634`. Nada de `#F58733` (era um
  tom errado herdado do template antigo).
- **Tipografia:** Audiowide (display, vive nos títulos/URL), Ubuntu (texto).
  Ambas embutidas nas imagens — por isso funcionam em qualquer cliente.
- **Ângulo do itálico:** 14,7°, medido no glifo "I" do logotipo. Usado no
  painel do card e em qualquer diagonal.

## Regras invioláveis

1. **`v1/` é imutável depois de publicado.** E-mails já enviados apontam
   para essas URLs *para sempre*. Nunca renomeie nem apague nada dentro de
   `v1/`. Arte nova entra como `v2/` (nova pasta), e os HTMLs passam a
   apontar para `v2/`. Os e-mails antigos continuam válidos.
2. **Repositório é público** (exigência do Pages gratuito). Só material de
   assinatura aqui — nada sensível.
3. **Branch de deploy é `master`**, não `main`. Todo push é
   `git push origin master`.
4. **O gerador é a fonte da verdade**, não os PNGs. Para mudar o visual,
   edite `gerar_card.py`/`gerar_contatos.py` e rode `build.py` — não edite
   PNG na mão. As larguras/alturas das fatias de contatos no HTML precisam
   bater com o JSON que `gerar_contatos.py` imprime; se mexer no layout dos
   contatos, atualize o HTML com as novas dimensões.
   **Cuidado:** as métricas de fonte mudam entre versões do Pillow/FreeType,
   então o gerador não é reproduzível byte a byte — regerar hoje produz uma
   imagem sutilmente diferente da publicada. Peça nova com conteúdo diferente
   é `v2/`, nunca overwrite em `v1/` (o build já recusa sobrescrever).

## Adicionar uma nova pessoa (rumo às ~30)

Hoje o fluxo é manual por pessoa; o próximo passo natural é parametrizar.
Manualmente:

1. Ponha a foto sem fundo em `ferramentas/insumos/` (o `recorte-limpo.png`
   do Rafael foi gerado com remoção de fundo + limpeza de halo; replicar
   esse tratamento para a nova foto).
2. Em `gerar_card.py` e `gerar_contatos.py`, troque nome, cargo, telefone,
   e-mail (são strings no topo/corpo dos arquivos). Ajuste o `SLUG` em
   `build.py` — ele nomeia **as duas** peças (o card e, via argumento, a
   faixa de contatos).
3. `python3 build.py` → gera `<slug>.png` e as 3 fatias de contatos
   (`<slug>-contatos-tel/-email/-end.png`, mais a faixa inteira para
   compatibilidade). O build **recusa sobrescrever** qualquer peça que já
   exista em `v1/` (inclusive as compartilhadas de `v1/comum/`). Se
   abortar, é a regra 1 funcionando — não use `--forcar` numa peça já
   publicada.
4. Duplique `assinaturas-html/rafael-serra.html` para `<slug>.html`,
   trocando: nome do card, os 3 `src` das fatias, telefone (link `wa.me`
   + texto no alt), e-mail (link `mailto:` + alt), endereço (link do Maps
   + alt), e as **larguras/alturas das fatias** que o build imprimiu no
   JSON — elas mudam por pessoa, porque dependem da largura do telefone e
   do e-mail renderizados. A soma das duas larguras da linha 1 tem que dar
   exatamente 600.
5. Commit + push.

**Evolução recomendada (bom candidato a tarefa para o Claude Code):**
transformar isso numa fábrica orientada a dados — uma planilha/CSV com
nome, cargo, telefone, e-mail, arquivo da foto → um script que gera os 30
cards, 30 contatos e 30 HTMLs de uma vez. Se for fazer, os geradores já
estão modulares o suficiente; falta abstrair as strings pessoais para
parâmetros e iterar sobre o CSV.

## Instalar a assinatura (resumo; detalhes em docs/como-instalar.md)

O Gmail não aceita colar HTML cru. Fluxo:
1. Abra o `.html` da pessoa **no Chrome** (as imagens carregam do Pages).
2. `Ctrl+A`, `Ctrl+C` na página renderizada.
3. Gmail → Configurações → Geral → Assinatura → Criar nova → `Ctrl+V` →
   definir como padrão → Salvar.

No celular, a assinatura configurada no desktop sincroniza sozinha (não
mexa na "assinatura mobile" do app, que é texto puro).

## Histórico de decisões (por que está assim)

- Começou como assinatura HTML tradicional; virou card escuro estilo
  "card de atleta" seguindo uma referência que o cliente trouxe (Destra).
- Contatos eram texto HTML clicável até quebrarem no celular (encolhiam) e
  no dark mode (fundo clareava — a "faixa branca"). Viraram imagem.
- A imagem primeiro veio com `<map>`/`<area>`. Testava bem (abrindo o
  `.html` no navegador) e falhava em produção: o `<map>` não sobrevive ao
  `Ctrl+C`/`Ctrl+V` no editor de assinatura do Gmail, então nenhum contato
  ficava clicável. **Lição:** testar o HTML no navegador não é teste — o
  teste é instalar no Gmail e clicar.
- Hoje: **3 fatias, cada uma com seu `<a>`** — o mesmo mecanismo do card e
  da barra. Sobrevive ao copiar-colar e funciona no celular também, o que
  o `<map>` nunca fez. "Montagem chata" (o motivo de fatias terem sido
  descartadas antes) deixou de ser problema: o gerador corta sozinho e
  imprime as dimensões.
- Testadas e descartadas: GIF único (cliques não funcionam — 1 link por
  imagem), marca-d'água de "T" no fundo (poluía). Não reintroduza sem
  motivo.
- Hospedagem: GitHub Pages venceu por ser da própria equipe e transferível
  via domínio. Recomendação pendente: apontar `assinaturas.timeforte.com`
  por CNAME antes do rollout dos 30, para sair da conta pessoal.
