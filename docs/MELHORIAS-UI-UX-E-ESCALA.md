# Dolce Vita Di Sandi — melhorias, operação e escala

Este documento registra o que foi melhorado no redesign e o caminho recomendado para transformar o site em um canal de pedidos sem perder o caráter artesanal da marca.

## Entregue nesta rodada

- Navegação por âncoras com rolagem suave e offset para o header fixo.
- Header, logo e chamadas principais apontando para seções reais da home.
- Cardápio simplificado somente com produtos da doceria; cafeteria e bebidas foram removidas.
- Nomes corrigidos: coxinha recheada, bolo no pote, cookies recheados, camafeu de morango e camafeu de uva quando houver foto confirmada.
- Fotos editoriais aplicadas à capa, torta holandesa e camafeu de nozes.
- Logo oficial usada em pontos de reconhecimento da marca.
- Estados de foco visíveis, layout responsivo, modal de produto e seleção persistente no navegador.
- CTA de pedido preparado para montar uma mensagem organizada para o WhatsApp.

## Componentes e UI/UX

### Navegação

Manter um único header fixo, com marca clicável para o início e links para `Doces`, `Ingredientes`, `Galeria`, `Nossa história` e `Contato`. O menu móvel deve continuar acessível por teclado, fechar após a escolha e não esconder o destino atrás do header.

### Catálogo

Cada produto deve ter nome, categoria, descrição curta, foto, disponibilidade e um CTA claro. Os dados devem ficar em uma estrutura única, separada do HTML, para que uma futura tela administrativa ou CMS não exija reescrever componentes.

O filtro deve ser complementar, nunca a única forma de encontrar um produto. O estado vazio precisa explicar que não houve resultado e oferecer limpar filtros.

### Pedido

O fluxo atual deve ser curto: escolher produto, informar quantidade, data desejada e observação opcional, revisar e abrir o WhatsApp. O botão precisa indicar que o usuário ainda revisará e enviará a mensagem no próprio WhatsApp.

Não coletar cartão, senha, CPF ou dados desnecessários. Para alimentos personalizados, mostrar antecedência mínima e avisos de alergênicos antes da confirmação.

### Acessibilidade

- Contraste suficiente entre texto e fundos.
- `alt` descritivo para fotos e logo.
- Foco visível em links, filtros, botões e campos.
- Modal fechável por Escape e com foco controlado.
- Respeito a `prefers-reduced-motion`.
- Não usar animação como única forma de comunicar estado.

### Imagens e desempenho

Manter fotos originais arquivadas fora do fluxo crítico e servir versões otimizadas para a web. Usar `width`, `height`, `loading="lazy"` nas imagens abaixo da dobra e `fetchpriority="high"` somente na imagem principal. Evitar repetir a mesma composição em vários cards.

## O que confirmar antes de publicar as políticas

Os textos de privacidade e reembolso ainda devem ser tratados como rascunho até a Sanderly confirmar os dados e, idealmente, um advogado revisar o conteúdo. Preencher ou confirmar cuidadosamente:

1. Nome completo da responsável e, se existir, razão social, nome fantasia, CPF/CNPJ e endereço oficial.
2. E-mail, WhatsApp, horário de atendimento e cidade/área real de retirada e entrega.
3. Se existe taxa de entrega, como ela é calculada e quem pode receber o pedido.
4. Formas de pagamento aceitas, momento do pagamento e procedimento para sinal ou pagamento antecipado.
5. Prazo mínimo real para cada tipo de encomenda e o que acontece em urgências.
6. Regras reais para cancelamento em mais de 48 horas, entre 24 e 48 horas e em menos de 24 horas. Os percentuais sugeridos não devem ser publicados sem aprovação.
7. Se remarcação, crédito e reembolso por Pix realmente podem ser oferecidos, incluindo prazo operacional.
8. Canal e prazo para reclamações de produto, entrega danificada, item incorreto e conservação inadequada.
9. Ingredientes e alergênicos efetivamente usados na cozinha, inclusive risco de traços e possibilidade de adaptações.
10. Quais dados são anotados, onde ficam guardados, quem acessa e por quanto tempo. Remover a promessa de histórico se isso não acontecer na prática.
11. Serviços terceirizados realmente utilizados. A política cita WhatsApp, Gmail e Hostinger; confirmar se todos continuam verdadeiros.
12. Atualização da data. Não publicar “setembro de 2026” como última atualização até revisar e aprovar o texto.

Também conferir se os nomes das fontes citados na política correspondem às fontes efetivamente carregadas no site. A política deve refletir a implementação real, não um texto genérico.

## Escala do pedido via WhatsApp

### Fase 1 — site estático, baixo volume

O catálogo fica em dados estruturados no JavaScript ou em JSON local. O navegador monta uma mensagem usando `encodeURIComponent`, abre o WhatsApp e o cliente revisa antes de enviar. O site não precisa de banco nem servidor para começar.

Mensagem sugerida:

```text
Olá! Quero fazer um pedido na Dolce Vita Di Sandi.

Produto: {produto}
Quantidade: {quantidade}
Data desejada: {data}
Observações: {observações}

Nome: {nome}
```

### Fase 2 — organização interna

Adicionar um identificador local do pedido, status visual e campos de disponibilidade. A mensagem pode incluir um código curto para a família localizar rapidamente a conversa. O catálogo deve prever preço, unidade, antecedência, sabores, alergênicos e datas bloqueadas.

### Fase 3 — volume maior

Quando o atendimento manual começar a gerar perda de mensagens, migrar para uma camada de servidor: formulário HTTPS, validação, banco de pedidos, painel de status e integração oficial com WhatsApp Business Platform. O navegador não deve carregar tokens secretos nem depender de links longos para transportar dados sensíveis.

Fluxo futuro:

```text
Site → API segura → pedido registrado → aviso no WhatsApp Business → confirmação da família → status atualizado
```

Guardar somente o necessário, aplicar controle de acesso, registrar consentimento para novidades e definir rotina de exclusão. A integração oficial e os limites de envio devem ser avaliados quando essa fase for necessária.

## Spell.sh: o que vale aproveitar

O Spell se apresenta como uma coleção de componentes React de alta qualidade para copiar e adaptar. Para este projeto vanilla, não vale adicionar React ou uma dependência de build somente por causa da biblioteca. Vale aproveitar como referência visual pontual:

- microinterações de botão, desde que não prejudiquem leitura ou acessibilidade;
- gradientes suaves e estados de foco em ações principais;
- transições de galeria e modal com movimento reduzido quando o usuário preferir;
- composição editorial de cards e destaques.

Evitar efeitos pesados, raios de luz, animações contínuas e dependências externas que aumentem o peso da home ou disputem atenção com as fotos dos doces. Referência consultada: [Spell UI](https://spell.sh/).

## Critérios de aceite contínuos

- Nenhum produto removido reaparece no cardápio ou nos dados estruturados.
- Todos os links de navegação chegam a um ID existente.
- Não há overflow horizontal em 320, 390, 768 e 1440 px.
- O pedido abre o WhatsApp com texto legível e sem perder caracteres especiais.
- O site funciona sem JavaScript para leitura básica das políticas.
- Fotos e logo têm `alt`, caminhos válidos e versões adequadas para produção.
- A política só é marcada como oficial depois das confirmações da família e revisão jurídica.

## Benchmark e novas seções recomendadas

O benchmark foi feito em sites oficiais de marcas reconhecidas, observando padrões de experiência e não copiando identidade visual.

- A [Ladurée](https://laduree.com/en-ww) combina história de marca, endereços, entrega, embalagem e coleções sazonais. Para a Dolce Vita, isso sugere uma seção **Encomendas especiais** com ocasiões, tamanhos, antecedência e embalagem para presente.
- A [Pierre Hermé](https://pierreherme.com/en/our-shops) organiza criações, lojas, cafés, serviços e coleções. Para a Dolce Vita, isso sugere **Coleção da temporada**, **Como funciona a encomenda** e um mini guia de retirada/entrega.
- A [Magnolia Bakery](https://www.magnoliabakery.com/pages/about-us) transforma origem e comunidade em parte da marca. Para a Dolce Vita, isso sugere **A cozinha da Sanderly**, depoimentos reais e uma seção de clientes/ocasiões, sem inventar avaliações.
- O [Dominique Ansel](https://www.dominiqueansel.com/) integra chef, lojas, compras, histórias e conteúdo de preparo. Para a Dolce Vita, isso sugere **Vídeos da cozinha**, receitas de bastidores e uma página de conteúdo conectada ao canal do YouTube.

### Prioridade de implementação

1. **Vídeos da cozinha** — entrar quando a URL oficial do canal e uma miniatura real forem confirmadas. Usar vídeos incorporados somente quando fizer sentido; manter uma imagem leve e link externo como fallback.
2. **Encomendas para ocasiões** — aniversário, presente, café da tarde e festa. Cada card pode pré-preencher uma mensagem diferente no WhatsApp.
3. **Coleção da temporada** — destaque editorial com validade e disponibilidade, sem deixar item esgotado parecendo disponível.
4. **Como pedir** — três passos: escolher, conversar e combinar entrega/retirada.
5. **Depoimentos e clientes** — publicar somente avaliações autorizadas, com nome ou identificação aprovada.
6. **FAQ de conservação e alergênicos** — reduzir dúvidas repetidas e deixar o atendimento mais seguro.

O canal confirmado no projeto é [@DolceVitaDiSandi](https://www.youtube.com/@DolceVitaDiSandi/videos). A home já ganhou um acesso direto no bloco de contato; a próxima evolução pode trazer uma seção editorial com uma miniatura real do vídeo mais recente.
