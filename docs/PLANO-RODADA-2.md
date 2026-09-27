# Plano — Rodada 2

**Projeto:** Dolce Vita Di Sandi  
**Escopo:** experiência de navegação, saneamento do cardápio, troca de marca/fotos, pendências de políticas e avaliação da futura jornada de pedido via WhatsApp.  
**Regra desta rodada:** este arquivo é planejamento. Nenhum código ou texto jurídico deve ser alterado automaticamente nesta entrega.

## 1. Leitura do estado atual

A implementação que deve orientar a próxima rodada está em `Client/Public/Src`. Há também uma versão paralela em `index/` e uma prévia em `preview-dolce/`; isso precisa ser resolvido antes do deploy para evitar corrigir uma camada e publicar outra.

Pontos encontrados:

- A home editorial já tem âncoras, header sticky, `scroll-padding-top` e `scroll-behavior: smooth` em `Client/Public/Src/Styles/editorial.css`, mas o header/logo e a rolagem devem ser validados em todos os breakpoints e com `prefers-reduced-motion`.
- A home usa “Bombom de morango” no hero e em conteúdo de ingredientes; o cardápio usa “Sonho”, “Sobremesa no pote”, “Bombom de morango”, cafeteria, bebidas geladas e “Chocolate & carinho”.
- O JavaScript mantém um catálogo próprio em `Client/Public/Src/Js/script.js`; o cardápio HTML e os metadados JSON-LD mantêm outro catálogo. A rodada deve alinhar todas as superfícies, não somente os títulos visíveis.
- Não existe arquivo identificado como logo/marca PNG no inventário do repositório. Os logos atuais são texto/HTML.
- Não há arquivo ou referência textual identificada para Camafeu de uva. A galeria possui muitas fotos sem nomes semânticos; a inclusão depende de validação visual do cliente.
- As políticas estão marcadas como rascunho para revisão e contêm dados concretos, mas ainda não estão confirmadas como dados jurídicos/operacionais definitivos.

## 2. Entregas da rodada

### 2.1 Navegação e rolagem

Implementar e validar:

1. Header/logo clicável levando a `#inicio` na home e à página inicial nas páginas internas.
2. Rolagem natural para âncoras, com compensação do header sticky para que o título da seção não fique encoberto.
3. Transição suave somente quando o usuário não tiver solicitado redução de movimento; com `prefers-reduced-motion`, manter salto/rolagem instantânea e sem animações supérfluas.
4. Estado de foco visível no logo e nos links; links internos devem continuar funcionando por teclado, toque e mouse.
5. Verificação específica no mobile: header em duas linhas, navegação horizontal sem cortar o CTA e sem bloquear a rolagem vertical.
6. Se o logo PNG for aprovado, usar o arquivo como marca visual no header/footer sem remover texto alternativo acessível; preservar o nome da marca em texto acessível.

### 2.2 Nomenclatura e catálogo

| Nome final | Substitui | Imagem/decisão inicial |
|---|---|---|
| Coxinha recheada | Sonho | Confirmar foto fornecida; não reaproveitar a foto `produto-sonho-*` sem aprovação visual. |
| Bolo no pote | Doce no pote / Sobremesa no pote | A foto existente `produto-pote-*` pode ser candidata, mas precisa ser confirmada como bolo no pote. |
| Cookies recheados | Cookies | Usar `produto-cookies-*` ou nova foto fornecida, conforme o produto real. |
| Camafeu de morango | Bombom de morango | A foto `produto-bombom-morango-*` só deve ser mantida se representar o camafeu; atualizar alt text, hero, OG e textos relacionados. |
| Camafeu de uva | Novo item condicional | Adicionar somente se o cliente identificar uma foto/asset correspondente e confirmar disponibilidade do item. |

Aplicar o alinhamento em: cards da home, modal de seleção, link/CTA do WhatsApp, cardápio HTML, JSON-LD do cardápio, meta description/OG, alt texts, filtros/categorias, textos da galeria e qualquer teste automatizado que selecione os nomes antigos.

“Coxinha recheada” deve substituir “Sonho” como produto, não apenas trocar o rótulo: a descrição, categoria, alt text, slug/ID interno se houver e imagem precisam descrever a coxinha. O mesmo vale para cada substituição.

### 2.3 Remoções obrigatórias

Remover da experiência publicada e dos metadados de produto:

- seção **Cafeteria**;
- seção **Bebidas geladas**;
- item **Soda italiana**;
- seção **Chocolate & carinho**;
- item **Sonho** do cardápio interno.

Também remover referências derivadas: descrições SEO, JSON-LD, filtros, cards, fotos de faixa, links, dados de seleção, alt texts e qualquer chamada que sugira café/bebida como produto vendável. A palavra “café” pode continuar em contexto editorial somente se o cliente confirmar que não é oferta do cardápio; não deve parecer item encomendada.

### 2.4 Logo PNG e novas fotos

O cliente deve fornecer/confirmar:

- logo PNG final, preferencialmente com fundo transparente;
- versão clara/escura, se houver necessidade para header chocolate e fundos claros;
- largura/altura original e área de respiro desejada;
- autorização de uso das novas fotos;
- associação de cada foto a um produto e indicação da foto principal;
- indicação de cortes permitidos (quadrado para cards, vertical/hero e faixa da galeria).

Fluxo de assets:

1. Receber o logo e as fotos sem sobrescrever os arquivos atuais.
2. Criar nomes estáveis e sem acentos, por exemplo `logo-dolce-vita-di-sandi.png` e `produto-camafeu-uva-01.jpg`.
3. Gerar derivados responsivos em WebP/PNG/JPEG conforme o uso, preservando o original em uma pasta de origem.
4. Atualizar o manifesto de assets e os caminhos usados no HTML/JS.
5. Conferir dimensões, foco do corte, peso, alt text e ausência de imagem quebrada.

## 3. Mapeamento de assets

| Uso | Asset atual/candidato | Ação da rodada | Dependência |
|---|---|---|---|
| Favicon/header atual | `Client/Public/Src/Assets/otimizadas/menu/menu-torta-01-480w.png` | Substituir pelo favicon/logo aprovado, se adequado | Logo PNG e preferência de favicon |
| Torta Holandesa | `menu/produto-torta-holandesa-400w/800w.(webp|jpg)` | Manter se continuar no catálogo | Confirmação normal |
| Sonho → Coxinha recheada | `menu/produto-sonho-400w/800w.(webp|jpg)` | Não reutilizar automaticamente; arquivar como legado até o cliente mapear nova foto | Foto correta da coxinha |
| Doce/Sobremesa no pote → Bolo no pote | `menu/produto-pote-400w/800w.(webp|jpg)` | Candidato a renome lógico; validar conteúdo da foto | Confirmação do cliente |
| Cookies → Cookies recheados | `menu/produto-cookies-400w/800w.(webp|jpg)` | Usar apenas se a foto mostrar cookies recheados; caso contrário trocar | Foto/descrição correta |
| Bombom de morango → Camafeu de morango | `menu/produto-bombom-morango-400w/800w.(webp|jpg)` | Validar antes de manter; atualizar todos os textos | Confirmação visual |
| Camafeu de uva | Nenhum asset semântico encontrado | Não publicar placeholder; escolher entre fotos de `raw-photos/` somente após identificação | Foto e confirmação de disponibilidade |
| Café/soda | `menu/menu-cafe-01-*`, `menu/menu-soda-01-*` | Retirar do conjunto publicado do cardápio; não apagar o original nesta rodada | Confirmação de que não haverá oferta |
| Galeria | `Client/Public/Src/Assets/otimizadas/galeria/` e `raw-photos/` | Manter galeria geral, mas etiquetar/marcar novas fotos por produto antes de promovê-las a card | Mapeamento foto → produto |
| Logo | Nenhum arquivo logo encontrado no repositório | Aguardar entrega do cliente | PNG final |

O arquivo `Client/Public/Src/Assets/otimizadas/manifesto.json` deve ser a fonte de rastreabilidade dos derivados. Os arquivos originais de `raw-photos/` não devem ser apagados durante a limpeza.

## 4. Políticas: dados que o cliente ainda precisa preencher/confirmar

Não alterar o texto jurídico automaticamente. Entregar ao cliente a lista abaixo para resposta e, depois, encaminhar as respostas para revisão jurídica antes de publicar.

### Política de privacidade

Confirmar por escrito:

1. Nome empresarial/razão social ou confirmação de que o responsável será publicado somente como pessoa física.
2. CPF/CNPJ, se será exibido na política e qual endereço oficial de contato/sede deve constar.
3. Nome e contato do responsável pelo tratamento/encarregado (DPO), ou confirmação de que o e-mail e WhatsApp atuais cumprem esse papel.
4. E-mail, telefone e WhatsApp oficiais; confirmar se o número `15 99129-1842` continua correto.
5. Quais dados realmente chegam pelo site, WhatsApp, e-mail, hospedagem, formulários, analytics, pixels, fontes externas e logs do servidor.
6. Se existe formulário, armazenamento local, banco, CRM, planilha, backup ou histórico de pedidos fora do WhatsApp; por quanto tempo cada um é retido e como é eliminado.
7. Se o histórico de encomendas de fato é mantido e quem tem acesso a ele.
8. Quais serviços/provedores estão ativos (Hostinger, Google/Gmail, Meta/WhatsApp e outros) e em que região os dados podem ser tratados.
9. Se haverá marketing/promocional, por qual canal, com qual base legal e como o opt-out será registrado.
10. Se o site usa apenas fontes externas ou se haverá analytics/pixel/cookies; confirmar antes de manter a afirmação atual de que não há rastreamento.
11. Prazo operacional real para responder solicitações de titulares; o texto atual menciona até 15 dias.
12. Data de vigência/última atualização que deve ser publicada e quem aprova futuras alterações.

### Política de reembolso e cancelamento

Confirmar com a operação e com revisão jurídica:

1. Se o pedido somente é confirmado após item, quantidade, valor, data e forma de entrega serem respondidos no WhatsApp.
2. Prazos e percentuais de cancelamento: mais de 48h, 24–48h e menos de 24h.
3. Quando a produção é considerada iniciada e como isso é comunicado ao cliente.
4. Se remarcação é possível, em quais condições e quantas vezes.
5. Prazo e método real de devolução (Pix, dinheiro ou outro), inclusive dados necessários para devolver.
6. Tratamento de taxas de entrega, retirada, pagamento e eventuais tarifas de terceiros.
7. Procedimento para atraso, ausência do cliente, endereço incorreto e falha de entrega.
8. Prazo de 24h para reclamação, necessidade de foto e conservação do produto; confirmar se esses requisitos são praticáveis e juridicamente adequados.
9. Lista real de alergênicos/traços e se há procedimentos separados para produção; não publicar garantia sem validação da cozinha.
10. Horário de atendimento informado como “todos os dias, das 9h às 20h”.
11. Disponibilidade real de troca, crédito, refação e reembolso em caso de problema.
12. Quem aprova a versão final e data de vigência.

Até essas respostas chegarem, manter as políticas claramente identificadas como rascunho interno e não prometer que o texto atual é definitivo.

## 5. Arquitetura futura: pedido que cai no WhatsApp

### Recomendação para a próxima etapa

Manter, por enquanto, uma arquitetura client-side simples: o visitante monta uma seleção e o navegador abre um link `wa.me` com uma mensagem estruturada. Não coletar pedido em servidor nesta rodada e não tratar a abertura do WhatsApp como confirmação do pedido.

Mensagem futura sugerida, montada a partir de dados estruturados:

```text
Olá! Vi o site da Dolce Vita Di Sandi e gostaria de fazer um pedido.
Itens: [produto x quantidade]
Data desejada: [data]
Entrega ou retirada: [opção]
Observações/alergias: [texto]
Nome: [nome]
```

O fluxo deve distinguir:

1. seleção/preenchimento no site;
2. mensagem aberta no WhatsApp;
3. mensagem efetivamente enviada pelo cliente;
4. confirmação manual da Dolce Vita com item, quantidade, preço, data e logística;
5. pagamento e produção somente após confirmação.

Antes de automatizar mais, definir: tabela de preços, quantidades mínimas, disponibilidade por data, sabores/variações, entrega ou retirada, taxa/área de entrega, formas de pagamento, conservação, contato de atendimento e rotina de registro do pedido. Sem esses dados, o site deve continuar orientando para conversa, não simulando checkout.

### Evolução quando houver volume

Se o volume justificar, avaliar WhatsApp Business com catálogo e respostas rápidas; depois, uma camada de backend/CRM apenas se houver necessidade de status, estoque, histórico, pagamento ou múltiplos atendentes. A privacidade deve ser revisada antes de criar armazenamento próprio.

### Spell.sh — consideração limitada ao produto

O Spell.sh consultado é o Spell UI, um registry de componentes e demos interativas via MCP, útil como referência de cards, estados, feedback e microinterações. Ele não deve ser adotado como sistema de pedidos, catálogo operacional, banco de dados, checkout ou integração WhatsApp. Se usado, a decisão fica restrita a padrões visuais/motion, com acessibilidade, performance e `prefers-reduced-motion` como requisitos. Fonte: [documentação MCP do Spell UI](https://spell.sh/docs/mcp).

## 6. Critérios de aceite

### Navegação

- [ ] Clique no logo retorna ao início sem recarregar a home.
- [ ] Cada âncora posiciona o título abaixo do header, sem sobreposição, em desktop e mobile.
- [ ] A rolagem é suave para usuários que aceitam movimento e reduzida/desligada para quem optou por redução.
- [ ] Header, logo, links e CTA têm foco visível e não impedem a rolagem no mobile.

### Catálogo

- [ ] Não há “Sonho”, “Doce no pote”, “Sobremesa no pote”, “Bombom de morango”, “Cafeteria”, “Bebidas geladas”, “Soda italiana” ou “Chocolate & carinho” nas superfícies publicadas onde foram removidos/substituídos.
- [ ] Os nomes finais aparecem de forma consistente na home, cardápio, seleção, modal, SEO, JSON-LD e alt texts.
- [ ] “Camafeu de uva” só aparece com foto aprovada e confirmação de disponibilidade.
- [ ] Nenhum produto tem imagem que represente outro produto.
- [ ] Não há imagem quebrada, asset legado apontado por HTML/JS ou filtro sem resultado.

### Marca e fotos

- [ ] Logo PNG aprovado aparece nos usos definidos, com contraste, proporção e texto alternativo corretos.
- [ ] Cada nova foto tem origem, licença/autorização, produto associado e derivados responsivos registrados.
- [ ] Favicon, Open Graph, hero, cards e galeria usam caminhos válidos.

### Políticas e pedido

- [ ] Nenhum texto jurídico foi reescrito sem aprovação explícita e revisão jurídica.
- [ ] Todas as pendências da seção 4 têm resposta do cliente ou permanecem marcadas como pendentes.
- [ ] O CTA de WhatsApp pré-preenche uma mensagem legível, mas não comunica confirmação automática de pedido.
- [ ] O fluxo deixa claro que a confirmação ocorre manualmente no WhatsApp.

## 7. Ordem recomendada de execução

1. Cliente aprova a fonte de publicação (`Client/Public/Src`) e envia logo/fotos com mapeamento.
2. Cliente confirma nomes, disponibilidade e produto Camafeu de uva.
3. Implementar saneamento do catálogo e remoções, incluindo SEO/JSON-LD/JS.
4. Integrar assets aprovados e revisar alt texts/cortes.
5. Ajustar e testar header, logo, âncoras e rolagem.
6. Validar a jornada de seleção → WhatsApp em desktop, Android e iOS.
7. Preencher pendências das políticas e encaminhar para revisão jurídica; só então publicar a versão final.

