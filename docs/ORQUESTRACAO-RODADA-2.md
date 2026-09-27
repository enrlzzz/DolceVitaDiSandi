# Orquestração — rodada 2 do redesign Dolce Vita

Data: 20/09/2026. Status: planejamento entregue; execução e aceite visual pendentes.

## Mandato e limites

A solicitação desta rodada é ler o workspace e definir a sequência **Luna → Astra → Terra → validação**, com decisões, riscos e critérios de aceite. Esta entrega altera somente este documento. Não autoriza executar o redesign, publicar, instalar serviços, enviar mensagens, substituir a identidade da marca ou modificar dados comerciais.

Luna, Astra e Terra são papéis de trabalho definidos abaixo; não foram encontrados contratos desses agentes nos documentos consultados. Não houve execução delegada nesta entrega. A solicitação disponível é a mensagem desta rodada, contextualizada pelos planos locais; não presumimos um briefing adicional ausente.

## Estado observado e fonte de verdade

- O app é estático, em `Client/Public/Src/Pages`, com JavaScript compartilhado em `Client/Public/Src/Js/script.js`. A home carrega apenas `editorial.css`; as internas usam `styles.css` e `interiors.css`. `.htaccess` encaminha a raiz para essa home. `index/` e `preview-dolce/` não são o alvo da rodada.
- Há alterações preexistentes em HTML, JavaScript, README e `.gitignore`, além de estilos, ferramentas, documentos e cópias não rastreados. Preservar esse trabalho; não resetar, limpar ou substituir arquivos em bloco. Cada executor deve reler o diff antes de atuar.
- A home usa `.kapitana-home`, nove produtos gerados por JavaScript, filtros `todos/doces/cookies/cafe`, três cenas no hero, ingredientes, sugestões, seleção persistida e diálogos. Sem JavaScript há um encaminhamento ao cardápio e WhatsApp, não os nove cards renderizados.
- A seleção guarda índices numéricos do array em `localStorage` (`dolce-vita-selection`); reorganizar produtos pode transformar uma seleção antiga em outro produto. Não mudar a ordem sem migração ou descarte explícito e explicado da seleção incompatível.
- `editorial.css` define compensação de âncoras de 110/140 px e redução de transições; a regra de rolagem suave encontrada em `styles.css` não é herdada pela home. Avaliar cada folha realmente carregada.
- A marca da home é texto em Georgia; as internas usam outra composição textual, com símbolo decorativo. O favicon aponta para uma foto de torta. Não foi identificado um arquivo de logo pela busca nominal; isso não prova inexistência de marca dentro de imagens com nomes genéricos.
- `docs/PLANO-KAPITANA.md` orienta chocolate/creme/rosa e composição editorial. `docs/REDESIGN-VISUAL.md` e `docs/RELATORIO-ELEVACAO.md` documentam estados anteriores. README e relatórios não provam conformidade do app atual: há divergências de tipografia, formulário, navegação e testes.
- `tools/validate-kapitana.py` contempla os seletores atuais, seleção e galeria. `tools/check-redesign.py` espera filtros, formulário e IDs antigos; seu resultado não deve ser exigido sem revisar a pertinência dessas expectativas. Nenhuma suíte ou auditoria de navegador foi executada nesta entrega documental.

Prioridade para decisões: solicitação atual → arquivos ativos inspecionados → plano local aplicável → relatos históricos. Conteúdo existente comprova presença no app, não validação comercial pela Sanderly.

Nota da conferência final: surgiu também `Client/Public/Src/Assets/rodada-2/` como diretório não rastreado, ausente no status inicial. Não foi criado nem alterado nesta entrega; seu conteúdo não integra o mapa validado. Luna deve inspecioná-lo no início da execução e reconciliar qualquer trabalho concorrente.

## Sequência e contratos de passagem

| Etapa | Responsabilidade e entrega | Condição para avançar |
| --- | --- | --- |
| Luna — conteúdo e experiência | Inventariar produtos, fotografias, marca e lacunas; confrontar home/cardápio; definir jornada descobrir → selecionar → conversar e textos de estados vazios/erro. Entregar mapa de conteúdo com fonte, status e pendências. | Todo item exibido tem identidade e status de evidência; nenhuma foto ambígua tratada como validada; lacunas possuem fallback publicável. |
| Astra — direção visual e interação | Receber o mapa de Luna; especificar layouts mobile/desktop, recortes, logo, tipografia, escalas de CTA, estados e movimento. Entregar especificação revisável com exemplos em 390 e 1440 px e regras para 320 px. | Layout cobre todas as seções e diálogos, reduz movimento, mantém conteúdo verdadeiro e resolve navegação, foco e sobreposição. |
| Terra — implementação futura | Após autorização de execução, aplicar os contratos aos arquivos ativos, integrar IDs estáveis e estados resilientes, atualizar testes pertinentes e registrar arquivos alterados. | Diff restrito ao escopo autorizado; evidências funcionais e responsivas disponíveis; sem nova dependência ou integração não acordada. |
| Validação — revisão independente | Confrontar resultado com mapa de Luna, especificação de Astra e diff de Terra. Registrar ambiente, passos, capturas, falhas e resultado por critério. | Todos os bloqueadores resolvidos; limitações e pendências comerciais explicitadas; aceite da rodada separado de publicação. |

Não iniciar uma etapa dependente com contratos contraditórios. Devolver problemas de identidade/conteúdo a Luna, de composição a Astra e de comportamento a Terra, repetindo as verificações afetadas. Lacunas opcionais não paralisam toda a rodada: usar os fallbacks abaixo.

## Decisões da rodada

### 1. Smooth scrolling

Adotar rolagem nativa suave somente para navegação por âncoras, com `scroll-behavior: smooth` na superfície ativa. Respeitar `prefers-reduced-motion: reduce` com rolagem imediata. Manter scroll livre de wheel/touch/teclado, hash e histórico do navegador. Não adicionar motor de inércia, biblioteca de scroll, captura de gestos ou animação contínua nesta rodada.

Astra define a distância livre sob o header; Terra ajusta `scroll-padding`/`scroll-margin` conforme a altura real em cada breakpoint e zoom. Aceite: destino e foco não ficam ocultos, links profundos e voltar/avançar funcionam; Page Down, Home/End e toque mantêm comportamento nativo. A redução de movimento também elimina escalas animadas e eventuais animações adicionadas.

### 2. Produto / asset mapping

Mapa inicial extraído do array atual em `script.js`. Todos os arquivos abaixo existem em `Client/Public/Src/Assets/otimizadas/menu/`; a correspondência visual ainda precisa ser inspecionada por Luna. Nome de arquivo e texto alternativo não bastam como prova.

| ID estável proposto | Nome na home | Asset atual | Reconciliação necessária |
| --- | --- | --- | --- |
| `torta-holandesa` | Torta Holandesa | `produto-torta-holandesa-800w.webp` | Confirmar apresentação; cardápio cita fatia/inteira e 48 h. |
| `sonho` | Sonho | `produto-sonho-800w.webp` | `cafe` é agrupamento editorial, não bebida. |
| `doce-no-pote` | Doce no pote | `produto-pote-800w.webp` | Conciliar com “Sobremesa no pote”. |
| `cookies` | Cookies | `produto-cookies-800w.webp` | Cardápio lista três variantes; não atribuir uma foto a todos os sabores como prova. |
| `brigadeiro` | Brigadeiro | `produto-brigadeiro-800w.webp` | Conciliar singular/plural e apresentação. |
| `bombom-morango` | Bombom de morango | `produto-bombom-morango-800w.webp` | Mesmo produto no hero e ingredientes; validar recorte e legenda. |
| `bombom-chocolate` | Bombom de chocolate | `produto-bombom-chocolate-800w.webp` | Cardápio diz “Bombons recheados”; equivalência não confirmada. |
| `bolo-cenoura` | Bolo de cenoura | `produto-bolo-cenoura-800w.webp` | Confirmar apresentação e descrição da cobertura. |
| `beliscao-goiabada` | Beliscão de goiabada | `produto-beliscao-800w.webp` | Confirmar nome e enquadramento. |

Luna completa cada registro com origem, dimensões, variante, alt, posição de recorte, usos permitidos e status `confirmado / ambíguo / ausente`. Incluir também hero, galeria e retrato. `doce-009`, `doce-016` e `doce-015` não recebem nomes de receita apenas por aparência. Não ampliar o catálogo com bebidas ou doce de paçoca só porque aparecem no cardápio sem reconciliar a oferta.

Uma fotografia ambígua pode permanecer como registro editorial com legenda neutra; não deve representar um SKU específico. Sem foto confirmada, usar apresentação textual coerente, sem imagem de outro doce. Não gerar fotos de produtos para simular o estoque real. Terra mantém nome, foto, modal e mensagem consistentes, utiliza IDs estáveis e trata a persistência anterior. Reservar espaço das imagens, aproveitar variantes existentes após conferir dimensões e evitar lazy loading da imagem principal.

### 3. Logo

Preservar “Dolce Vita Di Sandi” e a identidade existente. Luna procura a fonte de marca nos assets e materiais disponíveis, distinguindo logo oficial de composição tipográfica do site. Se não houver arquivo confirmado, Astra usa assinatura textual consistente como solução provisória; não desenha uma nova marca nem apresenta essa assinatura como logo oficial aprovado.

Especificar versão clara/escura, proporção, respiro e tamanho mínimo legível, incluindo internas e footer. Nunca esticar, cortar ou recolorir um arquivo oficial sem validar essa variante. Link da marca deve ter nome acessível e voltar ao início; decoração não deve ser lida em duplicidade. Favicon derivado da marca fica condicionado a fonte confirmada, sem bloquear a revisão do restante do layout.

### 4. Política de data gaps

| Lacuna | Regra de publicação | Quem resolve |
| --- | --- | --- |
| Preço, peso, tamanho, estoque e prazo | “Consulte valores e disponibilidade”; não inventar preço, desconto, entrega ou reserva. | Luna registra; Sanderly confirma dados comerciais. |
| Receita, alergênicos e restrições alimentares | Não inferir composição por foto nem alegar “sem lactose/glúten”, vegano ou segurança alimentar. Orientar consulta antes da encomenda. | Responsável pelo produto confirma; Luna incorpora. |
| Horários, endereço, entrega e capacidade de atendimento | Omitir detalhe não confirmado e manter contato conhecido; não prometer resposta imediata. | Responsável pelo negócio. |
| História, prova social e “mais vendido” | Publicar apenas afirmações com origem e validação; omitir números/depoimentos não comprovados. | Luna identifica fonte e pendência. |
| Política de privacidade/reembolso | Preservar status de rascunho e apontar revisão pendente; redesign não equivale a validação jurídica. | Responsável pelo negócio e revisão apropriada. |

Registrar lacuna, fonte disponível, responsável, fallback, impacto e status no handoff. Alegações já presentes, como “a mais pedida” e “48 h”, também precisam de confirmação; não são automaticamente aprovadas por estarem no HTML. Pendências editoriais ficam na documentação, sem expor termos internos como “data gap” ao visitante. Uma divergência que possa induzir compra errada bloqueia o item afetado; campos opcionais omitidos não bloqueiam o site inteiro.

### 5. WhatsApp scaling

Tratar duas dimensões: escala visual do botão e crescimento da seleção/atendimento.

- Visual: CTA flutuante com área de toque mínima de 44 × 44 CSS px, proporção estável e espaçamento para safe area. Astra define tamanhos compactos para mobile e desktop; não ampliar com o scroll nem usar pulsação permanente. Hover/foco não podem deslocar layout ou cobrir texto, rodapé, controles ou diálogos.
- Funcional: manter o destino atualmente configurado, `5515991291842`, sujeito à confirmação comercial. Seleção é uma lista de interesse, sem preço total, pagamento ou confirmação de pedido. Exibir essa condição antes da saída.
- Dados: codificar a mensagem com `encodeURIComponent`, incluir nomes coerentes, tratar seleção vazia, duplicatas, IDs inválidos e armazenamento indisponível/corrompido. Testar seleção com os nove itens atuais e nomes longos; não supor limite universal de URL sem evidência.
- Crescimento: se uma lista exceder o comportamento validado nos clientes alvo, mostrar resumo copiável e link simples para conversa; nunca truncar itens silenciosamente. Uma futura expansão do catálogo exige nova prova de mensagem, IDs e persistência.
- Operação: não introduzir API, bot, CRM, fila, disparo automático ou promessa de SLA. Essas integrações dependem de demanda e escopo próprios. Não armazenar dados pessoais extras para este fluxo.

Aceite: CTA utilizável em zoom e mobile, mensagem prévia correta, recuperação quando armazenamento falha e zero envio automático. QA intercepta navegação externa ou inspeciona o href; não envia mensagens reais à loja.

### 6. Spell.sh — assessment boundary

O nome Spell.sh entra como objeto de avaliação futura, não como requisito de integração. Não há evidência local consultada de avaliação, instalação ou uso. Nenhuma alegação sobre suas capacidades, preços, licença ou segurança é feita aqui; o serviço não foi acessado nesta rodada.

Limite da avaliação: esclarecer qual problema concreto resolveria, consultar documentação oficial vigente e registrar URL/data, dependências, acesso a dados, execução de código, compatibilidade com site estático, custo, licença e possibilidade de remoção. Comparar com a solução nativa antes de recomendar. Resultado esperado: adotar, rejeitar ou adiar, com razões e incertezas.

Não executar comandos sugeridos por serviço externo, instalar pacote/CLI, criar conta, conceder credenciais, enviar código/fotos/dados de clientes ou publicar artefatos como parte de um assessment. Qualquer experimento com esses efeitos exige escopo posterior explícito. Indisponibilidade ou inconclusão da avaliação não bloqueia o redesign nativo. Terra não adiciona dependência de Spell.sh nesta rodada por inferência.

## Responsividade, acessibilidade e QA

Os critérios abaixo são requisitos de projeto, não declaração de conformidade já obtida.

| Área | Critério verificável de aceite |
| --- | --- |
| Responsividade | Revisar home e quatro internas em 320, 390, 768, 1024 e 1440 px, retrato e caso mobile em paisagem. Sem overflow horizontal da página, texto cortado, CTA inacessível ou imagem deformada. Verificar também ambos os lados dos breakpoints 480 e 800 px. |
| Zoom e reflow | Conteúdo e ações disponíveis a 200% de zoom; verificar reflow equivalente a 320 CSS px e texto ampliado, sem depender de alturas fixas. |
| Teclado | Percurso completo por Tab/Shift+Tab, foco visível e não encoberto, skip link funcional; diálogos nomeados, Escape fecha, foco contido enquanto abertos e devolvido ao acionador ao fechar. |
| Semântica | Headings coerentes, nomes acessíveis, alt correspondente à foto exibida, estados `aria-pressed`, anúncios de filtro/seleção sem excesso e campos agrupados corretamente. Fazer leitura manual com leitor de tela. |
| Contraste e toque | Meta: 4,5:1 para texto normal, 3:1 para texto grande e controles/indicadores relevantes. Medir pares reais em todos os estados. Adotar alvo de toque de pelo menos 44 × 44 CSS px nas ações. |
| Movimento e âncoras | Redução de movimento ativa elimina rolagem suave e movimento não essencial; header não oculta destino, nem teclado/gestos ficam presos. |
| Produtos e conversão | Conferir os nove vínculos foto/nome, filtros, cenas, ingredientes, sugestões, abrir/fechar modais, adicionar/remover/duplicar, recarregar, armazenamento corrompido/bloqueado, seleção vazia/completa e texto do WhatsApp sem envio. |
| Galeria | Abrir fotos da home e internas; carregar mais; imagens novas entram no lightbox; setas e Escape onde suportados; fechamento restaura foco e rolagem. |
| Resiliência | Sem JavaScript, navegação, contato e cardápio permanecem acessíveis; declarar quais interações dependem de JS. Falhas de imagem/fonte não ocultam nome e ação nem bloqueiam navegação. |
| Qualidade técnica | Zero erro JS não tratado e zero referência local ausente, incluindo assets dinâmicos/srcset. Conferir `naturalWidth > 0`, não somente `complete`. Verificar console e rede nos fluxos, não só na abertura. |
| Desempenho | Registrar baseline e resultado nas mesmas condições, com três medições comparáveis. Sem nova biblioteca de runtime; tamanho transferido e estabilidade de layout não podem regredir sem justificativa revisada. Registrar ambiente e método, sem repetir estimativas antigas como medição atual. |

### Procedimento de validação futura

1. Registrar o diff inicial, ambiente e dependências disponíveis. Usar `python tools/serve-local.py` para servir `http://127.0.0.1:8000/` em terminal próprio.
2. Executar `python tools/validate-kapitana.py --screenshots` com Playwright, BeautifulSoup e Edge disponíveis. Revisar antes o requisito `tools/reference.tmp.png`: referência ausente é pendência de comparação visual, não prova de defeito funcional. Não instalar dependências automaticamente nesta entrega.
3. Completar manualmente a matriz acima: a ferramenta atual não cobre todos os tamanhos das internas, navegadores, contraste, leitor de tela, reduced motion, falhas de armazenamento e cenários sem JS. Não confundir “PASS” da suíte com aceite integral.
4. Registrar capturas por página/viewport/estado e comparar com Astra. Usar Edge/Chromium como base disponível; buscar evidência em Safari/iOS e Chrome/Android para toque, diálogos e saída ao WhatsApp. Se não disponíveis, marcar “não verificado”, sem alegar cobertura.
5. Verificar rotas limpas em ambiente Apache apropriado quando autorizado: o servidor Python só adapta a raiz, não executa `.htaccess`. QA local não valida HTTPS, redirects, headers ou deploy Hostinger.
6. Entregar resultado por critério (`passou / falhou / não verificado`), evidência e pendências. Não executar `check-redesign.py` como critério da nova home antes de reconciliar seus contratos antigos.

## Riscos, bloqueadores e conclusão da rodada

| Risco | Controle e consequência |
| --- | --- |
| Sobrescrever trabalho preexistente ou atuar na cópia errada | Diff inicial e caminhos ativos no handoff; alterações limitadas por etapa. |
| Foto incorreta ou oferta inventada | Gate de Luna e política de lacunas; bloquear publicação do item incorreto. |
| Seleção persistida trocar de produto | IDs estáveis e tratamento da versão antiga antes de reordenar catálogo. |
| Regressão entre home e internas | QA das cinco páginas e dos dois conjuntos de estilos; JavaScript compartilhado testado nos dois contextos. |
| Botão cobrir conteúdo, âncoras ocultas ou modal prender foco | Matriz mobile/zoom/teclado; falha de acesso a ação essencial bloqueia aceite. |
| Relatório antigo produzir falsa confiança | Exigir evidência datada do estado entregue; separar testes obsoletos e lacunas de cobertura. |
| Serviço externo ampliar escopo | Spell.sh restrito a assessment; nenhuma dependência de integração para finalizar o redesign. |

Bloqueadores de aceite: conteúdo enganoso, foto atribuída ao produto errado, perda/troca silenciosa de seleção, destino WhatsApp incorreto, ação essencial inacessível, falha JS que interrompe a jornada, asset essencial quebrado ou regressão responsiva que impede uso. Refinamentos cosméticos menores podem ir para backlog com responsável e impacto registrados.

A rodada de implementação estará concluída quando Luna e Astra tiverem contratos reconciliados, Terra entregar o diff autorizado e a validação comprovar os critérios aplicáveis, explicitando os não verificados. Publicação é uma ação separada. Nesta entrega, o resultado é exclusivamente este plano; não houve alteração do app, execução dos agentes, teste de navegador, contato externo ou deploy.
