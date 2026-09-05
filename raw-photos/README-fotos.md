# 📸 Como trocar e adicionar fotos do site — passo a passo

Este é o único arquivo que você precisa ler para atualizar qualquer foto do
site. Não é preciso mexer em código.

---

## ⚡ Resposta rápida: "baixo tudo num zip e jogo no projeto?"

**Sim, é exatamente isso.** O fluxo é:

1. No Google Fotos, seleciona tudo → **Baixar** → vem um `.zip`.
2. Descompacta e joga **todos os arquivos** dentro de `raw-photos/galeria/`.
   Não precisa renomear, não precisa escolher, não precisa separar.
3. Roda dois comandos:

   ```bash
   python tools/processar-galeria.py
   python tools/gerar-galeria-html.py
   ```

4. Pronto. O site já está com as fotos novas.

O programa cuida sozinho de:

- **corrigir a rotação** (aquela foto que fica deitada);
- **descartar as tremidas** e desfocadas;
- **juntar as rajadas** — se você tirou 4 fotos seguidas do mesmo bolo, ele
  mantém só a mais nítida;
- **reduzir e comprimir** (uma foto de 4 MB do celular vira ~22 KB);
- **sortear 10** para a vitrine da página inicial;
- **montar a página** `galeria.html` com todas.

> Foi assim que as 282 fotos que você colocou viraram **194 fotos boas**,
> ocupando 23 MB em vez de 911 MB.

**Não commite a pasta `raw-photos`.** Ela está no `.gitignore` de propósito:
são centenas de MB que o site não usa. Guarde num HD externo ou no Drive — o
que vai para o repositório é só o resultado otimizado.

### Quero outro sorteio na página inicial

```bash
python tools/gerar-galeria-html.py --semente 42     # troca as 10 fotos
python tools/gerar-galeria-html.py --destaques 14   # mostra 14 em vez de 10
```

### Quero manter tudo, sem descarte automático

```bash
python tools/processar-galeria.py --sem-dedupe
```

---

## Fotos de produto do Menu (essas precisam de nome certo)

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
├── menu/       → fotos dos produtos dos cards do "Nosso Menu"
│                 (precisam do nome na convenção: menu-cafe-01.jpg)
├── galeria/    → fotos dos doces (pode jogar tudo aqui, sem renomear)
└── equipe/     → retratos da Sanderly / da família
```

> **A pasta `galeria/` é a exceção boa:** ali o nome do arquivo não importa.
> Pode despejar o zip inteiro do Google Fotos. Nas outras duas, siga a
> convenção do Passo 2, porque o site precisa saber qual foto é qual produto.

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

---

## Os dois programas, lado a lado

| Programa | Para que serve | Quando rodar |
| --- | --- | --- |
| `tools/processar-galeria.py` | Lê `raw-photos/galeria/`, limpa, comprime e escreve o `galeria.json` | Sempre que adicionar ou remover fotos da galeria |
| `tools/gerar-galeria-html.py` | Monta a vitrine da home e a página `galeria.html` a partir do `galeria.json` | Depois do de cima, ou sozinho para re-sortear as 10 da home |
| `tools/otimizar-fotos.py` | Fotos de produto do Menu, do herói e retratos (usa a convenção de nomes) | Ao trocar foto de produto |
| `tools/recortar-heroi.py` | Recorta o morango do fundo branco para a cena do herói | Só se trocar a imagem do herói |
