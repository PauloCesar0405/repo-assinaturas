# Assinatura de e-mail Time Forte — instalação

A assinatura é uma pilha de **4 imagens** hospedadas no GitHub Pages, montada
por uma `<table>` num arquivo HTML. As URLs já vêm preenchidas — não há nada
para hospedar nem para substituir. Vá direto ao **Passo único**, abaixo.

Os contatos (telefone, e-mail, endereço) são **imagem**, não texto. Isso é
deliberado: como texto HTML eles encolhiam no celular e o dark mode clareava o
fundo. Os cliques voltam por um `<map>` de áreas no HTML. Não "conserte" isso
voltando para texto — ver `CLAUDE.md`, "Histórico de decisões".

## Arquivos

| Arquivo                                  | O que é                              |
|------------------------------------------|--------------------------------------|
| `assinaturas-html/<pessoa>.html`         | A assinatura, URLs já preenchidas    |
| `v1/pessoas/<pessoa>.png`                | Card: foto, nome, cargo (600×145)    |
| `v1/pessoas/<pessoa>-contatos.png`       | Contatos + mapa de cliques (600×48)  |
| `v1/comum/faixa-marcas.gif`              | Marcas licenciadas deslizando (600×38) |
| `v1/comum/barra-chamada.png`             | Barra WWW.TIMEFORTE.COM (600×36)     |

Hoje existe uma pessoa: `rafael-serra`.

## Passo único — instalar

**Gmail (web):** abra `assinaturas-html/<pessoa>.html` no Chrome →
`Ctrl+A`, `Ctrl+C` na página renderizada → Gmail → Configurações →
Geral → Assinatura → Criar nova → `Ctrl+V` → definir como padrão para
novos e-mails e respostas → Salvar. (Copia-se a página renderizada,
nunca o código-fonte.)

**Outlook clássico (Windows):** crie uma assinatura vazia chamada
`Time Forte` em Arquivo → Opções → Email → Assinaturas, feche o Outlook
e substitua o `%APPDATA%\Microsoft\Signatures\Time Forte.htm` pelo nosso
arquivo renomeado. O editor dele desmonta HTML colado; o replace é fiel.

**Outlook novo / Web:** Configurações → Redigir e responder → colar o
renderizado (mesmo truque do Gmail).

**Celular:** os apps usam uma "assinatura mobile" própria em texto puro.
Deixe-a desativada; a assinatura configurada no desktop sincroniza sozinha.

## Comportamentos esperados

- **No celular, tocar nos contatos pode não abrir nada.** Alguns apps de
  e-mail ignoram `<map>`. A imagem continua perfeita e legível (dá para
  copiar o telefone/e-mail), só o toque não responde. É um limite conhecido
  e aceito — o cliente escolheu "visual idêntico em todo lugar" em vez de
  "clique garantido no celular". No computador o mapa clica os 4 destinos.
- Outlook do Windows congela o GIF da faixa no frame 1 (Flamengo visível).
- Destinatários novos podem ver "Exibir imagens" — padrão de qualquer
  assinatura com imagem hospedada. Com as imagens bloqueadas, o texto
  alternativo carrega nome, cargo, telefone, e-mail e endereço.
- Peso total das 4 peças ~436 KB; o HTML tem ~4 KB, longe do limite de
  clipping do Gmail.

## Onde as imagens moram

GitHub Pages, servido de `master`:
`https://paulocesar0405.github.io/repo-assinaturas/v1/...`

Para conferir se o deploy está no ar, abra o `index.html` publicado — ele
mostra as 4 peças na ordem da assinatura.

> Pendência registrada no `CLAUDE.md`: apontar `assinaturas.timeforte.com`
> por CNAME antes do rollout do time, para as URLs saírem de uma conta
> pessoal. As URLs de `v1/` são imutáveis, então essa migração precisa
> acontecer **antes** de a assinatura ser distribuída em escala.

## Nota histórica

As rotas em GIF único e em fatias clicáveis foram aposentadas (imagem no
Gmail carrega um link só, o que quebrava os cliques). Se algum dia fizerem
falta, os geradores em `ferramentas/` reconstroem tudo em um comando.
