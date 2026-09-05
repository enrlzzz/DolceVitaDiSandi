# Dolce Vita Di Sandi — Relatório de elevação de patamar

Setembro de 2026 · Site: <https://dolcevitadisandi.com.br>

---

## 1. Auditoria da stack (o que realmente existe)

| Item | Situação encontrada |
| --- | --- |
| Framework | Nenhum. HTML5 + CSS3 + JavaScript puro |
| Build / bundler | Não existe. Os arquivos são servidos como estão |
| Gerenciador de pacotes | Nenhum `package.json` no repositório |
| CMS | Nenhum. Conteúdo escrito direto no HTML |
| Hospedagem | Hostinger, servindo arquivos estáticos |
| Testes | Nenhum |
| CI/CD | Nenhum (deploy manual) |
| Analytics | Nenhum |
| Backend do formulário | **Não existe.** O `<form>` tinha `action="#"` — a mensagem não ia para lugar nenhum |
| Tokens de cor | Já existiam em `:root`, mas o restante do CSS misturava variáveis e valores fixos |
| `.gallery-image` / `.menu-image` | `Client/Public/Src/Styles/styles.css` |

### Dois bugs críticos que a auditeria de produção não podia enxergar

**a) A media query nunca fechava.** No `styles.css` da árvore de trabalho, o
bloco `@media (max-width: 900px)` aberto na linha 285 nunca era fechado. O
resultado: **todo o CSS das linhas 525 a 695** — seção Sobre, galeria, contato e
rodapé — só era aplicado em telas de até 900px. No desktop, essas seções ficavam
sem estilo. O arquivo também tinha ~200 linhas duplicadas literalmente.

**b) O `<form>` não enviava nada.** Sem `action`, sem backend, sem validação e
sem proteção anti-spam. Qualquer pessoa que preenchesse achando que estava
mandando mensagem simplesmente não era atendida.

---

## 2. O que foi executado, por prioridade

### P0 — Correções críticas

- **Galeria sem distorção.** Substituído `object-fit: fill` por `cover`, com
  grid bento (cards de tamanhos diferentes), `grid-auto-flow: dense`,
  `loading="lazy"` e lightbox acessível (teclado, setas ← →, ESC, foco devolvido
  ao elemento de origem, rolagem da página restaurada ao fechar).
- **Media query fechada** e CSS reescrito do zero, sem duplicação.
- **Políticas reais publicadas** — `politica-de-privacidade.html` (LGPD:
  quais dados, para quê, por quanto tempo, direitos do titular, responsável) e
  `politica-de-reembolso.html` (prazos de cancelamento, o que fazer se o doce
  vier com problema, o que não é reembolsável por ser perecível/personalizado,
  aviso de alergênicos). Ambas com **aviso destacado de rascunho para revisão**
  e linkadas corretamente no rodapé de todas as páginas.

### P1 — Credibilidade e conteúdo

- **"Membros" virou "Nossa História"** — linha do tempo 2015 → hoje (o começo,
  o boca a boca, a pausa, a volta), retrato da Sanderly com selo "Desde 2015",
  três números de credibilidade e três espaços de depoimento marcados como
  "Em breve", com convite para o cliente mandar o dele pelo WhatsApp.
  O Enrico saiu do card de equipe e virou uma linha discreta no rodapé:
  *"Site feito com carinho pelo filho da Sanderly, Enrico."*
- **Pipeline de fotos** — `tools/otimizar-fotos.py` (só precisa de Pillow):
  corrige rotação de EXIF, recorta na proporção da seção **sem esticar**, gera
  480/800/1200/1600px em WebP + fallback, escreve `manifesto.json` e imprime o
  bloco `<picture>` pronto. Passo a passo completo em
  `raw-photos/README-fotos.md`, incluindo como exportar do Google Fotos.

### P2 — UI/UX e herói 3D

- **Auditoria de contraste (WCAG 2.1 AA).** O CTA "Compre Agora" usava texto
  **branco sobre rosa #E06CFD = 2,72:1 — reprovado** (o mínimo é 4,5:1).
  Trocado para tinta escura `#2C1810` sobre o mesmo rosa: **6,21:1 — aprovado**,
  sem mexer na cor de marca. Todos os botões ganharam estados
  `hover` / `focus-visible` / `active` distintos, alvo de toque de 48px e anel
  de foco visível em duas camadas (funciona sobre fundo claro e escuro).
- **Herói 3D.** Cena com profundidade real em CSS `preserve-3d`: halo de luz,
  plano de sombra, cinco partículas de ingrediente orbitando em `translateZ`
  diferentes, morango flutuando, inclinação suave seguindo o mouse e transição
  de saída no scroll que entrega a cena para a seção "Sobre".
  Respeita `prefers-reduced-motion` e detecta aparelho fraco
  (`saveData`, `effectiveType 2g`, `deviceMemory ≤ 2`, `hardwareConcurrency ≤ 2`)
  → nesses casos a cena vira imagem estática, sem animação.

> **Decisão técnica que diverge do briefing, e o porquê.** O pedido sugeria
> `<model-viewer>`, Three.js ou R3F. Não usei nenhum dos três, por dois motivos
> concretos: (1) exigiriam um modelo glTF de morango que **não existe** no
> projeto — e os modelos do CGTrader citados como referência são licenciados,
> não podem ser baixados nem redistribuídos; (2) `<model-viewer>` sozinho pesa
> ~250 KB de JS, mais o modelo — num site cujo público abre pelo celular, muitas
> vezes em rede móvel, isso é mais caro do que todo o resto da página somada.
> A cena em CSS 3D entrega profundidade, paralaxe e movimento com **0 KB de
> biblioteca**. Se no futuro houver orçamento para um modelo 3D licenciado ou
> feito sob medida, a estrutura já está pronta para receber: basta trocar o
> `<picture>` dentro de `.hero-image-wrapper`.

### P3 — Estrutura, SEO e segurança

- Meta tags completas + **Open Graph e Twitter Card** (essencial: o link é
  compartilhado no WhatsApp o tempo todo).
- **Schema.org `Bakery`** com NAP consistente, ano de fundação, fundadora,
  redes sociais e `OrderAction` apontando para o WhatsApp. Página de cardápio
  com schema `Menu`.
- `robots.txt` e `sitemap.xml`.
- **Formulário que funciona:** validação no cliente com mensagens em português,
  `aria-invalid` + `aria-live` para leitor de tela, **honeypot anti-spam** e
  montagem de uma mensagem pronta no WhatsApp. Nenhum dado trafega para
  servidor de terceiros.
- **`.htaccess`** com HTTPS forçado, cabeçalhos de segurança (CSP,
  X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy),
  compressão, cache longo para imagens e URLs limpas.
- **Deploy automático GitHub → Hostinger** documentado em
  `docs/DEPLOY-HOSTINGER.md`.

---

## 3. Arquivos criados e alterados

### Criados

| Arquivo | O que é |
| --- | --- |
| `Client/Public/Src/Pages/politica-de-privacidade.html` | Política de privacidade (LGPD) — rascunho para revisão |
| `Client/Public/Src/Pages/politica-de-reembolso.html` | Política de reembolso e cancelamento — rascunho para revisão |
| `Client/Public/Src/Pages/cardapio.html` | Cardápio em página web (o PDF continua disponível) |
| `Client/Public/Src/Assets/otimizadas/**` | 16 fotos em 4 tamanhos, WebP + fallback |
| `tools/otimizar-fotos.py` | Otimizador de fotos |
| `raw-photos/README-fotos.md` | Passo a passo para trocar fotos sem mexer em código |
| `.htaccess` | Rotas, segurança, cache, compressão |
| `robots.txt`, `sitemap.xml` | SEO |
| `docs/DEPLOY-HOSTINGER.md` | Guia de deploy automático |
| `docs/RELATORIO-ELEVACAO.md` | Este documento |

### Alterados

| Arquivo | Mudança |
| --- | --- |
| `Client/Public/Src/Pages/index.html` | Reescrito: nova estrutura, SEO, acessibilidade, herói 3D, história, galeria bento, formulário funcional |
| `Client/Public/Src/Styles/styles.css` | Reescrito: tokens, media query corrigida, sem duplicação, mobile-first |
| `Client/Public/Src/Js/script.js` | Reescrito: sem GSAP/Swiper, IntersectionObserver, lightbox, validação |

---

## 4. Antes e depois

### O bug da galeria

**Antes:** `.gallery-image { object-fit: fill }` forçava todas as fotos para
385×691px. As fotos reais são 1080×648, 1600×1200, 901×1600, 1200×1600,
1600×939 e 1080×648 — ou seja, fotos deitadas eram **espremidas dentro de um
frame em pé**. Um bolo redondo virava um oval.

**Depois:** grid bento com `object-fit: cover`. Medido no navegador, cada foto
agora é exibida na proporção correta, apenas recortada nas bordas. Nenhuma
imagem distorcida em nenhum dos dois layouts (mobile 2 colunas, desktop 4).

### Outros defeitos encontrados e corrigidos durante os testes no navegador

1. O `<dialog>` do lightbox aparecia por cima da página inteira desde o
   carregamento (`display: grid` anulava o `display: none` nativo).
2. Os atributos `height` do HTML venciam o `aspect-ratio` do CSS e esticavam o
   retrato da Sanderly para 1070px de altura.
3. O `<picture>` não herdava altura, então o `object-fit: cover` não tinha caixa
   para preencher e os cards do bento ficavam com buracos.
4. O evento `close` do `<dialog>` não dispara de forma confiável — a página
   ficava **sem rolagem** depois de fechar uma foto. Agora a restauração é
   explícita em todos os caminhos de saída.
5. O `backdrop-filter` do header fazia dele o bloco de contenção do menu mobile
   `position: fixed` — o painel abria com 60px de altura em vez da tela cheia.
6. `<img src="">` no lightbox gerava uma requisição fantasma da própria página.

### Performance

Medido no navegador, mesma máquina, carga a frio.

| Métrica | Antes (produção) | Depois | Variação |
| --- | ---: | ---: | ---: |
| Requisições | 34 | 16 | **−53%** |
| Peso total da página | 4.613 KB | 1.347 KB | **−71%** |
| **Carga inicial (o que o visitante espera para ver)** | **~4.613 KB** | **152 KB** (desktop) · **~44 KB** (mobile, com gzip) | **−97%** |
| JS de terceiros | 152 KB (GSAP + ScrollTrigger + Swiper) | 0 KB | **−100%** |
| CSS de terceiros | 108 KB (Font Awesome) | 0 KB (só Google Fonts) | **−100%** |
| Hosts de terceiros | 3 | 1 | −67% |
| `domInteractive` | 284 ms | 46 ms | **−84%** |
| Imagens com lazy loading | 0 de 16 | 14 de 15 | — |
| Maior imagem (morango) | 957 KB | 22 KB (mobile) / 39 KB (desktop) | **−96%** |

Ganhos estruturais que a tabela não mostra: `width`/`height` em todas as
imagens e altura reservada no palco do herói (**CLS próximo de zero**);
`preload` com `fetchpriority="high"` na imagem do herói, que é o LCP.

> **Sobre o Lighthouse:** não foi possível rodá-lo — o Lighthouse não está
> instalado nesta máquina e o site novo ainda não está publicado, então não
> existe URL pública para medir. Os números acima foram medidos de verdade via
> `PerformanceResourceTiming` no Chrome, servindo as duas versões lado a lado
> em `localhost`. **Assim que o deploy for feito**, rode
> <https://pagespeed.web.dev/> na URL de produção para ter as quatro notas
> oficiais — a expectativa, pelos números acima, é Performance e Best Practices
> altos; Acessibilidade e SEO devem ficar próximos de 100, já que contraste,
> foco, alt text, landmarks, meta tags e schema foram tratados.

---

## 5. Recomendação: sistema de agendamento (P4 — não implementado, aguardando decisão)

**Recomendação: comece pelo que já está no ar agora — formulário estruturado com
confirmação manual pelo WhatsApp. Não construa sistema de agendamento ainda.**

Por quê, em três pontos:

1. **O gargalo hoje não é organização, é volume.** A Sanderly está retomando com
   pouco pedido. Um Calendly ou WhatsApp Business API resolve um problema de
   agenda cheia — problema que ainda não existe. Construir agora é otimizar o
   que não é o gargalo.
2. **Atrito mata conversão em doceria de bairro.** Cada campo a mais e cada
   redirecionamento derruba pedido. O caminho "clico → WhatsApp abre com a
   mensagem pronta → aperto enviar" tem o menor atrito possível e mantém a
   conversa pessoal, que é justamente o diferencial da marca.
3. **A confirmação manual é uma vantagem, não uma limitação.** Falar com a
   Sanderly *é* parte do produto. Automatizar cedo demais tiraria o que faz o
   cliente voltar.

**O que já está funcionando** (implementado nesta rodada): o formulário monta
uma mensagem estruturada — nome, item, data, detalhes — e abre a conversa. A
Sanderly recebe tudo organizado e só confirma.

**Fase 2 — critério objetivo para migrar:**

| Gatilho | O que fazer |
| --- | --- |
| **Mais de 10 pedidos/semana** por 3 semanas seguidas | Planilha compartilhada de encomendas (Google Sheets) para não depender do caderninho |
| **Mais de 20 pedidos/semana** ou começar a perder data por esquecimento | WhatsApp Business (catálogo, respostas rápidas, etiquetas de pedido) — gratuito |
| **Mais de 40 pedidos/semana** ou 2+ pessoas atendendo | Aí sim: agendamento com bloqueio de agenda e/ou WhatsApp Business API |
| Começar a pedir sinal antecipado | Link de pagamento (Mercado Pago/PagSeguro) no fluxo de confirmação |

**Pergunto explicitamente:** você quer que eu implemente algo além disso agora,
ou seguimos com o WhatsApp e revisitamos quando bater o gatilho de 10
pedidos/semana? Minha recomendação é a segunda opção.

---

## 6. Backlog de Inovação — 10 sugestões

**1. SEO local em Sorocaba**
*Problema:* quem busca "doceria em Sorocaba" ou "torta holandesa Sorocaba" não
encontra a marca; o site não aparece no mapa e não tem avaliações.
*Solução:* criar o Perfil da Empresa no Google (grátis) com o mesmo NAP do site,
categoria "Doceria", fotos reais e área de entrega; enviar o `sitemap.xml` ao
Search Console; criar uma página por produto-chave ("Torta Holandesa em
Sorocaba", "Beliscão de goiabada"), já que o schema `Bakery` está no ar.
*Esforço:* **médio** (perfil em 1 dia; páginas por produto ~1 dia cada).

**2. Prova social que existe de verdade**
*Problema:* a seção de depoimentos está vazia. Sem prova social, quem não conhece
a marca hesita em pagar por comida feita em casa.
*Solução:* pedir depoimento aos 15 clientes mais antigos por WhatsApp (mensagem
pronta), com print da conversa autorizado. Meta: 6 depoimentos com nome e bairro.
Os espaços "Em breve" já estão prontos para receber.
*Esforço:* **baixo** (a estrutura já existe; falta o conteúdo).

**3. Fidelidade em papel, não em app**
*Problema:* não há motivo estruturado para o cliente voltar; a recompra depende
de lembrança.
*Solução:* cartão físico "a cada 10 doces, 1 grátis", carimbado na entrega —
custo quase zero, funciona com o público certo e vira contato salvo no celular.
Versão digital só quando passar de 100 clientes recorrentes.
*Esforço:* **baixo**.

**4. Instagram como vitrine viva, site como fechamento**
*Problema:* o Instagram tem as fotos boas e o site tem as fracas; os dois não
conversam.
*Solução:* link do site na bio apontando para `#Menu`; a cada post de produto,
story com link direto para o WhatsApp com mensagem pronta (os links já existem
no site, é só reaproveitar); publicar 2× por semana no mesmo horário.
*Esforço:* **baixo**, contínuo.

**5. Cardápio sazonal com data de encerramento**
*Problema:* cardápio fixo não cria urgência nem motivo para voltar ao site.
*Solução:* um item rotativo por temporada (paçoca em junho, panetone trufado em
dezembro, morango na primavera) com "só até [data]" em destaque no herói. Escassez
real, sem invenção — e resolve o excesso de ingrediente sazonal.
*Esforço:* **médio** (1 seção nova + disciplina de calendário).

**6. Resposta automática só no primeiro contato**
*Problema:* mensagem que chega às 23h fica sem resposta até de manhã, e o cliente
some.
*Solução:* mensagem de ausência do WhatsApp Business + 5 respostas rápidas
(cardápio, prazo, entrega, formas de pagamento, encomenda de festa). Automatiza
o primeiro toque sem robotizar a conversa.
*Esforço:* **baixo**.

**7. Campanha de volta para os clientes antigos**
*Problema:* existe uma base de clientes de 2015–2023 que não sabe que a doceria
voltou. É o público mais barato de reativar que existe.
*Solução:* varrer a agenda do WhatsApp, separar quem já comprou e mandar mensagem
individual (nunca lista de transmissão genérica): "Oi [nome], a Dolce Vita voltou
— lembra da torta que você pediu no aniversário do seu filho?". Meta: 50 contatos
na primeira semana.
*Esforço:* **baixo**, retorno alto.

**8. Fotografia de produto de verdade**
*Problema:* as fotos do menu hoje parecem banco de imagens genérico e não mostram
o que a Sanderly realmente faz. Em comida, a foto **é** o produto.
*Solução:* uma sessão de 2h com luz natural, fundo neutro, foto do doce inteiro
e um close do recheio, todas na mesma proporção. O pipeline
(`tools/otimizar-fotos.py`) já processa tudo automaticamente.
*Esforço:* **médio** — e é a mudança de maior impacto visual de toda a lista.

**9. Página por produto para busca e compartilhamento**
*Problema:* o site é uma página só; quem quer mandar "olha a torta" manda o site
inteiro, e o Google tem uma URL só para indexar.
*Solução:* uma página por produto principal (torta, beliscão, cookies) com foto
grande, história do doce, prazo, alergênicos e botão de pedido. Melhora SEO e
compartilhamento no WhatsApp.
*Esforço:* **médio**.

**10. Medir o que acontece**
*Problema:* hoje não há como saber quantas pessoas visitam, de onde vêm, nem
quantas clicam no WhatsApp. Toda decisão é no escuro.
*Solução:* uma ferramenta leve e sem cookies (Plausible ou Umami, ~1 KB), com
evento no clique do WhatsApp. Assim dá para responder "o Instagram traz pedido?"
com número, não com achismo. **Atenção:** se for instalado, a Política de
Privacidade precisa ser atualizada — está sinalizado no texto dela.
*Esforço:* **baixo**.

**Se fosse para fazer só três, nesta ordem:** 8 (fotos), 7 (clientes antigos), 1
(Google Maps). São os três que mexem em faturamento na semana seguinte.

---

## 7. Pendências que dependem do Enrico

### Bloqueiam o deploy

1. **Salvar o PDF do cardápio antes de esvaziar o `public_html`.** O arquivo
   `Cardápio Oficial DolceVitaDiSandi.pdf` existe só no servidor e **não está no
   repositório** — com o deploy via Git ele some. Baixe, coloque na raiz do
   projeto e versione. Passo a passo em `docs/DEPLOY-HOSTINGER.md`.
2. **Backup completo do `public_html`** antes de qualquer limpeza.

### Precisam da sua decisão ou da sua revisão

3. **Revisar as duas políticas.** Eu redigi rascunhos de boa qualidade, mas não
   sou advogado. Confirme com a Sanderly principalmente os prazos da política de
   reembolso (48h/24h) e o horário de atendimento (coloquei 9h–20h, todos os
   dias — se estiver errado, corrija: aparece em 3 lugares).
4. **Sistema de agendamento:** confirme se seguimos com a recomendação da
   seção 5 (WhatsApp por enquanto) ou se você quer algo mais robusto agora.
5. **Fotos de produto.** As imagens do menu hoje parecem banco de imagens. Suba
   as fotos boas do Google Fotos seguindo `raw-photos/README-fotos.md`.
6. **A foto da seção "Sobre"** (`about-image.jpg`) é um casal genérico tomando
   café — não tem nada a ver com a marca. Vale trocar por uma foto real da
   cozinha, da mesa de doces ou da Sanderly trabalhando.
7. **Prazo de encomenda.** Escrevi "48h de antecedência para torta". Confirme.
8. **Depoimentos:** 3 espaços prontos esperando conteúdo real (sugestão 2 do
   backlog).
9. **Perfil da Empresa no Google** — só você pode criar e validar.

### Verificar depois que estiver no ar

10. Rodar o PageSpeed Insights na URL de produção e guardar as notas oficiais.
11. Testar o compartilhamento do link no WhatsApp para conferir se a imagem do
    Open Graph aparece.
12. Depois de uma semana de HTTPS estável, descomentar o HSTS no `.htaccess`.
