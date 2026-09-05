#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Recorta os morangos da foto de fundo branco em camadas PNG/WebP transparentes,
para montar a cena 3D do heroi.

Por que nao basta "apagar o que for claro": a polpa do morango fatiado tambem e
clara, e sumiria junto. Aqui o fundo e definido como o branco DESSATURADO que
esta conectado a borda da imagem — a polpa, por estar cercada de fruta, fica.

Entrada : raw-photos/galeria/strawberry-berry-levitating-white-background.jpg
Saida   : Client/Public/Src/Assets/otimizadas/hero/morango-<n>-<w>w.webp/.png

Uso: python tools/recortar-heroi.py
"""

import os
import sys
from collections import deque

import numpy as np

try:
    from PIL import Image, ImageFilter
except ImportError:
    sys.exit("Pillow nao encontrado. Rode:  pip install Pillow")

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGEM = os.path.join(RAIZ, "raw-photos", "galeria",
                      "strawberry-berry-levitating-white-background.jpg")
SAIDA = os.path.join(RAIZ, "Client", "Public", "Src", "Assets", "otimizadas", "hero")

TRABALHO = 1800          # resolucao de trabalho; sobra para telas grandes
VALOR_MIN = 205          # abaixo disso o pixel e escuro demais para ser fundo
SATURACAO_MAX = 38       # acima disso tem cor: e fruta, nao fundo
RAMPA = 26               # suavizacao da borda, em niveis
ESCALA_BUSCA = 4         # o alagamento roda numa versao reduzida (rapido)
AREA_MINIMA = 0.004      # regioes menores que isso sao respingos/bokeh
LARGURAS = [480, 800, 1200]


def mascara_branco(arr):
    """Quao "branco de estudio" cada pixel e: claro e sem cor."""
    maximo = arr.max(axis=2).astype(np.int16)
    minimo = arr.min(axis=2).astype(np.int16)
    saturacao = maximo - minimo
    return (maximo >= VALOR_MIN) & (saturacao <= SATURACAO_MAX)


def alagar_das_bordas(mascara):
    """Marca so o branco conectado a moldura da imagem."""
    altura, largura = mascara.shape
    visitado = np.zeros((altura, largura), dtype=bool)
    fila = deque()

    def semear(y, x):
        if mascara[y, x] and not visitado[y, x]:
            visitado[y, x] = True
            fila.append((y, x))

    for x in range(largura):
        semear(0, x)
        semear(altura - 1, x)
    for y in range(altura):
        semear(y, 0)
        semear(y, largura - 1)

    vizinhos = ((1, 0), (-1, 0), (0, 1), (0, -1))
    while fila:
        y, x = fila.popleft()
        for dy, dx in vizinhos:
            ny, nx = y + dy, x + dx
            if 0 <= ny < altura and 0 <= nx < largura \
                    and mascara[ny, nx] and not visitado[ny, nx]:
                visitado[ny, nx] = True
                fila.append((ny, nx))
    return visitado


def componentes(mascara, area_minima_px):
    """Rotula regioes conectadas sem depender de scipy."""
    altura, largura = mascara.shape
    rotulos = np.zeros((altura, largura), dtype=np.int32)
    achados = []
    atual = 0
    vizinhos = ((1, 0), (-1, 0), (0, 1), (0, -1))

    for y0 in range(altura):
        for x0 in range(largura):
            if not mascara[y0, x0] or rotulos[y0, x0]:
                continue
            atual += 1
            fila = deque([(y0, x0)])
            rotulos[y0, x0] = atual
            pixels = 0
            minx = maxx = x0
            miny = maxy = y0
            while fila:
                y, x = fila.popleft()
                pixels += 1
                minx = min(minx, x); maxx = max(maxx, x)
                miny = min(miny, y); maxy = max(maxy, y)
                for dy, dx in vizinhos:
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < altura and 0 <= nx < largura \
                            and mascara[ny, nx] and not rotulos[ny, nx]:
                        rotulos[ny, nx] = atual
                        fila.append((ny, nx))
            if pixels >= area_minima_px:
                achados.append({"id": atual, "pixels": pixels,
                                "caixa": (minx, miny, maxx + 1, maxy + 1)})
    return rotulos, achados


def nitidez(recorte_rgb, recorte_alpha):
    """Variancia do gradiente: separa a fruta em foco do bokeh do fundo."""
    cinza = np.asarray(recorte_rgb.convert("L"), dtype=np.float32)
    gy, gx = np.gradient(cinza)
    forca = np.hypot(gx, gy)
    dentro = recorte_alpha > 0.6
    if dentro.sum() < 50:
        return 0.0
    return float(forca[dentro].var())


def main():
    if not os.path.exists(ORIGEM):
        sys.exit("Nao encontrei a foto de origem:\n  %s" % ORIGEM)
    os.makedirs(SAIDA, exist_ok=True)

    print("Abrindo a foto original...")
    img = Image.open(ORIGEM).convert("RGB")
    print("  original: %dx%d" % img.size)
    img.thumbnail((TRABALHO, TRABALHO), Image.LANCZOS)
    largura, altura = img.size
    print("  trabalhando em: %dx%d" % (largura, altura))

    arr = np.asarray(img)
    branco = mascara_branco(arr)

    # Trabalha numa versao reduzida: mesma resposta, fracao do tempo.
    pequena = Image.fromarray((branco * 255).astype(np.uint8)).resize(
        (largura // ESCALA_BUSCA, altura // ESCALA_BUSCA), Image.NEAREST)
    branco_p = np.asarray(pequena) > 127
    print("Localizando o fundo (%dx%d)..." % pequena.size)

    # Nao basta alagar pelas bordas: o vao ENTRE dois morangos tambem e fundo,
    # mas fica cercado de fruta e o alagamento nunca chega la. Entao tratamos
    # como fundo toda regiao branca grande, esteja ela na borda ou no meio.
    # A polpa clara da fruta tem cor (rosa), nao entra na mascara de branco.
    total_p = branco_p.shape[0] * branco_p.shape[1]
    _, regioes_brancas = componentes(branco_p, int(total_p * 0.0006))
    fundo_p = np.zeros_like(branco_p)
    rotulos_p, _ = componentes(branco_p, 1)
    ids_fundo = set(r["id"] for r in regioes_brancas)
    if ids_fundo:
        fundo_p = np.isin(rotulos_p, list(ids_fundo))
    print("  %d regioes de fundo" % len(ids_fundo))

    # Volta ao tamanho de trabalho com uma folga, para nao serrilhar a borda.
    fundo_img = Image.fromarray((fundo_p * 255).astype(np.uint8)).resize(
        (largura, altura), Image.NEAREST).filter(ImageFilter.MaxFilter(5))
    fundo = np.asarray(fundo_img) > 127

    # Alpha: rampa suave pelo quanto o pixel e branco, mas so onde e fundo.
    maximo = arr.max(axis=2).astype(np.float32)
    suave = np.clip((maximo - (VALOR_MIN - RAMPA)) / float(RAMPA), 0.0, 1.0)
    alpha = np.where(fundo, 1.0 - suave, 1.0).astype(np.float32)

    # Desfaz a mistura com o fundo branco. Sem isto, todo pixel de borda fica
    # com um pouco de branco embutido e a fruta ganha uma franja luminosa
    # quando colocada sobre o marrom do site.
    # Formula padrao de un-matte:  cor_real = (observada - (1-a)*branco) / a
    a = np.clip(alpha, 0.0, 1.0)[..., None]
    observada = arr.astype(np.float32)
    segura = np.maximum(a, 0.25)
    limpa = (observada - (1.0 - a) * 255.0) / segura
    # So a faixa de meia-transparencia precisa de correcao: o miolo opaco fica
    # como esta, e o que ja e quase invisivel nao importa.
    franja = (a > 0.06) & (a < 0.98)
    arr = np.clip(np.where(franja, limpa, observada), 0, 255).astype(np.uint8)
    img = Image.fromarray(arr)

    # Encolhe a silhueta em ~1px: mata o que sobrou de meia-borda.
    canal_alpha = Image.fromarray((np.clip(alpha, 0, 1) * 255).astype(np.uint8))
    canal_alpha = canal_alpha.filter(ImageFilter.MinFilter(3))
    alpha = np.asarray(canal_alpha).astype(np.float32) / 255.0

    # As bolhas desfocadas do fundo (bokeh) viram manchas sem forma sobre o
    # marrom do site. Elas se distinguem por nao terem detalhe: o mapa de
    # nitidez local separa a fruta em foco (sementes, brilho) do borrao.
    print("Removendo o que esta fora de foco...")
    cinza = np.asarray(Image.fromarray(arr).convert("L"), dtype=np.float32)
    gy, gx = np.gradient(cinza)
    detalhe = Image.fromarray(
        np.clip(np.hypot(gx, gy) * 6.0, 0, 255).astype(np.uint8))
    # O desfoque espalha o detalhe das sementes por todo o corpo da fruta,
    # para que areas lisas de um morango nitido nao sejam confundidas com bokeh.
    detalhe = detalhe.filter(ImageFilter.GaussianBlur(22))
    mapa = np.asarray(detalhe).astype(np.float32)
    if mapa.max() > 0:
        mapa /= mapa.max()
    foco = np.clip((mapa - 0.10) / 0.10, 0.0, 1.0)
    alpha = (alpha * foco).astype(np.float32)

    print("Separando as frutas...")
    total = largura * altura
    _, achados = componentes(alpha > 0.5, int(total * AREA_MINIMA))
    print("  %d regioes relevantes" % len(achados))

    candidatos = []
    for c in achados:
        x0, y0, x1, y1 = c["caixa"]
        recorte = img.crop((x0, y0, x1, y1))
        c["nitidez"] = nitidez(recorte, alpha[y0:y1, x0:x1])
        c["recorte"] = recorte
        c["alpha"] = alpha[y0:y1, x0:x1]
        candidatos.append(c)

    candidatos.sort(key=lambda c: c["nitidez"], reverse=True)
    for c in candidatos:
        x0, y0, x1, y1 = c["caixa"]
        print("  regiao %5d  %4dx%-4d  area %7d  nitidez %8.1f"
              % (c["id"], x1 - x0, y1 - y0, c["pixels"], c["nitidez"]))

    escolhidos = candidatos[:2]          # os dois grupos em foco
    escolhidos.sort(key=lambda c: c["pixels"], reverse=True)

    print("\nGerando as camadas:")
    for i, c in enumerate(escolhidos, start=1):
        rgba = c["recorte"].convert("RGBA")
        canal = Image.fromarray((np.clip(c["alpha"], 0, 1) * 255).astype(np.uint8))
        # Um leve desfoque so no canal alpha tira o serrilhado da silhueta.
        canal = canal.filter(ImageFilter.GaussianBlur(0.6))
        rgba.putalpha(canal)

        caixa = rgba.getbbox()
        if caixa:
            rgba = rgba.crop(caixa)

        base = "morango-%d" % i
        for w in LARGURAS:
            if w > rgba.width:
                continue
            h = max(1, round(rgba.height * w / rgba.width))
            menor = rgba.resize((w, h), Image.LANCZOS)
            menor.save(os.path.join(SAIDA, "%s-%dw.webp" % (base, w)),
                       "WEBP", quality=88, method=6)
            menor.quantize(colors=224, method=Image.FASTOCTREE).save(
                os.path.join(SAIDA, "%s-%dw.png" % (base, w)), "PNG", optimize=True)
        print("  + %-12s %4dx%-4d" % (base, rgba.width, rgba.height))

    print("\nPronto. Arquivos em %s" % SAIDA)


if __name__ == "__main__":
    main()
