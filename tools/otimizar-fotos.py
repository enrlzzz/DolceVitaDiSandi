#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Otimizador de fotos da Dolce Vita Di Sandi.

Le as fotos originais de /raw-photos, gera versoes leves (WebP + JPEG de
fallback) em varios tamanhos dentro de Client/Public/Src/Assets/otimizadas/
e escreve um manifesto JSON com os caminhos prontos para o srcset.

Uso:
    python tools/otimizar-fotos.py                   # processa /raw-photos
    python tools/otimizar-fotos.py --incluir-atuais  # tambem reotimiza os
                                                     # assets ja usados no site

Requisito unico: Pillow  ->  pip install Pillow
Passo a passo completo em raw-photos/README-fotos.md
"""

import argparse
import json
import os
import re
import sys

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("Pillow nao encontrado. Rode:  pip install Pillow")

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRADA = os.path.join(RAIZ, "raw-photos")
SAIDA = os.path.join(RAIZ, "Client", "Public", "Src", "Assets", "otimizadas")
MANIFESTO = os.path.join(SAIDA, "manifesto.json")
URL_BASE = "/Client/Public/Src/Assets/otimizadas"

# Larguras geradas para o srcset. Cobrem de 360px ate telas grandes.
LARGURAS = [480, 800, 1200, 1600]

# WebP em 82 fica visualmente identico ao original e pesa uma fracao.
Q_WEBP = 82
Q_JPEG = 82

EXTENSOES = (".jpg", ".jpeg", ".png", ".webp")

# Convencao de nome:  <secao>-<produto>-<numero>
# Ex.: menu-cafe-01.jpg / galeria-torta-holandesa-02.jpg / equipe-sanderly-01.jpg
PADRAO_NOME = re.compile(r"^(menu|galeria|equipe|hero)-([a-z0-9-]+)-(\d{2,})$")

# Proporcao alvo por secao. None = preserva a proporcao original.
# A galeria nao recorta: o layout bento + object-fit: cover cuidam disso.
PROPORCAO = {
    "menu": (1, 1),      # cards quadrados
    "equipe": (4, 5),    # retrato
    "hero": None,
    "galeria": None,
}


def slug(texto):
    texto = texto.lower().strip()
    texto = re.sub(r"[^a-z0-9]+", "-", texto)
    return texto.strip("-")


def recortar_para(img, proporcao):
    """Recorte central respeitando a proporcao pedida, sem distorcer nada."""
    if proporcao is None:
        return img
    alvo = proporcao[0] / proporcao[1]
    largura, altura = img.size
    atual = largura / altura
    if abs(atual - alvo) < 0.01:
        return img
    if atual > alvo:                       # larga demais -> corta as laterais
        nova = int(altura * alvo)
        x = (largura - nova) // 2
        return img.crop((x, 0, x + nova, altura))
    nova = int(largura / alvo)             # alta demais -> corta topo e base
    y = (altura - nova) // 2
    return img.crop((0, y, largura, y + nova))


def processar(caminho, secao_padrao=None):
    nome = os.path.splitext(os.path.basename(caminho))[0]
    base = slug(nome)
    achado = PADRAO_NOME.match(base)
    if achado:
        secao = achado.group(1)
    elif secao_padrao:
        secao = secao_padrao
        base = secao + "-" + base
    else:
        print("  ! %s ignorado: nome fora da convencao "
              "<secao>-<produto>-<numero>" % os.path.basename(caminho))
        return None

    img = Image.open(caminho)
    img = ImageOps.exif_transpose(img)           # respeita a rotacao do celular
    tem_alpha = img.mode in ("RGBA", "LA") or (
        img.mode == "P" and "transparency" in img.info)
    img = img.convert("RGBA" if tem_alpha else "RGB")
    img = recortar_para(img, PROPORCAO.get(secao))

    largura, altura = img.size
    tamanhos = [w for w in LARGURAS if w <= largura]
    if not tamanhos:
        tamanhos = [largura]

    destino = os.path.join(SAIDA, secao)
    os.makedirs(destino, exist_ok=True)

    entrada = {
        "id": base,
        "arquivo": os.path.basename(caminho),
        "secao": secao,
        "largura": largura,
        "altura": altura,
        "proporcao": round(largura / altura, 4),
        "webp": [],
        "jpeg": [],
    }

    for w in sorted(set(tamanhos)):
        h = max(1, round(altura * w / largura))
        pequena = img.resize((w, h), Image.LANCZOS)

        pequena.save(os.path.join(destino, "%s-%dw.webp" % (base, w)),
                     "WEBP", quality=Q_WEBP, method=6)
        entrada["webp"].append(
            {"url": "%s/%s/%s-%dw.webp" % (URL_BASE, secao, base, w), "w": w})

        if tem_alpha:
            # Fallback com transparencia preservada: PNG quantizado no mesmo
            # tamanho. Nada de PNG em resolucao cheia - e o que pesava 900 KB.
            fallback = pequena.quantize(colors=192, method=Image.FASTOCTREE)
            fallback.save(os.path.join(destino, "%s-%dw.png" % (base, w)),
                          "PNG", optimize=True)
            entrada["jpeg"].append(
                {"url": "%s/%s/%s-%dw.png" % (URL_BASE, secao, base, w), "w": w})
        else:
            pequena.save(os.path.join(destino, "%s-%dw.jpg" % (base, w)),
                         "JPEG", quality=Q_JPEG, optimize=True, progressive=True)
            entrada["jpeg"].append(
                {"url": "%s/%s/%s-%dw.jpg" % (URL_BASE, secao, base, w), "w": w})

    entrada["transparente"] = tem_alpha

    print("  + %-32s %4dx%-4d -> %d tamanhos" % (base, largura, altura, len(tamanhos)))
    return entrada


def bloco_html(entrada, alt="", classe="", sizes="(max-width: 700px) 100vw, 33vw",
               lazy=True):
    """Bloco <picture> pronto para colar no HTML."""
    webp = ", ".join("%s %dw" % (i["url"], i["w"]) for i in entrada["webp"])
    jpeg = ", ".join("%s %dw" % (i["url"], i["w"]) for i in entrada["jpeg"])
    maior = entrada["jpeg"][-1]["url"]
    return (
        '<picture>\n'
        '  <source type="image/webp" srcset="%s" sizes="%s">\n'
        '  <img src="%s" srcset="%s" sizes="%s"\n'
        '       width="%d" height="%d" alt="%s" class="%s"%s>\n'
        '</picture>'
        % (webp, sizes, maior, jpeg, sizes, entrada["largura"], entrada["altura"],
           alt, classe, ' loading="lazy" decoding="async"' if lazy else ""))


# Assets que ja estao no site, mapeados para a convencao de nomes nova.
ATUAIS = {
    "morango.png": "hero-morango-01",
    "about-image.jpg": "galeria-vitrine-01",
    "user-2.png": "equipe-sanderly-01",
    "foto4.jpg": "equipe-enrico-01",
    "img1.jpg": "galeria-doce-01",
    "img2.jpg": "galeria-doce-02",
    "img3.jpg": "galeria-doce-03",
    "img4.jpg": "galeria-doce-04",
    "img5.jpg": "galeria-doce-05",
    "img6.jpg": "galeria-doce-06",
    "cafe.png": "menu-cafe-01",
    "beliscao.png": "menu-beliscao-01",
    "cake.png": "menu-torta-01",
    "cookies.png": "menu-cookies-01",
    "soda.png": "menu-soda-01",
    "pacoca.png": "menu-pacoca-01",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--incluir-atuais", action="store_true",
                    help="reotimiza tambem os assets que ja estao no site")
    args = ap.parse_args()

    os.makedirs(SAIDA, exist_ok=True)
    manifesto = {}
    if os.path.exists(MANIFESTO):
        with open(MANIFESTO, encoding="utf-8") as f:
            manifesto = json.load(f)

    print("Lendo /raw-photos ...")
    achou = False
    for pasta, _, arquivos in os.walk(ENTRADA):
        atual = os.path.basename(pasta)
        secao_padrao = atual if atual in PROPORCAO else None
        for arq in sorted(arquivos):
            if not arq.lower().endswith(EXTENSOES):
                continue
            achou = True
            entrada = processar(os.path.join(pasta, arq), secao_padrao)
            if entrada:
                manifesto[entrada["id"]] = entrada
    if not achou:
        print("  (nenhuma foto nova - veja raw-photos/README-fotos.md)")

    if args.incluir_atuais:
        print("Reotimizando os assets atuais do site ...")
        # Os originais podem estar na pasta antiga ou em index/ (layout do deploy)
        pastas = [os.path.join(RAIZ, "Client", "Public", "Src", "Assets"),
                  os.path.join(RAIZ, "index")]
        for origem, novo in sorted(ATUAIS.items()):
            caminho = next((os.path.join(d, origem) for d in pastas
                            if os.path.exists(os.path.join(d, origem))), None)
            if caminho is None:
                continue
            ext = os.path.splitext(origem)[1]
            tmp = os.path.join(SAIDA, novo + ext)
            Image.open(caminho).save(tmp)
            entrada = processar(tmp)
            os.remove(tmp)
            if entrada:
                entrada["arquivo"] = origem
                manifesto[entrada["id"]] = entrada

    with open(MANIFESTO, "w", encoding="utf-8") as f:
        json.dump(manifesto, f, ensure_ascii=False, indent=2, sort_keys=True)

    print("\nManifesto salvo: %s (%d fotos)" % (MANIFESTO, len(manifesto)))
    if manifesto:
        exemplo = sorted(manifesto)[0]
        print("\nExemplo de bloco pronto para colar no HTML:\n")
        print(bloco_html(manifesto[exemplo],
                         alt="Doce artesanal da Dolce Vita Di Sandi",
                         classe="gallery-image"))


if __name__ == "__main__":
    main()
