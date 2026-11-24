#!/usr/bin/env python3
"""
Cadastro dos titulares das assinaturas. É a ÚNICA fonte de dados pessoais:
os geradores leem daqui, nada de constante espalhada dentro do código.

Para adicionar alguém, acrescente uma entrada e rode:
    python3 build.py <slug>

Campos:
  nome      como sai no card (Ubuntu Bold 50) - cabe até ~23 caracteres;
            mais longo encolhe o corpo até 44 antes de abortar
  cargo     como sai no card, em CAIXA ALTA   - cabe até ~24 caracteres
  tel       telefone como TEXTO na faixa de contatos
  whatsapp  só dígitos, com DDI, para montar o link wa.me
  email     endereço real; divide a linha 1 com o telefone, então é o campo
            mais apertado - com o telefone atual sobram ~191px, o que exclui
            padrões longos como nome.sobrenome@timeforte.com
  endereco  como sai na linha 2
  maps      link do Google Maps do endereço
  foto      arquivo em insumos/, PNG RGBA com fundo já removido
  crop      (x0, y0, x1, y1) na foto. Proporção ~1.283 (largura/altura) para
            encher o painel laranja sem sobrar nem vazar. Pode ultrapassar as
            bordas da imagem: o gerador preenche com transparência. Mais
            largo que 1.283, a sobra passa por baixo da diagonal (o painel
            recorta a foto) - para esconder cabelo ou ombro que encoste na
            borda direita da foto.
  espelhar  True inverte a foto na horizontal (para o olhar apontar ao nome)
  rev       opcional. Troca de foto DEPOIS que a pessoa instalou: o card novo
            sai em <slug>-r<rev>.png, endereço novo, e o antigo fica intacto
            para os e-mails já enviados (regra 1). A pessoa reinstala. Sem
            rev, o card é <slug>.png
  rev_contatos  opcional. O mesmo para a faixa de contatos (telefone ou
            e-mail novo): as fatias saem em <slug>-r<n>-contatos-*.png.
            Independe do rev do card

Os geradores abortam se nome, cargo, e-mail ou endereço não couberem - nunca
publicam peça cortada.
"""

ENDERECO_SEDE = "R. Barão de Ipanema, 56/301 — Copacabana, Rio de Janeiro/RJ"
MAPS_SEDE = ("https://maps.google.com/?q=R.+Bar%C3%A3o+de+Ipanema,+56,"
             "+Copacabana,+Rio+de+Janeiro")

PESSOAS = {
    "rafael-serra": {
        "nome": "Rafael Serra",
        "cargo": "CEO",
        "tel": "+55 21 98124-6506",
        "whatsapp": "5521981246506",
        "email": "rafael@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "recorte-limpo.png",
        "crop": (132, 14, 545, 336),
        "espelhar": False,
    },
    "camila-melo": {
        "nome": "Camila Melo",
        "cargo": "GERENTE DE OPERAÇÕES",
        "tel": "+55 21 96725-1171",
        "whatsapp": "5521967251171",
        "email": "camila@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "camila-limpo.png",
        # recorte fornecido já sem fundo (327x359). É estreita para a proporção
        # do painel: em altura cheia precisaria de 461px de largura. O crop
        # abaixo estoura as bordas de propósito — o gerador preenche com
        # transparência, que vira o laranja do painel.
        "crop": (-18, 0, 382, 312),
        "espelhar": False,
    },
    "jose-martins": {
        "nome": "José Martins",
        "cargo": "PRESIDENTE E CVO",
        "tel": "+55 21 99955-6207",
        "whatsapp": "5521999556207",
        "email": "zemartins@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "jose-martins-limpo.png",
        # recorte fornecido já sem fundo (401x232). Pessoa centrada em x~189;
        # o crop desce até a borda inferior da foto (corte seco no ombro) e
        # deixa ~22px de respiro acima do cabelo.
        "crop": (55, 22, 324, 232),
        "espelhar": False,
    },
    "cassio-lopes": {
        "nome": "Cássio Lopes",
        "cargo": "DIRETOR DE EXPANSÃO",
        "tel": "+55 21 99181-3831",
        "whatsapp": "5521991813831",
        "email": "cassio@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "cassio-lopes-limpo.png",
        # recorte fornecido já sem fundo (447x558). Foto tem corpo de sobra:
        # o crop enquadra cabeça e ombros da metade de cima, com corte seco
        # no peito, e estoura ~20px nas laterais (viram laranja do painel).
        "crop": (-20, 12, 452, 380),
        "espelhar": False,
    },
    "claudio-calabria": {
        "nome": "Claudio Calabria",
        "cargo": "GERENTE DE PLANEJAMENTO",
        "tel": "+55 21 99150-1531",
        "whatsapp": "5521991501531",
        "email": "claudiocalabria@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "claudio-calabria-limpo.png",
        # recorte fornecido já sem fundo (545x458). Cabeça e ombros com corte
        # seco no peito, rosto centrado em x~275. O e-mail de 29 caracteres é
        # o 1º caso do encolhe-até-caber da linha 1 (ver gerar_contatos.py).
        "crop": (41, 0, 509, 365),
        "espelhar": False,
    },
    "thamerson-fortuna": {
        "nome": "Thamerson Fortuna",
        "cargo": "ANALISTA FINANCEIRO",
        "tel": "+55 21 96718-9010",
        "whatsapp": "5521967189010",
        "email": "thamerson@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "thamerson-fortuna-limpo.png",
        # foto TROCADA em 26/08/2026 (mesmo dia da publicação, ninguém tinha
        # instalado): a 1ª era um perfil de frame de vídeo, espelhado.
        # Trocada de novo em 19/11/2026, de terno (1312x1199, estante com
        # planta e cadeira atrás - o birefnet-portrait deixou as duas de
        # fora). O card v2 dele estava no ar desde 18/11, então a foto nova é
        # rev 2: card em thamerson-fortuna-r2.png, o antigo fica intacto.
        "crop": (65, 50, 1267, 987),
        "espelhar": False,
        "rev": 2,
    },
    "paulo-cesar": {
        "nome": "Paulo Cesar",
        "cargo": "ANALISTA DE TI",
        "tel": "+55 21 96748-2875",
        "whatsapp": "5521967482875",
        "email": "paulocesar@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "paulo-cesar-limpo.png",
        # 2ª foto (18/11/2026 12:11, mais aberta). O PNG do remove.bg vem em
        # resolução de "preview" (461x541) e deixou o card borrado; por isso o
        # recorte é rembg (receita acima) na original 1366x1600, limitado pela
        # silhueta do remove.bg (o rembg deixava luminária e cadeira), sem
        # brilho de luminária no cabelo, com as íris (azuladas pelo filtro de
        # luz azul da lente) de volta ao castanho, reduzido a 683x800. Nada
        # de contraste/nitidez artificiais, e NÃO estenda o casaco para abrir
        # o crop - os dois foram testados na 1ª foto e reprovados.
        "crop": (5, 167, 702, 710),
        "espelhar": False,
    },
    "wagner-queiroz": {
        "nome": "Wagner de Queiroz Junior",
        "cargo": "HEAD DESIGNER",
        "tel": "+55 21 98457-4494",
        "whatsapp": "5521984574494",
        "email": "wagner@tstorm.com.br",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "wagner-queiroz-limpo.png",
        # selfie de 18/11/2026 (original 959x1280). Recorte rembg na original
        # com o alpha limitado pelo do remove.bg (o rembg deixava blocos de
        # parede cinza no cabelo; o remove.bg acerta o cabelo) e a cor dos
        # fios re-estimada sem o cinza (pymatting). Um objeto preto com LED
        # colado no ombro direito foi cortado na linha do ombro. Reduzido a
        # 719x960. A selfie corta os ombros: o crop estoura as laterais.
        "crop": (-90, 120, 808, 820),
        "espelhar": False,
    },
    "fernanda-oliveira": {
        "nome": "Fernanda Oliveira",
        "cargo": "COORDENADORA DE RH",
        "tel": "+55 21 98498-2373",
        "whatsapp": "5521984982373",
        "email": "fernanda@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "fernanda-oliveira-limpo.png",
        # 2ª foto (18/11/2026 16:31, 760x666): a mesma selfie com o quadro
        # ampliado - as laterais (fim do cabelo, mão, ombro) parecem geradas
        # por IA. A 1ª, fechada, deixava cortes retos no cabelo em qualquer
        # crop. Recorte com o birefnet-portrait do rembg (o u2net não vê o
        # cabelo cacheado como pessoa), armação dos óculos tornada opaca e
        # cor dos cachos re-estimada sem o fundo (pymatting), sem redução.
        # Primeira assinatura direto em v2/ (nunca teve v1/).
        "crop": (-10, 15, 670, 545),
        "espelhar": False,
    },
    "natalia-herdy": {
        "nome": "Natália Herdy",
        "cargo": "COORDENADORA DE MARKETING",
        "tel": "+55 21 99375-5404",
        "whatsapp": "5521993755404",
        "email": "natalia@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "natalia-herdy-limpo.png",
        # foto de 18/11/2026 (original 4075x5434, parede branca), reduzida a
        # 1/4 (1018x1358) antes do recorte. birefnet-portrait: segurou a
        # camiseta creme contra a parede branca. Cor dos fios re-estimada
        # sem o branco da parede (pymatting). O cargo, com 25 caracteres,
        # cabe (507 de 594px) - o "~24" da tabela de limites é conservador.
        "crop": (-122, 255, 1033, 1155),
        "espelhar": False,
    },
    "henrique-gomes": {
        "nome": "Henrique Gomes",
        "cargo": "GESTOR DE PROJETO",
        "tel": "+55 21 98071-2522",
        "whatsapp": "5521980712522",
        # e-mail CORRIGIDO em 23/11/2026 (era henriquegones@, com N, como veio
        # no pedido de 18/11): os contatos antigos estavam no ar, então os
        # novos são rev_contatos 2
        "email": "henriquegomes@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "henrique-gomes-limpo.png",
        # foto TROCADA em 23/11/2026. A 1ª (18/11) era um PRINT de celular de
        # uma foto com zoom, em evento: suave, cortando os ombros (crop
        # (-332, 80, 1413, 1440), estourando as laterais). A nova, 1536x1024 e
        # já sem fundo, é pela pose e pelo nome do arquivo a mesma foto
        # refeita por IA, com os dois ombros inteiros. Como na do Mauricio, o
        # corpo veio com alpha 253: reescalei para opaco e tirei 372 pixels
        # soltos de alpha <= 6. Borda clara = o cabelo grisalho, não halo. O
        # card v2 dele estava no ar desde 18/11, então a foto nova é rev 2:
        # card em henrique-gomes-r2.png, o antigo fica intacto. Crop mais
        # largo que 1.283 para o ombro direito sair por baixo da diagonal; o
        # esquerdo termina em curva, 14px antes da borda do crop.
        "crop": (208, -25, 1388, 788),
        "espelhar": False,
        "rev": 2,
        "rev_contatos": 2,
    },
    "beatriz-leal": {
        "nome": "Beatriz Leal da Silva",
        "cargo": "SOCIAL MEDIA",
        "tel": "+55 21 99948-1634",
        "whatsapp": "5521999481634",
        "email": "beatrizleal@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "beatriz-leal-limpo.png",
        # foto de 18/11/2026: só veio o "-removebg-preview" (460x543), sem a
        # original. Exceção à regra do preview porque o crop (488px de largura)
        # não precisa de ampliação para o painel em 2x - conferido no zoom, sem
        # borrar. Borda limpa (luminância 87), uma ilha só, usado sem retoque.
        # A foto corta os ombros: o crop estoura as laterais.
        "crop": (-9, 125, 479, 505),
        "espelhar": False,
    },
    "ronaldo-spinelli": {
        "nome": "Ronaldo Leal Spinelli",
        "cargo": "COORDENADOR TÉCNICO",
        "tel": "+55 21 96409-0243",
        "whatsapp": "5521964090243",
        "email": "naldo@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "ronaldo-spinelli-limpo.png",
        # selfie de 18/11/2026 (original 2556x3408, parede branca), reduzida a
        # 1/3 (852x1136) antes do recorte. birefnet-portrait: segurou o cabelo
        # grisalho curto contra a parede branca; armação dos óculos opaca e cor
        # da borda re-estimada sem o branco (pymatting). Borda clara (lum 144)
        # = cabelo grisalho e pele, não halo.
        "crop": (18, 286, 865, 946),
        "espelhar": False,
    },
    "alessandra-moreira": {
        "nome": "Alessandra Carvalho Moreira",
        "cargo": "COORDENADORA DE LOGÍSTICA",
        # telefone TROCADO em 19/11/2026 (era +55 21 96468-6330): os contatos
        # antigos estavam no ar, então os novos são rev_contatos 2
        "tel": "+55 21 98498-2375",
        "whatsapp": "5521984982375",
        "email": "alessandra@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "alessandra-moreira-limpo.png",
        # foto TROCADA em 19/11/2026, de blazer branco: de novo só o
        # "-removebg-preview" (433x577), sem a original; serve pelo mesmo
        # motivo da Beatriz (sem ampliação em 2x). Recorte limpo, sem pixel
        # solto. A 1ª (18/11, crop (-120, 62, 433, 452) mais largo que 1.283
        # porque os cachos encostavam na borda direita) estava no ar desde
        # 19/11 00h, então a nova é rev 2: card em alessandra-moreira-r2.png,
        # o antigo fica intacto. A mão do lado direito some sob a diagonal.
        # O nome, com 27 caracteres, é o 1º que encolhe (1px a mais em 50 -
        # ver gerar_card.py).
        "crop": (-60, -14, 420, 358),
        "espelhar": False,
        "rev": 2,
        "rev_contatos": 2,
    },
    "joao-mauricio": {
        # nome completo (João Mauricio Antunes Monteiro de Souza, 39 ch) não
        # cabe nem no piso de 44; opção 3 da prévia mandada a ele
        "nome": "João Mauricio",
        "cargo": "COORDENADOR DE EVENTOS",
        "tel": "+55 21 99826-2643",
        "whatsapp": "5521998262643",
        "email": "joaomauricio@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "joao-mauricio-limpo.png",
        # 3ª foto (19/11/2026, 1024x1536): a 2ª (painel de evento, com a
        # jaqueta de outra pessoa colada no ombro) ampliada até o corpo
        # inteiro - pelo tamanho e pelo nome do arquivo, por IA; o rosto é o
        # mesmo. A 1ª era de corpo inteiro num palco, inutilizável.
        # birefnet-portrait sem redução. Paulo pediu "do peito pra cima": o
        # crop pega os dois ombros inteiros e corta acima do bordado do peito.
        "crop": (93, 20, 940, 680),
        "espelhar": False,
    },
    "antonio-barreto": {
        "nome": "Antonio Barreto",
        "cargo": "EVENTOS",
        "tel": "+55 21 97137-3228",
        "whatsapp": "5521971373228",
        "email": "antonio@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "antonio-barreto-limpo.png",
        # 2ª foto (19/11/2026, 1774x887, já sem fundo): a selfie de parede
        # branca da 1ª, ampliada até os ombros inteiros - pelo nome do arquivo,
        # por IA; o rosto é o mesmo. Usada como veio, só sem 4 pixels soltos:
        # as pontas do cabelo têm o branco da parede embutido na cor (o
        # pymatting clareou em vez de limpar), mas no card não aparece. O crop
        # pega os dois ombros inteiros, sem corte reto nas laterais.
        "crop": (315, -5, 1445, 876),
        "espelhar": False,
    },
    "jessica-carneiro": {
        "nome": "Jéssica Carneiro",
        "cargo": "COORDENADORA DE SISTEMA",
        "tel": "+55 21 98498-2372",
        "whatsapp": "5521984982372",
        "email": "jessica@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "jessica-carneiro-limpo.png",
        # foto de 19/11/2026: só veio o "-removebg-preview" (440x566), sem a
        # original; serve como a da Beatriz (sem ampliação em 2x). Só tirei 2
        # ilhas soltas. O alto da cabeça encosta na borda de cima e o cabelo
        # longo nas laterais a partir de y=343: o crop é a foto inteira até
        # y=343 (largura cheia, proporção exata), então não aparece corte reto
        # - o cabelo sai pela borda de cima do painel, como retrato fechado.
        "crop": (0, 0, 440, 343),
        "espelhar": False,
    },
    "flavia-elisque": {
        "nome": "Flávia Elisque",
        "cargo": "DIRETORA ADMINISTRATIVA",
        "tel": "+55 21 98915-5925",
        "whatsapp": "5521989155925",
        "email": "flavia@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "flavia-elisque-limpo.png",
        # foto de 19/11/2026: veio só um recorte já sem fundo, 440x440, sem a
        # original. Usado como veio (uma ilha só). Borda clara (lum 186) = o
        # cabelo grisalho e a blusa creme, não halo. O crop amplia 1,13x no
        # card 2x - fica um pouco suave, no nível dos outros recortes prontos.
        "crop": (50, 45, 351, 280),
        "espelhar": False,
    },
    "clara-bardaro": {
        "nome": "Clara Bardaro",
        "cargo": "ATENDIMENTO",
        "tel": "+55 21 96714-1157",
        "whatsapp": "5521967141157",
        "email": "clara@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "clara-bardaro-limpo.png",
        # foto de 19/11/2026: só o "-removebg-preview" (432x577), selfie em
        # close. O cabelo encosta no topo (o crop começa em y=0, então esse
        # corte cai na borda de cima do painel) e camisa/cabelo encostam nas
        # duas laterais da metade de baixo - no enquadramento dos outros
        # cards isso virava um corte reto com laranja do lado. As laterais
        # foram estendidas 120px de cada lado, espelhando a faixa junto à
        # borda e recortando o espelho num ombro que desce para fora; a
        # imagem original começa em x=120 deste insumo.
        "crop": (60, 0, 612, 430),
        "espelhar": False,
    },
    "miriam-fernandes": {
        "nome": "Miriam Fernandes",
        "cargo": "ASSISTENTE FINANCEIRO",
        # mesmo número do Thamerson (linha do financeiro), como veio no pedido
        "tel": "+55 21 96718-9010",
        "whatsapp": "5521967189010",
        "email": "miriam@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "miriam-fernandes-limpo.png",
        # foto de 19/11/2026: só o "-removebg-preview" (490x509), sem a
        # original. Tirei 1 pixel solto. Os ombros encostam nas laterais só
        # abaixo de y=396, fora do crop.
        "crop": (0, -10, 520, 395),
        "espelhar": False,
    },
    "gabriel-muniz": {
        "nome": "Gabriel Monteiro Muniz",
        # 30 caracteres e cabe (540 de 594px): como na Natália, o "~24" da
        # tabela de limites é conservador
        "cargo": "SUPERVISOR DE ESCOLAS PRÓPRIAS",
        "tel": "+55 21 98704-3477",
        "whatsapp": "5521987043477",
        # o pedido trouxe "Gabriel Muniz" no campo do e-mail; endereço dado
        # pelo Paulo. Com 26 caracteres, ainda sai no corpo cheio de 14px
        "email": "gabrielmuniz@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "gabriel-muniz-limpo.png",
        # foto de 23/11/2026: só o "-removebg-preview" (433x576), sem a
        # original. Tirei o filete bege de fundo (um poste) colado no braço
        # esquerdo, de y=408 até a mesa; o resto como veio (uma ilha, borda
        # com luminância 109). Altura 266 = escala 1:1, o maior rosto sem
        # ampliar o preview, e mais largo que 1.283 para o ombro direito sair
        # por baixo da diagonal. O braço esquerdo abre na base e fica a 3px da
        # borda do crop: x0 acima de 28 vira corte reto. Base no peito, acima
        # do crachá (y~397).
        "crop": (26, 80, 394, 346),
        "espelhar": False,
    },
    "mauricio-helayel": {
        "nome": "Mauricio Helayel",
        "cargo": "SUPERVISOR DE MARKETING",
        "tel": "+55 21 98883-2979",
        "whatsapp": "5521988832979",
        "email": "mauricio@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "mauricio-helayel-limpo.png",
        # foto de 23/11/2026: retrato frontal já sem fundo, 1309x1201, com o
        # nome de arquivo no padrão da 2ª do Antonio (IA). Borda limpa (lum
        # 69, sem halo). O corpo veio com alpha 253, não 255: reescalei o
        # alpha (x255/253) para ficar opaco e tirei 1015 pixels soltos de
        # alpha <= 6 (ilhas e poeira longe do corpo). A foto é quase quadrada
        # e o rosto enche o quadro: o crop usa a altura inteira (a jaqueta vai
        # até a base, sem laranja embaixo) e sobe 10px, o que deixa o rosto do
        # tamanho do Henrique e a folga do cabelo igual à do Antonio. Os
        # ombros terminam antes das laterais do painel, como no Henrique.
        "crop": (-142, -10, 1412, 1201),
        "espelhar": False,
    },
    "thais-faria": {
        "nome": "Thais Rosa Faria",
        "cargo": "AUXILIAR ADMINISTRATIVA",
        # mesmo número da Camila (Gerente de Operações), como veio no pedido
        "tel": "+55 21 96725-1171",
        "whatsapp": "5521967251171",
        "email": "thais@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "thais-faria-limpo.png",
        # foto de 23/11/2026: selfie de WhatsApp (720x1280, JPEG), à noite,
        # parede clara e cabelo cacheado volumoso. Recorte com o
        # birefnet-portrait (o u2net erra nesse cabelo, caso Fernanda), corpo
        # de 254 reescalado para opaco e pymatting nos fios (borda com
        # luminância de 81 para 37). O braço encosta na borda esquerda da foto
        # de y=690 até embaixo, e nada encosta na direita: espelhada, essa
        # borda vai para a direita e some sob a diagonal (crop mais largo que
        # 1.283, como na Alessandra). A mão no cabelo fica embaixo à esquerda.
        "crop": (-72, 313, 730, 879),
        "espelhar": True,
    },
    "rafael-marinho": {
        "nome": "Rafael Marinho",
        "cargo": "ANALISTA FINANCEIRO",
        "tel": "+55 21 98498-2376",
        "whatsapp": "5521984982376",
        "email": "rafaelmarinho@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "rafael-marinho-limpo.png",
        # foto de 24/11/2026 (WhatsApp, 1166x1349, fundo branco de estúdio):
        # o rosto enche o quadro e os dois ombros saíam pelas bordas da foto,
        # o que no card viraria dois cortes retos com laranja dos lados.
        # Recorte com o birefnet-portrait + pymatting. Os ombros que a foto
        # cortou foram COMPLETADOS a pedido do Paulo: lona 300px mais larga de
        # cada lado, contorno desenhado continuando a posição e a inclinação
        # do ombro real na borda até o braço, e tecido sintetizado com a cor e
        # a textura da camisa. A foto original fica em x=300 do insumo, com
        # rosto, cabelo, pescoço e gola idênticos byte a byte: só se acrescentou
        # o que estava fora do quadro, sem alterar a aparência dele.
        "crop": (115, -56, 1688, 1170),
        "espelhar": False,
    },
    "inara-modena": {
        "nome": "Inara Modena",
        "cargo": "ASSISTENTE DE LOGÍSTICA",
        # mesmo número da Alessandra (Coordenadora de Logística), como veio
        # no pedido
        "tel": "+55 21 98498-2375",
        "whatsapp": "5521984982375",
        "email": "inara@timeforte.com",
        "endereco": ENDERECO_SEDE,
        "maps": MAPS_SEDE,
        "foto": "inara-modena-limpo.png",
        # foto de 24/11/2026: print de story (1206x2144, WebP), com a foto
        # levemente girada dentro de uma moldura escura e gente ao fundo.
        # Recorte com o birefnet-portrait + pymatting; saíram restos de um
        # homem ao fundo junto do cabelo, e a xuxinha rosa ficou opaca como
        # na foto (o birefnet a deixou meio transparente). O ombro direito
        # saía pela borda da foto: a pedido do Paulo, foi COMPLETADO além
        # dela, pele com a cor e a textura da borda. O contorno segue a
        # descida natural do ombro da foto (inclinação 1,2 na borda) até o
        # ombro (o mesmo da versão de 150px) e daí passa, com a mesma
        # tangente, para o BRAÇO, que desce reto a 230px da borda. O Paulo
        # foi ajustando: o ombro em bola (125px) ficou desproporcional, os
        # braços de 110 e 150px ficaram finos, alargar o ombro junto (250px)
        # estragou o ombro, que estava bom, e engrossar o braço abrindo para
        # baixo ficou "torto". Então o ombro ficou igual e o braço desce
        # grosso e reto.
        # As pontas dos cachos que encostavam na borda esmaecem em vez do
        # corte reto. Lona 340px mais larga à direita; o rosto e o resto da
        # foto ficam como no recorte. Enquadramento mais aberto que o das outras
        # (escala 0,165): com 0,19 a cabeça dominava o painel ("muito
        # cabeçuda", nas palavras do Paulo), e aberto aparecem a mão e a
        # pulseira.
        "crop": (-373, 190, 1695, 1802),
        "espelhar": False,
    },
}


def card(slug):
    """Nome do arquivo do card em <versao>/pessoas/ (ver o campo rev)."""
    rev = pega(slug).get("rev")
    return f"{slug}-r{rev}.png" if rev else f"{slug}.png"


def contatos(slug):
    """Prefixo das fatias de contatos em <versao>/pessoas/ (ver rev_contatos):
    <prefixo>.png, <prefixo>-tel.png, <prefixo>-email.png, <prefixo>-end.png."""
    rev = pega(slug).get("rev_contatos")
    return f"{slug}-r{rev}-contatos" if rev else f"{slug}-contatos"


def pega(slug):
    """Devolve o dicionário da pessoa ou erra com a lista de slugs válidos."""
    if slug not in PESSOAS:
        raise SystemExit(
            f"ABORTADO: slug '{slug}' não está em pessoas.py.\n"
            f"  Conhecidos: {', '.join(sorted(PESSOAS))}"
        )
    return PESSOAS[slug]
