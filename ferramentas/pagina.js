/* Página de instalação (index.html): comportamento. Lido por gerar_html.py e
   embutido no fim do <body>. Sem este script a página continua funcionando:
   todas as assinaturas aparecem em lista, cada nome é um link para a sua, o
   "Abrir em outra aba" segue valendo e o passo 2 mostra os três tutoriais um
   embaixo do outro. */
(function () {
  "use strict";
  var raiz = document.documentElement;
  var pessoas = {};
  Array.prototype.forEach.call(document.querySelectorAll(".pessoa"), function (a) {
    pessoas[a.id] = a;
  });
  var itens = Array.prototype.slice.call(document.querySelectorAll("#nomes li"));
  var busca = document.getElementById("busca");
  var nada = document.getElementById("nada");
  var vazia = document.getElementById("vazia");
  var baixar = document.getElementById("baixar");
  var baixarDica = document.getElementById("baixar-dica");
  var escolhida = null;

  function semAcento(s) {
    return s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
  }

  // ---- busca: filtra os nomes enquanto digita (sem acento, palavras em qualquer ordem)
  itens.forEach(function (li) { li.setAttribute("data-busca", semAcento(li.textContent)); });
  busca.addEventListener("input", function () {
    var termos = semAcento(busca.value).split(/\s+/).filter(Boolean);
    var achados = 0;
    itens.forEach(function (li) {
      var texto = li.getAttribute("data-busca");
      li.hidden = !termos.every(function (t) { return texto.indexOf(t) !== -1; });
      if (!li.hidden) achados++;
    });
    nada.hidden = achados > 0;
  });
  // Enter escolhe o primeiro que sobrou
  busca.addEventListener("keydown", function (e) {
    if (e.key !== "Enter") return;
    var primeiro = itens.filter(function (li) { return !li.hidden; })[0];
    if (primeiro) {
      e.preventDefault();
      primeiro.querySelector("a").click();
    }
  });

  // ---- a escolha vive no endereço (#slug): o link pode ir direto para a
  // pessoa e o "voltar" do navegador funciona. #todas mostra todas
  // (conferência do deploy); outra âncora não mexe na escolha.
  function escolher(rolar) {
    var alvo = decodeURIComponent(location.hash.slice(1));
    var todas = alvo === "todas";
    if (alvo && !todas && !pessoas.hasOwnProperty(alvo)) return;
    escolhida = todas ? null : pessoas[alvo] || null;
    raiz.classList.toggle("todas", todas);
    Object.keys(pessoas).forEach(function (s) {
      pessoas[s].classList.toggle("ativa", pessoas[s] === escolhida);
    });
    itens.forEach(function (li) {
      var a = li.querySelector("a");
      if (escolhida && a.getAttribute("href") === "#" + escolhida.id) a.setAttribute("aria-current", "true");
      else a.removeAttribute("aria-current");
    });
    vazia.hidden = !!escolhida || todas;
    ajustarPrevias();
    if (baixar) {
      baixar.disabled = !escolhida;
      baixarDica.textContent = escolhida
        ? "Assinatura de " + escolhida.getAttribute("data-nome") + "."
        : "Antes, escolha seu nome no passo 1.";
    }
    if (escolhida && rolar) escolhida.scrollIntoView({ block: "start" });
  }
  window.addEventListener("hashchange", function () { escolher(true); });

  // ---- prévia: no celular a assinatura (600px) encolhe para caber na tela,
  // em vez de rolar de lado. O zoom fica na .escala, fora da <table> copiada.
  function ajustarPrevias() {
    Array.prototype.forEach.call(document.querySelectorAll(".previa"), function (p) {
      var largura = p.clientWidth;
      if (largura) p.firstElementChild.style.zoom = largura < 600 ? (largura / 600).toFixed(3) : "";
    });
  }
  window.addEventListener("resize", ajustarPrevias);

  // ---- copiar: a <table> da prévia é o próprio .html da pessoa (o mesmo do
  // "Abrir em outra aba"), então o que chega no e-mail é igual ao do
  // Ctrl+A/Ctrl+C de lá. Sem a API de área de transferência, cai para a
  // seleção + copiar do navegador, que é o mesmo caminho do Ctrl+C.
  function copiarSelecionando(el) {
    var sel = window.getSelection();
    var faixa = document.createRange();
    faixa.selectNode(el);
    sel.removeAllRanges();
    sel.addRange(faixa);
    var ok = false;
    try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
    sel.removeAllRanges();
    return ok;
  }

  function copiar(artigo) {
    var tabela = artigo.querySelector(".previa table");
    var retorno = artigo.querySelector(".retorno");
    var texto = Array.prototype.map.call(tabela.querySelectorAll("img"), function (i) { return i.alt; }).join("\n");
    function avisar(ok) {
      retorno.className = "retorno " + (ok ? "ok" : "erro");
      retorno.innerHTML = ok
        ? "<b>Copiada!</b> Agora cole no seu e-mail com <kbd>Ctrl</kbd> + <kbd>V</kbd>, seguindo o " +
          "<a href=\"#como-instalar\" data-rolar>passo 2</a>."
        : "Não deu para copiar por aqui. Use o <b>Abrir em outra aba</b> (veja como logo abaixo).";
    }
    if (navigator.clipboard && window.ClipboardItem) {
      navigator.clipboard.write([new ClipboardItem({
        "text/html": new Blob([tabela.outerHTML], { type: "text/html" }),
        "text/plain": new Blob([texto], { type: "text/plain" })
      })]).then(function () { avisar(true); }, function () { avisar(copiarSelecionando(tabela)); });
    } else {
      avisar(copiarSelecionando(tabela));
    }
  }

  // ---- Outlook clássico: baixa a assinatura como "Time Forte.htm", o arquivo
  // que o passo a passo manda trocar na pasta de assinaturas. O BOM e a meta
  // charset fazem o Outlook ler os acentos dos textos alternativos como UTF-8.
  function baixarArquivo() {
    if (!escolhida) return;
    var doc = "﻿<html>\n<head>\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">\n" +
              "</head>\n<body>\n" + escolhida.querySelector(".previa table").outerHTML + "\n</body>\n</html>\n";
    var url = URL.createObjectURL(new Blob([doc], { type: "text/html;charset=utf-8" }));
    var a = document.createElement("a");
    a.href = url;
    a.download = "Time Forte.htm";
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 4000);
  }
  if (baixar) baixar.addEventListener("click", baixarArquivo);

  document.addEventListener("click", function (e) {
    if (!e.target.closest) return;
    var botao = e.target.closest(".copiar");
    if (botao) copiar(botao.closest(".pessoa"));
    // links internos que só rolam a página, sem trocar a pessoa do endereço
    var link = e.target.closest("a[data-rolar]");
    if (link) {
      var destino = document.getElementById(link.getAttribute("href").slice(1));
      if (destino) {
        e.preventDefault();
        destino.scrollIntoView({ block: "start" });
      }
    }
  });

  // ---- passo 2: abas Gmail / Outlook novo / Outlook clássico. A última
  // escolhida fica guardada neste navegador.
  var abas = Array.prototype.slice.call(document.querySelectorAll(".aba"));
  function abrirAba(aba, focar) {
    abas.forEach(function (t) {
      var sel = t === aba;
      t.setAttribute("aria-selected", sel ? "true" : "false");
      t.tabIndex = sel ? 0 : -1;
      document.getElementById(t.getAttribute("aria-controls")).hidden = !sel;
    });
    if (focar) aba.focus();
  }
  abas.forEach(function (t, i) {
    t.addEventListener("click", function () {
      abrirAba(t);
      try { localStorage.setItem("tf-assinatura-aba", t.id); } catch (e) { /* sem armazenamento: tudo bem */ }
    });
    t.addEventListener("keydown", function (e) {
      var passo = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
      if (!passo) return;
      e.preventDefault();
      abrirAba(abas[(i + passo + abas.length) % abas.length], true);
    });
  });
  var guardada = null;
  try { guardada = localStorage.getItem("tf-assinatura-aba"); } catch (e) { guardada = null; }
  abrirAba(abas.filter(function (t) { return t.id === guardada; })[0] || abas[0]);

  escolher(true);
})();
