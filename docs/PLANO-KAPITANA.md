# Plano de redesign — Dolce Vita Di Sandi

## Direção

Traduzir a linguagem editorial de `KAPITANA_VEG(3).html` para a Dolce Vita Di Sandi: experiência de confeitaria autoral, com ritmo de revista, blocos amplos, fotos em destaque e chamadas curtas. Preservar a paleta atual de `Client/Public/Src/Styles/styles.css`; a referência funciona como estrutura e comportamento, não como cópia de identidade.

## Layout proposto

1. **Header fixo/compacto** — logo Dolce Vita, links `Início`, `Catálogo`, `Galeria`, `Ingredientes`, `História`, `Contato` e CTA `Encomendar`. Fundo chocolate escuro, borda sutil e navegação horizontal; menu recolhido no mobile.
2. **Hero escuro grande** — grid 50/50, altura mínima de uma viewport. À esquerda: eyebrow, headline bold em caixa alta, frase de apoio e dois CTAs. À direita: foto vertical de doce/mesa, crop controlado e legenda sobreposta. Faixa inferior com 2–3 provas rápidas (feito à mão, ingredientes, encomendas).
3. **Catálogo** — fundo creme, título editorial e filtros por categoria. Cards em grade de 3 colunas desktop / 2 tablet / 1–2 mobile, com imagem, nome, descrição curta e ação. Valores sob consulta, pois não há preços confirmados para publicação. Usar cartões limpos, sem excesso de molduras.
4. **Galeria** — mosaico assimétrico de fotos reais, com uma imagem dominante e duas/ três menores. Legendas discretas; preservar proporções com `object-fit: cover`. No mobile, virar carrossel ou coluna única.
5. **Ingredientes** — seção de contraste em chocolate escuro. Layout texto + foto/diagrama do produto; abas ou chips para destacar ingredientes e benefícios. Rosa apenas como estado ativo/destaque.
6. **História** — bloco narrativo em duas colunas: foto tipo editorial à esquerda e capítulos/linha do tempo à direita. Cada capítulo deve ter título forte, texto curto e indicador de progresso; no mobile, empilhar foto antes da narrativa.
7. **Contato / encomenda** — fundo creme ou rosa suave derivado do token rosa, com headline de fechamento, canais de contato, horário/local e formulário curto. CTA primário `Fazer encomenda`; incluir WhatsApp/Instagram como links secundários.
8. **Footer** — assinatura grande da marca, links essenciais, redes e aviso legal. Repetir a linguagem de rodapé amplo da referência sem competir com o CTA.

## Tokens de design

```css
:root {
  --chocolate: #4E342E;       /* superfícies, header, botões */
  --chocolate-escuro: #2C1810;/* hero, ingredientes, texto forte */
  --creme: #F5EEE9;           /* fundo principal */
  --rosa: #E06CFD;            /* ação, seleção, pequenos acentos */
  --rosa-suave: #F2B3FF;      /* apoio em fundos claros */
  --texto: #2C1810;
  --texto-inverso: #F5EEE9;
  --borda: rgba(78, 52, 46, .14);
  --raio: 18px;
  --raio-grande: 28px;
  --largura-max: 1240px;
  --espaco-secao: clamp(64px, 9vw, 120px);
}
```

### Tipografia e uso

- **Display:** sans bold/condensada em caixa alta para o hero e títulos principais, seguindo o impacto do `welcome h1` da referência.
- **Corpo:** Poppins já presente no projeto; pesos 400/500/600/700.
- **Acento:** fonte script atual somente em microdetalhes/assinaturas, nunca em texto essencial.
- Contraste: texto claro somente sobre `--chocolate-escuro`; texto escuro sobre `--creme` ou rosa. Manter foco visível e alvos de toque confortáveis.

## Regras visuais e responsivas

- Container máximo de 1240px, gutters de 20–48px; seções com bastante respiro vertical.
- Fotos sempre com `width/height` ou `aspect-ratio`, `object-fit: cover` e posição definida para evitar distorção/CLS.
- Desktop usa grids de duas colunas; abaixo de 800px empilhar conteúdo e manter CTA visível após o hero.
- Animações devem ser discretas (entrada por opacidade/translate) e desligadas em `prefers-reduced-motion`.
- Rosa é cor de ação: reservar para CTA, foco, seleção e detalhes; não usar como fundo dominante do site.

## Critério de fidelidade à referência

Manter: header sticky, hero split texto/foto, eyebrow numerado, títulos com quebra editorial, alternância de fundos, galeria assimétrica, narrativa por capítulos e fechamento com CTA. Adaptar: nomes, conteúdo, fotos e linguagem para Dolce Vita Di Sandi e substituir a paleta verde/oliva original pela paleta chocolate/creme/rosa acima.

## Escopo desta etapa

Este documento é somente planejamento. Nenhum HTML, CSS ou JavaScript foi alterado nesta etapa.
