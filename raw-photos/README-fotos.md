# 📸 Como trocar as fotos do site — passo a passo

Este é o único arquivo que você precisa ler para atualizar qualquer foto do
site. Não é preciso mexer em código.

---

## Resumo em 4 passos

1. Exporte as fotos do Google Fotos (instruções abaixo).
2. Renomeie seguindo a convenção de nomes.
3. Jogue os arquivos dentro da pasta certa em `/raw-photos`.
4. Rode um comando. Pronto — o site já usa as fotos novas.

---

## Passo 1 — Exportar do Google Fotos

**Pelo computador (recomendado, mantém a qualidade máxima):**

1. Abra <https://photos.google.com> no navegador.
2. Selecione as fotos que você quer (clique na bolinha do canto de cada uma).
3. Clique nos três pontinhos `⋮` no canto superior direito → **Baixar**.
4. O Google gera um arquivo `.zip`. Baixe e descompacte na sua área de trabalho.

**Pelo celular:** abra a foto → `⋮` → **Baixar**. Depois passe para o
computador (cabo, Google Drive ou WhatsApp Web — evite mandar por WhatsApp
comum, ele reduz muito a qualidade).

> ⚠️ Não use print de tela nem foto baixada do Instagram. A qualidade cai muito
> e o site fica com cara de amador. Use sempre o arquivo original.

**Dica de fotografia (vale mais que qualquer código):** luz natural perto da
janela, fundo limpo (uma toalha branca ou uma tábua de madeira já resolve),
foto do doce inteiro e uma bem de perto mostrando o recheio.

---

## Passo 2 — Renomear os arquivos

A regra é sempre a mesma:

```
<seção>-<produto>-<número>.jpg
```

| Parte      | O que colocar                                            |
| ---------- | -------------------------------------------------------- |
| `seção`    | `menu`, `galeria`, `equipe` ou `hero`                     |
| `produto`  | nome curto, tudo minúsculo, sem acento, com `-` no lugar do espaço |
| `número`   | `01`, `02`, `03`... (dois dígitos)                        |

**Exemplos corretos:**

```
menu-cafe-01.jpg
menu-torta-holandesa-01.jpg
menu-cookies-02.jpg
galeria-torta-holandesa-02.jpg
galeria-beliscao-01.jpg
equipe-sanderly-01.jpg
hero-morango-01.png
```

**Exemplos errados:**

```
IMG_20250612.jpg          ← não diz o que é
Torta Holandesa.jpg       ← tem espaço e letra maiúscula
café-01.jpg               ← tem acento
menu-cafe-1.jpg           ← número precisa de dois dígitos: 01
```

---

## Passo 3 — Colocar na pasta certa

```
raw-photos/
├── menu/       → fotos dos produtos que aparecem nos cards do "Nosso Menu"
├── galeria/    → fotos bonitas para a seção "Galeria"
└── equipe/     → retratos da Sanderly / da família
```

Se você colocar a foto dentro da pasta certa, pode até esquecer o prefixo da
seção no nome — o programa completa sozinho. Mas com o prefixo fica mais
organizado.

---

## Passo 4 — Rodar o otimizador

Abra o terminal na pasta do projeto e rode:

```bash
python tools/otimizar-fotos.py
```

Na primeira vez, se der erro dizendo que o Pillow não foi encontrado:

```bash
pip install Pillow
```

O programa vai:

- corrigir a rotação (aquela foto do celular que fica deitada);
- recortar no formato certo da seção **sem esticar nada**;
- gerar versões de 480, 800, 1200 e 1600 pixels de largura;
- criar `.webp` (formato moderno, bem mais leve) com `.jpg`/`.png` de reserva;
- salvar tudo em `Client/Public/Src/Assets/otimizadas/`;
- atualizar o `manifesto.json` com os caminhos.

No final ele imprime na tela um bloco de código `<picture>` pronto. Se a foto é
substituição de uma que já existe (mesmo nome), **não precisa fazer mais nada** —
o site já aponta para ela. Se é uma foto nova, copie o bloco impresso e cole no
`index.html` no lugar indicado.

### Ganho real dessa etapa

A foto `morango.png` original tinha **957 KB**. Depois do otimizador, a versão
que o celular baixa tem **22 KB** — 43× mais leve, sem diferença visível.

---

## Perguntas rápidas

**Posso apagar as fotos de `/raw-photos` depois?**
Pode, mas é melhor guardar. Elas são o original em alta; a pasta `otimizadas`
tem só as versões reduzidas.

**Rodei o comando e a foto não mudou no site.**
Aperte `Ctrl + Shift + R` no navegador para forçar o recarregamento — o
navegador guarda as imagens antigas em cache.

**Como sei que deu certo?**
O terminal mostra uma linha `+ nome-da-foto 1200x1600 -> 3 tamanhos` para cada
foto processada. Se aparecer `! ignorado`, o nome do arquivo está fora da
convenção do Passo 2.

**Quero reotimizar tudo que já está no site.**

```bash
python tools/otimizar-fotos.py --incluir-atuais
```
