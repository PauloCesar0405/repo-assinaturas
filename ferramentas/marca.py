#!/usr/bin/env python3
"""
Marca e versão: fonte ÚNICA das constantes visuais e da pasta de publicação
que os geradores usam (como pessoas.py é a fonte dos dados pessoais). Antes
o laranja vivia duplicado em gerar_card.py e gerar_contatos.py - num rebrand,
é assim que sai uma peça com um laranja e outra com outro.

VERSAO é a pasta onde saem as peças IMUTÁVEIS (card, contatos, barra).
Mudar cor, ângulo ou tipografia muda a arte de todo mundo: isso é pasta nova
(v3/...) e todos reinstalam - nunca sobrescrever uma versão publicada
(regra 1 do CLAUDE.md).

A faixa de marcas é a exceção: é viva e mora para sempre em v1/comum/, a URL
que as assinaturas já instaladas usam. Todas as versões apontam para ela, e
ela segue sempre a marca atual.

  v1  LARANJA #F58634, itálico 14,7° (logotipo antigo, medido no "I")
  v2  LARANJA #F36D21, itálico 10°   (logotipo novo, nov/2026). Medidos em
      insumos/timeforte_aplicacao_preto.png: todo pixel laranja opaco é
      exatamente #F36D21; as duas bordas do "I" dão 10,0°, e T, M, F, T e E
      batem.
"""

VERSAO = "v2"
FAIXA = ("v1", "comum", "faixa-marcas.gif")   # viva, compartilhada (ver acima)

PRETO = (32, 30, 30)            # #201E1E
LARANJA = (243, 109, 33)        # #F36D21
# fim do gradiente do painel do card: o LARANJA escurecido na mesma relação
# (matiz, saturação, brilho) que o v1 usava (#F58634 -> #D36620)
LARANJA_ESCURO = (209, 78, 15)
ANG = 10.0                      # itálico do logotipo, em graus
