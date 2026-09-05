#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prepara as fotos da galeria da Dolce Vita Di Sandi.

O que ele faz, em ordem:
  1. Le tudo que estiver em raw-photos/galeria/
  2. Corrige a rotacao do celular (EXIF)
  3. Descarta fotos tremidas e fotos repetidas (as rajadas de 3-4 cliques
     seguidos viram uma foto so: a mais nitida do grupo)
  4. Gera versoes leves em WebP (miniatura + tamanho de visualizacao)
  5. Escreve Client/Public/Src/Assets/otimizadas/galeria.json, que e o que as
     paginas do site consomem

Uso:
    python tools/processar-galeria.py
    python tools/processar-galeria.py --limite 40      # teste rapido
    python tools/processar-galeria.py --sem-dedupe     # mantem tudo

Requisitos: Pillow e numpy.
"""

import argparse
import json
import os
import sys

import numpy as np

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("Pillow nao encontrado. Rode:  pip install Pillow")

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRADA = os.path.join(RAIZ, "raw-photos", "galeria")
SAIDA = os.path.join(RAIZ, "Client", "Public", "Src", "Assets", "otimizadas", "galeria")
MANIFESTO = os.path.join(os.path.dirname(SAIDA), "galeria.json")
URL_BASE = "/Client/Public/Src/Assets/otimizadas/galeria"

MINIATURA = 480          # o que aparece no grid
VISUALIZACAO = 1100      # o que abre no lightbox
Q_MINIATURA = 78
Q_VISUALIZACAO = 80

# Fotos com nitidez abaixo disso estao tremidas ou desfocadas demais.
NITIDEZ_MINIMA = 55.0
# Distancia de hash abaixo disso = mesma foto (rajada / print repetido).
DISTANCIA_IGUAL = 6

# Imagens que nao sao doces da Sanderly: ilustracoes de banco de imagem que o
# Enrico baixou para o heroi. Ficam de fora da galeria.
IGNORAR = {
    "strawberry-berry-levitating-white-background.jpg",
    "floating-fruit-splash.jpg",
    "fruit-splash-illustration-with-juice.jpg",
}

EXTENSOES = (".jpg", ".jpeg", ".png", ".webp")


def hash_medio(img):
    """Assinatura de 64 bits da foto: fotos parecidas geram hashes parecidos."""
    pequena = img.convert("L").resize((8, 8), Image.LANCZOS)
    arr = np.asarray(pequena, dtype=np.float32)
    return (arr > arr.mean()).flatten()


def distancia(a, b):
    return int(np.count_nonzero(a != b))


def nitidez(img):
    """Variancia do gradiente numa versao reduzida: detecta foto tremida."""
    pequena = img.convert("L")
    pequena.thumbnail((480, 480), Image.LANCZOS)
    arr = np.asarray(pequena, dtype=np.float32)
    gy, gx = np.gradient(arr)
    return float(np.hypot(gx, gy).var())


def formato(largura, altura):
    proporcao = largura / altura
    if proporcao > 1.25:
        return "paisagem"
    if proporcao < 0.8:
        return "retrato"
    return "quadrada"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limite", type=int, default=0,
                    help="processa apenas as N primeiras (para testar)")
    ap.add_argument("--sem-dedupe", action="store_true",
                    help="nao remove fotos repetidas nem tremidas")
    args = ap.parse_args()

    if not os.path.isdir(ENTRADA):
        sys.exit("Pasta nao encontrada: %s" % ENTRADA)
    os.makedirs(SAIDA, exist_ok=True)

    arquivos = sorted(f for f in os.listdir(ENTRADA)
                      if f.lower().endswith(EXTENSOES) and f not in IGNORAR)
    if args.limite:
        arquivos = arquivos[:args.limite]
    print("Fotos encontradas: %d\n" % len(arquivos))

    print("Etapa 1/3 — lendo e avaliando cada foto")
    fichas = []
    for i, nome in enumerate(arquivos, start=1):
        caminho = os.path.join(ENTRADA, nome)
        try:
            img = Image.open(caminho)
            img = ImageOps.exif_transpose(img).convert("RGB")
        except Exception as erro:
            print("  ! %s ignorada (%s)" % (nome, erro))
            continue
        ficha = {
            "nome": nome,
            "tamanho": img.size,
            "nitidez": nitidez(img),
            "hash": hash_medio(img),
        }
        fichas.append(ficha)
        if i % 25 == 0 or i == len(arquivos):
            print("  %d/%d" % (i, len(arquivos)))

    if args.sem_dedupe:
        escolhidas = fichas
        print("\nEtapa 2/3 — pulada (--sem-dedupe)")
    else:
        print("\nEtapa 2/3 — descartando tremidas e repetidas")
        antes = len(fichas)
        nitidas = [f for f in fichas if f["nitidez"] >= NITIDEZ_MINIMA]
        print("  tremidas/desfocadas descartadas: %d" % (antes - len(nitidas)))

        # Dentro de cada grupo de fotos parecidas, fica a mais nitida.
        nitidas.sort(key=lambda f: f["nitidez"], reverse=True)
        escolhidas = []
        for ficha in nitidas:
            repetida = any(distancia(ficha["hash"], j["hash"]) <= DISTANCIA_IGUAL
                           for j in escolhidas)
            if not repetida:
                escolhidas.append(ficha)
        print("  repetidas descartadas: %d" % (len(nitidas) - len(escolhidas)))
        print("  sobraram: %d fotos distintas" % len(escolhidas))

    # Ordem final: pelo nome do arquivo, que nas fotos de celular e cronologico.
    escolhidas.sort(key=lambda f: f["nome"])

    print("\nEtapa 3/3 — gerando as versoes leves")
    itens = []
    for i, ficha in enumerate(escolhidas, start=1):
        caminho = os.path.join(ENTRADA, ficha["nome"])
        img = ImageOps.exif_transpose(Image.open(caminho)).convert("RGB")
        largura, altura = img.size
        base = "doce-%03d" % i

        mini = img.copy()
        mini.thumbnail((MINIATURA, MINIATURA), Image.LANCZOS)
        mini.save(os.path.join(SAIDA, "%s-m.webp" % base),
                  "WEBP", quality=Q_MINIATURA, method=6)
        mini.save(os.path.join(SAIDA, "%s-m.jpg" % base),
                  "JPEG", quality=Q_MINIATURA, optimize=True, progressive=True)

        grande = img.copy()
        grande.thumbnail((VISUALIZACAO, VISUALIZACAO), Image.LANCZOS)
        grande.save(os.path.join(SAIDA, "%s-g.webp" % base),
                    "WEBP", quality=Q_VISUALIZACAO, method=6)

        itens.append({
            "id": base,
            "origem": ficha["nome"],
            "largura": largura,
            "altura": altura,
            "formato": formato(largura, altura),
            "mini": "%s/%s-m.webp" % (URL_BASE, base),
            "miniJpg": "%s/%s-m.jpg" % (URL_BASE, base),
            "grande": "%s/%s-g.webp" % (URL_BASE, base),
        })
        if i % 20 == 0 or i == len(escolhidas):
            print("  %d/%d" % (i, len(escolhidas)))

    with open(MANIFESTO, "w", encoding="utf-8") as f:
        json.dump({"total": len(itens), "fotos": itens}, f,
                  ensure_ascii=False, indent=1)

    peso = sum(os.path.getsize(os.path.join(SAIDA, a))
               for a in os.listdir(SAIDA)) / (1024 * 1024)
    contagem = {}
    for it in itens:
        contagem[it["formato"]] = contagem.get(it["formato"], 0) + 1

    print("\nPronto.")
    print("  %d fotos no manifesto  (%s)" % (len(itens), contagem))
    print("  %.1f MB em %s" % (peso, SAIDA))
    print("  manifesto: %s" % MANIFESTO)


if __name__ == "__main__":
    main()
