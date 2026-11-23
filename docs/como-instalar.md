# Assinatura de e-mail Time Forte — instalação

A assinatura é uma pilha de **4 blocos** (o do meio fatiado em 3 imagens
clicáveis, então 6 arquivos ao todo) hospedados no GitHub Pages, montada
por uma `<table>` num arquivo HTML. As URLs já vêm preenchidas — não há nada
para hospedar nem para substituir. Vá direto ao **Passo único**, abaixo.

Os contatos (telefone, e-mail, endereço) são **imagem**, não texto. Isso é
deliberado: como texto HTML eles encolhiam no celular e o dark mode clareava o
fundo (a "faixa branca"). Para continuarem clicáveis, a faixa é cortada em
**3 fatias**, cada uma dentro do próprio link. Não "conserte" isso voltando
para texto nem para `<map>` — ver `CLAUDE.md`, "Histórico de decisões".

## Arquivos

| Arquivo                                  | O que é                              |
|------------------------------------------|--------------------------------------|
| `assinaturas-html/<pessoa>.html`         | A assinatura, URLs já preenchidas    |
| `v2/pessoas/<pessoa>.png`                | Card: foto, nome, cargo (600×145)    |
| `v2/pessoas/<pessoa>-contatos-tel.png`   | Fatia telefone → WhatsApp (375×26)   |
| `v2/pessoas/<pessoa>-contatos-email.png` | Fatia e-mail → mailto (225×26)       |
| `v2/pessoas/<pessoa>-contatos-end.png`   | Fatia endereço → Maps (600×23)       |
| `v1/comum/faixa-marcas.gif`              | Marcas licenciadas deslizando (600×38) — viva, vale para todas as versões |
| `v2/comum/barra-chamada.png`             | Barra WWW.TIMEFORTE.COM (600×36)     |

A versão atual é a **v2** (marca nova de nov/2026). Quem instalou uma
assinatura v1 precisa **reinstalar** pelo HTML atual: card, contatos e barra
mudaram de endereço. Os e-mails já enviados com a v1 continuam funcionando.

Quem já tem assinatura: ver `ferramentas/pessoas.py` (um `.html` por pessoa
em `assinaturas-html/`).

## Passo único — instalar

**Página de instalação:** https://paulocesar0405.github.io/repo-assinaturas/
— cada um busca o próprio nome, vê a prévia e clica em **Copiar
assinatura**; o passo a passo tem abas para Gmail, Outlook novo/web e
Outlook clássico. Mande esse link para o time. Para mandar direto a de uma
pessoa: `.../repo-assinaturas/#<slug>` (ex.: `#mauricio-helayel`).

O botão Copiar põe na área de transferência a `<table>` do
`assinaturas-html/<pessoa>.html`: o mesmo que o `Ctrl+A`/`Ctrl+C` na
página renderizada da pessoa, que continua valendo pelo botão "Abrir em
outra aba". (Copia-se sempre a assinatura renderizada, nunca o
código-fonte.)

**Gmail (web):** Copiar assinatura → Gmail → Configurações → Geral →
Assinatura → Criar nova → `Ctrl+V` → definir como padrão para novos
e-mails e respostas → Salvar alterações.

**Outlook novo / Web:** Copiar assinatura → Configurações (engrenagem) →
Contas → Assinaturas → + Nova assinatura → `Ctrl+V` → Salvar → escolher a
nova como padrão para novas mensagens e respostas/encaminhamentos →
Salvar. No Mac: Outlook → Configurações → Assinaturas.

**Outlook clássico (Windows):** o editor dele desmonta HTML colado, então
a assinatura entra trocando o arquivo. Crie uma assinatura chamada
`Time Forte` (com um "x" de conteúdo) em Arquivo → Opções → Email →
Assinaturas, já como padrão para novas mensagens e respostas, e feche o
Outlook. Na aba Outlook clássico da página, **Baixar Time Forte.htm** gera
o arquivo da pessoa escolhida (UTF-8 com BOM e `meta charset`, para os
acentos dos textos alternativos). Ele substitui o `Time Forte.htm` em
`%APPDATA%\Microsoft\Assinaturas`; a pasta leva o nome na língua do
Office (`Signatures` no Office em inglês). Editar a assinatura depois
pelas Opções faz o Outlook regravar o arquivo e desfaz a troca.

**Celular:** os apps usam uma "assinatura mobile" própria em texto puro.
Deixe-a desativada; a assinatura configurada no desktop sincroniza sozinha.

## Comportamentos esperados

- **Depois de instalar, teste os cliques no próprio Gmail** — mandando um
  e-mail para você mesmo e clicando. Não basta testar abrindo o `.html` no
  navegador: já houve uma versão que funcionava no navegador e chegava sem
  nenhum clique no Gmail (era `<map>`, que não sobrevive ao copiar-colar).
  Telefone abre o WhatsApp, e-mail abre o compositor, endereço abre o Maps.
  Funciona também no celular.
- Outlook do Windows congela o GIF da faixa no frame 1 (Flamengo visível).
- Destinatários novos podem ver "Exibir imagens" — padrão de qualquer
  assinatura com imagem hospedada. Com as imagens bloqueadas, o texto
  alternativo carrega nome, cargo, telefone, e-mail e endereço.
- Peso total das peças ~600 KB (quase tudo é o GIF da faixa); o HTML tem
  ~5 KB, longe do limite de clipping do Gmail.
- Marca nova na faixa **não exige reinstalar**: a faixa é trocada no mesmo
  endereço e aparece sozinha em todas as assinaturas (pode levar um tempo
  por causa do cache do Gmail). Ver `CLAUDE.md`, regra 1.

## Onde as imagens moram

GitHub Pages, servido de `master`:
`https://paulocesar0405.github.io/repo-assinaturas/v2/...` (e a faixa em `.../v1/comum/`)

Para conferir se o deploy está no ar, abra a página de instalação em
`index.html#todas` (link "ver todas as assinaturas", no rodapé): a prévia
de cada pessoa tem que aparecer inteira, sem imagem quebrada, com a faixa
animando.

> Pendência registrada no `CLAUDE.md`: apontar `assinaturas.timeforte.com`
> por CNAME antes do rollout do time, para as URLs saírem de uma conta
> pessoal. As URLs publicadas são imutáveis, então essa migração precisa
> acontecer **antes** de a assinatura ser distribuída em escala — ou junto
> de uma reinstalação geral, como a da v2.

## Nota histórica

As rotas em GIF único e em fatias clicáveis foram aposentadas (imagem no
Gmail carrega um link só, o que quebrava os cliques). Se algum dia fizerem
falta, os geradores em `ferramentas/` reconstroem tudo em um comando.
