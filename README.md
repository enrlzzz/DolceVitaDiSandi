# 🍰 Dolce Vita Di Sandi

🔗 **Site:** <https://dolcevitadisandi.com.br/>

Site da **Dolce Vita Di Sandi**, doceria artesanal de Sorocaba/SP fundada em
2015 pela Sanderly. Feito pelo filho dela, o Enrico.

---

## 🛠️ Stack

HTML5, CSS3 e JavaScript puro. **Sem build, sem framework, sem dependência de
runtime** — os arquivos são servidos como estão.

Zero JavaScript de terceiros. As únicas requisições externas são as fontes
Poppins e Miniver do Google Fonts.

---

## 📁 Estrutura

```
.
├── .htaccess                  # rotas, HTTPS, cabeçalhos de segurança, cache
├── robots.txt  sitemap.xml    # SEO
├── Client/Public/Src/
│   ├── Pages/
│   │   ├── index.html                      # página principal
│   │   ├── cardapio.html                   # cardápio em página web
│   │   ├── politica-de-privacidade.html
│   │   └── politica-de-reembolso.html
│   ├── Styles/styles.css
│   ├── Js/script.js
│   └── Assets/
│       ├── otimizadas/        # gerado pelo script — WebP + fallback, 4 tamanhos
│       └── *.png *.jpg        # originais
├── raw-photos/                # fotos novas entram aqui (veja README-fotos.md)
├── tools/otimizar-fotos.py    # otimizador de imagens
└── docs/
    ├── DEPLOY-HOSTINGER.md    # deploy automático GitHub → Hostinger
    └── RELATORIO-ELEVACAO.md  # o que foi feito, medições e backlog
```

---

## 🚀 Rodar localmente

```bash
python -m http.server 8000
```

Depois abra <http://localhost:8000/Client/Public/Src/Pages/index.html>.

> Use um servidor, não abra o `index.html` direto pelo navegador: os caminhos
> dos arquivos são absolutos (`/Client/...`) e não funcionam via `file://`.

---

## 📸 Trocar as fotos

Sem mexer em código. O passo a passo completo está em
[`raw-photos/README-fotos.md`](raw-photos/README-fotos.md).

```bash
pip install Pillow                  # só na primeira vez
python tools/otimizar-fotos.py      # processa o que estiver em /raw-photos
```

---

## 🌐 Publicar

Deploy automático a cada `git push` na `main`, via o recurso **GIT** do hPanel
da Hostinger. Guia completo: [`docs/DEPLOY-HOSTINGER.md`](docs/DEPLOY-HOSTINGER.md).

---

## ✅ O que o site entrega

- Mobile-first, testado em viewport de 390px
- Acessibilidade WCAG 2.1 AA: contraste validado, navegação por teclado, foco
  visível, `alt` em todas as imagens, landmarks e ARIA
- `prefers-reduced-motion` respeitado e detecção de aparelho fraco
- SEO: Open Graph, Twitter Card, schema.org `Bakery` e `Menu`, sitemap
- Carga inicial de ~44 KB no celular (com gzip)
