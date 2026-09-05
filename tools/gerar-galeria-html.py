#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monta o HTML da galeria a partir do galeria.json.

Faz duas coisas:
  1. Escolhe N fotos variadas para a vitrine da pagina inicial e escreve o
     bloco entre os marcadores <!-- GALERIA:INICIO --> e <!-- GALERIA:FIM -->
     do index.html
  2. Gera a pagina galeria.html com todas as fotos

Uso:
    python tools/gerar-galeria-html.py                 # sorteio padrao
    python tools/gerar-galeria-html.py --semente 7     # outro sorteio
    python tools/gerar-galeria-html.py --destaques 12  # mais fotos na home
"""

import argparse
import json
import os
import random
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFESTO = os.path.join(RAIZ, "Client", "Public", "Src", "Assets",
                         "otimizadas", "galeria.json")
PAGINAS = os.path.join(RAIZ, "Client", "Public", "Src", "Pages")
INDEX = os.path.join(PAGINAS, "index.html")
GALERIA = os.path.join(PAGINAS, "galeria.html")

MARCA_INICIO = "<!-- GALERIA:INICIO -->"
MARCA_FIM = "<!-- GALERIA:FIM -->"

# Quantas fotos aparecem de cara na pagina de todas as fotos.
PRIMEIRO_LOTE = 48

ALT_PADRAO = "Doce artesanal feito à mão pela Dolce Vita Di Sandi em Sorocaba"


def cartao(foto, indice, sizes, classe_extra="", lazy=True, alt=None):
    """Um item da galeria: botão que abre o lightbox."""
    classe = "gallery-item " + foto["formato"]
    if classe_extra:
        classe += " " + classe_extra
    carregamento = ' loading="lazy" decoding="async"' if lazy else ' decoding="async"'
    return (
        '                    <li class="%s">\n'
        '                        <button type="button" class="gallery-botao"\n'
        '                            data-grande="%s" data-indice="%d">\n'
        '                            <picture>\n'
        '                                <source type="image/webp" srcset="%s">\n'
        '                                <img class="gallery-image" src="%s"\n'
        '                                    width="%d" height="%d"%s\n'
        '                                    alt="%s">\n'
        '                            </picture>\n'
        '                            <span class="sr-only">Abrir foto em tamanho grande</span>\n'
        '                        </button>\n'
        '                    </li>\n'
        % (classe, foto["grande"], indice, foto["mini"], foto["miniJpg"],
           foto["largura"], foto["altura"], carregamento, alt or ALT_PADRAO)
    )


def escolher_destaques(fotos, quantidade, semente):
    """
    Sorteia fotos espalhadas por toda a coleção, garantindo variedade de
    formato — o grid fica com ritmo em vez de uma coluna só de retratos.
    """
    rnd = random.Random(semente)
    paisagens = [f for f in fotos if f["formato"] != "retrato"]
    retratos = [f for f in fotos if f["formato"] == "retrato"]

    escolhidas = []
    # Até 3 fotos deitadas dão respiro ao bento.
    alvo_paisagem = min(3, len(paisagens), max(1, quantidade // 4))
    escolhidas += rnd.sample(paisagens, alvo_paisagem) if paisagens else []

    # O resto vem dos retratos, mas pescados em faixas diferentes da coleção
    # para não sair tudo do mesmo dia/evento.
    faltam = quantidade - len(escolhidas)
    if retratos and faltam > 0:
        blocos = max(1, len(retratos) // faltam)
        for i in range(faltam):
            fatia = retratos[i * blocos:(i + 1) * blocos] or retratos
            escolhidas.append(rnd.choice(fatia))

    # Remove repetição e completa se faltou
    vistos = set()
    unicas = []
    for f in escolhidas:
        if f["id"] not in vistos:
            vistos.add(f["id"])
            unicas.append(f)
    for f in rnd.sample(fotos, len(fotos)):
        if len(unicas) >= quantidade:
            break
        if f["id"] not in vistos:
            vistos.add(f["id"])
            unicas.append(f)

    rnd.shuffle(unicas)
    return unicas[:quantidade]


def bloco_home(destaques, total):
    sizes = "(max-width: 700px) 50vw, 25vw"
    itens = "".join(cartao(f, i, sizes) for i, f in enumerate(destaques))
    return (
        '%s\n'
        '                <ul class="gallery-list revelar" id="galeria">\n'
        '%s'
        '                </ul>\n'
        '\n'
        '                <div class="galeria-rodape revelar">\n'
        '                    <p>Estas são só %d de <strong>%d fotos</strong> de doces que\n'
        '                        já saíram da nossa cozinha.</p>\n'
        '                    <div class="buttons">\n'
        '                        <a class="button button-linha-clara" href="/Client/Public/Src/Pages/galeria.html">\n'
        '                            Ver todas as %d fotos\n'
        '                        </a>\n'
        '                        <a class="button order-now"\n'
        '                            href="https://wa.me/5515991291842?text=Ol%%C3%%A1!%%20Vi%%20as%%20fotos%%20no%%20site%%20e%%20fiquei%%20com%%20vontade%%20%%F0%%9F%%98%%8B"\n'
        '                            target="_blank" rel="noopener">\n'
        '                            <svg class="icone" aria-hidden="true">\n'
        '                                <use href="#i-whatsapp" />\n'
        '                            </svg>\n'
        '                            Quero um desses\n'
        '                        </a>\n'
        '                    </div>\n'
        '                </div>\n'
        '                %s'
        % (MARCA_INICIO, itens, len(destaques), total, total, MARCA_FIM)
    )


CABECALHO_GALERIA = '''<!DOCTYPE html>
<html lang="pt-BR">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="theme-color" content="#4E342E">
    <title>Galeria | Dolce Vita Di Sandi — %(total)d fotos dos nossos doces</title>
    <meta name="description"
        content="%(total)d fotos reais dos doces artesanais feitos pela Dolce Vita Di Sandi em Sorocaba/SP: tortas, beliscão, cookies, doce de paçoca e encomendas de festa.">
    <link rel="canonical" href="https://dolcevitadisandi.com.br/Client/Public/Src/Pages/galeria.html">
    <link rel="icon" href="/Client/Public/Src/Assets/otimizadas/menu/menu-torta-01-480w.png" sizes="any">

    <meta property="og:type" content="website">
    <meta property="og:title" content="Galeria | Dolce Vita Di Sandi">
    <meta property="og:description"
        content="%(total)d fotos reais dos doces feitos à mão pela Sanderly em Sorocaba.">
    <meta property="og:image" content="https://dolcevitadisandi.com.br%(capa)s">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet"
        href="https://fonts.googleapis.com/css2?family=Sacramento&family=Poppins:wght@400;500;600;700&display=swap">
    <link rel="stylesheet" href="/Client/Public/Src/Styles/styles.css">
</head>

<body>
    <svg class="sprite" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg">
        <symbol id="i-seta-esq" viewBox="0 0 24 24">
            <path d="M15.4 4.6 8 12l7.4 7.4 1.4-1.4L10.8 12l6-6z" />
        </symbol>
        <symbol id="i-seta-dir" viewBox="0 0 24 24">
            <path d="M8.6 19.4 16 12 8.6 4.6 7.2 6l6 6-6 6z" />
        </symbol>
        <symbol id="i-fechar" viewBox="0 0 24 24">
            <path
                d="M18.3 5.7 12 12l6.3 6.3-1.4 1.4L10.6 13.4 4.3 19.7 2.9 18.3 9.2 12 2.9 5.7l1.4-1.4L10.6 10.6l6.3-6.3z" />
        </symbol>
        <symbol id="i-whatsapp" viewBox="0 0 24 24">
            <path
                d="M12 2a10 10 0 0 0-8.6 15L2 22l5.2-1.4A10 10 0 1 0 12 2zm0 18a8 8 0 0 1-4.1-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8 8 0 1 1 12 20zm4.5-5.9c-.2-.1-1.4-.7-1.6-.8s-.4-.1-.6.1-.6.8-.8 1-.3.2-.6.1a6.5 6.5 0 0 1-3.2-2.8c-.2-.4.2-.4.6-1.2a.6.6 0 0 0 0-.6c0-.1-.6-1.4-.8-1.9s-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 2.9 2.9 0 0 0-.9 2.2 5 5 0 0 0 1.1 2.7 11.5 11.5 0 0 0 4.4 3.9c1.6.6 2.2.7 3 .6a2.6 2.6 0 0 0 1.7-1.2 2.1 2.1 0 0 0 .1-1.2c0-.1-.2-.2-.5-.3z" />
        </symbol>
    </svg>

    <a class="pular-para-conteudo" href="#conteudo">Pular para o conteúdo</a>

    <header>
        <nav class="navbar" aria-label="Navegação principal">
            <a href="/Client/Public/Src/Pages/index.html" class="nav-logo">
                <h2 class="logo"><span class="coracao" aria-hidden="true">♥</span> Dolce Vita Di Sandi</h2>
            </a>
            <ul class="nav-menu">
                <li class="nav-item"><a href="/Client/Public/Src/Pages/index.html" class="nav-link">Voltar ao site</a>
                </li>
                <li class="nav-item nav-cta">
                    <a class="button order-now button-pequeno"
                        href="https://wa.me/5515991291842?text=Ol%%C3%%A1!%%20Vi%%20a%%20galeria%%20no%%20site%%20e%%20queria%%20fazer%%20um%%20pedido%%20%%F0%%9F%%8D%%B0"
                        target="_blank" rel="noopener">
                        <svg class="icone" aria-hidden="true">
                            <use href="#i-whatsapp" />
                        </svg>
                        Peça agora
                    </a>
                </li>
            </ul>
        </nav>
    </header>

    <main class="pagina-interna" id="conteudo">
        <div class="section-content">
            <a class="voltar" href="/Client/Public/Src/Pages/index.html">
                <svg class="icone" aria-hidden="true">
                    <use href="#i-seta-esq" />
                </svg>
                Voltar para a página inicial
            </a>

            <div class="centralizado">
                <p class="olho">Galeria completa</p>
                <h1 class="section-title">Dez anos de doce, em %(total)d fotos</h1>
                <p class="section-intro">
                    Tudo aqui saiu da cozinha da Sanderly, em Sorocaba. São fotos reais,
                    tiradas no dia da encomenda — sem banco de imagens, sem produção.
                    Clique em qualquer uma para ver de perto.
                </p>
            </div>

            <p class="galeria-contador" id="galeria-contador">
                Mostrando <span id="galeria-mostrando">%(lote)d</span> de %(total)d fotos
            </p>

            <ul class="gallery-list galeria-completa" id="galeria">
'''

RODAPE_GALERIA = '''            </ul>

            <div class="carregar-mais" id="carregar-mais-area">
                <button type="button" class="button button-linha-clara" id="carregar-mais">
                    Carregar mais fotos
                </button>
            </div>
        </div>
    </main>

    <section class="faixa-cta">
        <div class="section-content">
            <h2>Bateu vontade?</h2>
            <p>
                Todos esses doces já foram encomenda de alguém. O próximo pode ser o seu —
                é só mandar uma mensagem que a Sanderly responde pessoalmente.
            </p>
            <div class="buttons">
                <a class="button order-now"
                    href="https://wa.me/5515991291842?text=Ol%%C3%%A1!%%20Vi%%20a%%20galeria%%20e%%20queria%%20encomendar%%20%%F0%%9F%%92%%97"
                    target="_blank" rel="noopener">
                    <svg class="icone" aria-hidden="true">
                        <use href="#i-whatsapp" />
                    </svg>
                    Fazer meu pedido
                </a>
                <a class="button contact-us" href="/Client/Public/Src/Pages/cardapio.html">Ver o cardápio</a>
            </div>
            <p class="reforco">Resposta no mesmo dia · Encomendas de torta com 48 h de antecedência</p>
        </div>
    </section>

    <footer class="footer-section">
        <div class="section-content">
            <div class="footer-base">
                <p class="copyright-text">© 2026 Dolce Vita Di Sandi — Sorocaba/SP</p>
                <p class="policy-text">
                    <a href="/Client/Public/Src/Pages/politica-de-privacidade.html" class="policy-link">Política de
                        Privacidade</a>
                    <span class="separator" aria-hidden="true">•</span>
                    <a href="/Client/Public/Src/Pages/politica-de-reembolso.html" class="policy-link">Política de
                        Reembolso</a>
                </p>
            </div>
        </div>
    </footer>

    <a class="whatsapp-flutuante"
        href="https://wa.me/5515991291842?text=Ol%%C3%%A1!%%20Vi%%20a%%20galeria%%20no%%20site%%20e%%20queria%%20fazer%%20um%%20pedido%%20%%F0%%9F%%8D%%B0"
        target="_blank" rel="noopener" aria-label="Falar no WhatsApp com a Dolce Vita Di Sandi">
        <svg class="icone" aria-hidden="true">
            <use href="#i-whatsapp" />
        </svg>
        <span class="rotulo">Pedir no WhatsApp</span>
    </a>

    <dialog class="lightbox" id="lightbox" aria-label="Foto ampliada">
        <button type="button" class="lightbox-botao lightbox-fechar" id="lightbox-fechar" aria-label="Fechar">
            <svg class="icone" aria-hidden="true">
                <use href="#i-fechar" />
            </svg>
        </button>
        <button type="button" class="lightbox-botao lightbox-anterior" id="lightbox-anterior"
            aria-label="Foto anterior">
            <svg class="icone" aria-hidden="true">
                <use href="#i-seta-esq" />
            </svg>
        </button>
        <button type="button" class="lightbox-botao lightbox-proximo" id="lightbox-proximo" aria-label="Próxima foto">
            <svg class="icone" aria-hidden="true">
                <use href="#i-seta-dir" />
            </svg>
        </button>
        <div>
            <img id="lightbox-img" alt="">
            <p class="lightbox-legenda" id="lightbox-legenda"></p>
        </div>
    </dialog>

    <script src="/Client/Public/Src/Js/script.js" defer></script>
</body>

</html>
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--semente", type=int, default=2015,
                    help="muda o sorteio das fotos da home")
    ap.add_argument("--destaques", type=int, default=10,
                    help="quantas fotos aparecem na home")
    args = ap.parse_args()

    if not os.path.exists(MANIFESTO):
        sys.exit("Rode antes:  python tools/processar-galeria.py")
    with open(MANIFESTO, encoding="utf-8") as f:
        dados = json.load(f)
    fotos = dados["fotos"]
    total = len(fotos)
    print("Fotos disponiveis: %d" % total)

    # ---- 1. vitrine da home ----
    destaques = escolher_destaques(fotos, args.destaques, args.semente)
    with open(INDEX, encoding="utf-8") as f:
        html = f.read()
    if MARCA_INICIO not in html or MARCA_FIM not in html:
        sys.exit("Marcadores GALERIA:INICIO/FIM nao encontrados no index.html")
    antes = html[:html.index(MARCA_INICIO)]
    depois = html[html.index(MARCA_FIM) + len(MARCA_FIM):]
    with open(INDEX, "w", encoding="utf-8") as f:
        f.write(antes + bloco_home(destaques, total) + depois)
    print("index.html: %d fotos em destaque (semente %d)"
          % (len(destaques), args.semente))
    for d in destaques:
        print("   %s  %s" % (d["id"], d["formato"]))

    # ---- 2. pagina com todas ----
    sizes = "(max-width: 700px) 50vw, (max-width: 1000px) 33vw, 25vw"
    partes = []
    for i, foto in enumerate(fotos):
        extra = "" if i < PRIMEIRO_LOTE else "oculto"
        partes.append(cartao(foto, i, sizes, classe_extra=extra,
                             lazy=True).replace('<li class="gallery-item',
                                                '<li class="gallery-item'))
    corpo = "".join(partes)
    capa = destaques[0]["grande"] if destaques else fotos[0]["grande"]
    with open(GALERIA, "w", encoding="utf-8") as f:
        f.write((CABECALHO_GALERIA % {"total": total, "capa": capa,
                                      "lote": min(PRIMEIRO_LOTE, total)})
                + corpo + RODAPE_GALERIA)
    print("galeria.html: %d fotos (%d visiveis de inicio)"
          % (total, min(PRIMEIRO_LOTE, total)))


if __name__ == "__main__":
    main()
