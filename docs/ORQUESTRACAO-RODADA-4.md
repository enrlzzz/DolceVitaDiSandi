# Orquestração — rodada 4

Data: 20/09/2026. Responsável: Astra.
Status: especificação de execução e aceite. Nenhum teste foi executado nesta entrega documental e nenhum arquivo do app foi alterado.

## Objetivo

Corrigir alinhamento do menu Explorar, correspondência entre vídeos e thumbnails, reprodução do tutorial dentro da página e marca da galeria interna. Reavaliar a organização das seções e definir uma integração verificável de avaliações do Google, sem inventar conteúdo ou extrair páginas por scraping.

## Sequência e responsabilidades

| Etapa | Responsável | Entrega e condição de passagem |
| --- | --- | --- |
| Diagnóstico e conteúdo | Luna | Inventário das seções, IDs e CTAs; proposta de ordem e agrupamento; identificação verificável do último vídeo público do canal; inventário do tutorial, poster e perfil Google disponíveis. Registrar fontes, data da consulta e lacunas. |
| Coordenação | Astra | Conciliar o plano com este documento, definir estados sem conteúdo, evitar edições concorrentes e entregar critérios de aceite a Terra. |
| Implementação | Terra | Corrigir HTML/CSS/JS e configuração de conteúdo, preservando alterações existentes. Manter um responsável por arquivo compartilhado. Documentar onde atualizar vídeos, posters e avaliações. |
| Verificação | Terra / agente validador | Executar Playwright e inspeção visual nas páginas reais; anexar resultados e capturas; registrar limitações de serviços externos. |
| Correções e entrega | Terra, com revisão de Astra | Corrigir falhas, reexecutar cenários afetados e entregar link local, alterações, evidências e pendências reais. |

Mudanças locais já estão autorizadas no pedido principal. A falta de vídeo ou credenciais não impede correções independentes. Não declarar concluída uma integração externa apenas porque seu estado vazio funciona.

## Contrato dos componentes

### Header e organização das seções

- Inventariar os destinos existentes antes de reorganizar. Agrupar conteúdo por intenção: conhecer os doces, entender como pedir, conhecer a Sanderly e entrar em contato.
- Priorizar acessos a Doces, Como pedir e Contato; reunir destinos secundários em Explorar. Remover CTAs redundantes e distinguir vídeos de receitas do tutorial de compra.
- Alinhar o acionador Explorar aos demais links pelo centro vertical da área clicável, com tipografia e altura consistentes. O painel deve estar ancorado ao acionador e permanecer dentro da viewport.
- Usar botão/disclosure sem semântica de menu de aplicativo. Expor estado expandido e associação com o painel; garantir Tab, Enter/Espaço, Escape e toque. Ao fechar por Escape, devolver foco ao acionador. Ao navegar, não deixar foco em conteúdo oculto.
- Menu fechado não expõe links à ordem de Tab. Links reais resolvem IDs únicos e destinos não ficam encobertos pelo header. Movimento reduzido deve ser respeitado.
- Reordenar seções somente com mapa de antes/depois documentado; manter os destinos antigos quando possível e revisar links afetados.

### Da cozinha para a tela

- Thumbnail, título e link devem corresponder ao mesmo último vídeo público confirmado do canal oficial. Registrar ID, URL e data da verificação.
- Não confundir avatar do canal, foto de produto ou thumbnail de outro vídeo com a imagem do vídeo escolhido.
- Se a atualização for manual, documentar isso. Não anunciar atualização automática sem rotina de atualização implementada e testada.
- Reservar proporção da imagem, tratar falha sem loop e fornecer nome acessível coerente com a ação. Canal e vídeo podem ter links separados, com rótulos distintos.

### Veja como fazer um pedido

- Reproduzir dentro da página. O CTA do tutorial não deve redirecionar ao canal nem abrir nova aba como comportamento principal.
- Para arquivo da gravação, preferir `<video controls playsinline preload="metadata">` com poster do próprio vídeo. Para provedor suportado, usar iframe incorporado após interação.
- Centralizar fonte, título, tipo de player, poster e legendas/transcrição em configuração documentada. Poster deve ser um frame real do tutorial ou imagem fornecida para ele.
- Enquanto gravação/poster não existirem, apresentar indisponibilidade clara e manter os passos textuais. Não simular reprodução nem usar thumbnail de receita como se fosse o tutorial.
- Sem reprodução automática com som ao entrar na página. Se o player estiver em modal, fechar pausa/remove o player e retorna foco ao acionador.

### Acessibilidade e segurança do iframe/player

- Iframe tem `title` específico, dimensões/proporção reservadas e apenas permissões necessárias ao provedor. Validar URL e host permitido; não aceitar HTML arbitrário de iframe.
- O player é alcançável pelo teclado e possui controles utilizáveis. Não criar armadilha de foco nem cobrir controles com overlays.
- Se houver modal: nome acessível, botão de fechar visível, foco inicial, contenção de foco e retorno ao acionador. Verificar Escape com foco no documento; se o foco estiver dentro de iframe de outra origem, não presumir que o evento atravessa a fronteira. Garantir saída por teclado e testar o comportamento real do provedor.
- Prever legendas para fala e transcrição/instruções equivalentes. A ausência da gravação deve aparecer como pendência editorial, não como teste de acessibilidade aprovado.
- Conexões externas do player e das thumbnails devem corresponder ao comportamento documentado de privacidade.

### Galeria interna

- Reproduzir o defeito em `/Client/Public/Src/Pages/galeria.html` e identificar conflito entre marca, imagem, texto e estilos herdados.
- Corrigir o escopo dos estilos sem comprometer home, cardápio ou políticas. Logo mantém proporção, nome acessível e link funcional de retorno à home.
- Verificar que logo e texto não se sobrepõem, não são duplicados e não colidem com menu em desktop/mobile.
- Preservar filtros, imagens, lightbox, fechamento, teclado e retorno de foco.

### Avaliações do Google

- Google Analytics não é fonte de avaliações. Confirmar o Perfil da Empresa correto e o identificador exigido pela integração escolhida.
- Antes de implementar, consultar documentação oficial atual: [Places API](https://developers.google.com/maps/documentation/places/web-service/place-details) e [Business Profile — reviews](https://developers.google.com/my-business/reference/rest/v4/accounts.locations.reviews/list). Confirmar elegibilidade, autenticação, custos, limites de retorno, atribuição e regras de armazenamento/exibição aplicáveis à opção adotada.
- Escolher a API oficial adequada ao acesso disponível. Não raspar Google Maps/Busca, contornar bloqueios, reutilizar cookies de sessão nem incluir credenciais privadas/OAuth no frontend.
- Se precisar de credenciais privadas, usar backend com configuração de ambiente; nenhuma chave secreta ou token entra em arquivos públicos ou logs de teste. Não ativar serviço pago ou contratar fornecedor por inferência.
- Exibir autoria, origem, links e atribuições exigidas pela API. Não representar um subconjunto como todas as avaliações nem recalcular uma nota global a partir dele.
- Renderizar textos como texto, tratar resposta vazia, indisponibilidade e limites de requisição. Cache e retenção seguem as condições verificadas do provedor, sem prazo inventado.
- Sem acesso confirmado, disponibilizar link para o perfil oficial quando conhecido e/ou relatos cadastrados com autorização. Manter origem manual identificada; não anunciar sincronização ativa.
- Separar leitura de avaliações do formulário de envio de depoimentos. O formulário não publica no Google nem automaticamente no site.

## Validação Playwright

Confirmar que localhost serve este projeto. Inspecionar os validadores existentes antes de utilizá-los; não remover asserts para ocultar regressões. Executar a suíte existente e complementar somente lacunas relevantes desta rodada.

Comandos de referência, a confirmar no ambiente:

```powershell
python tools/serve-local.py
node --check Client/Public/Src/Js/script.js
git diff --check
python tools/validate-kapitana.py --screenshots
```

Iniciar servidor apenas se não houver instância correta disponível. Registrar comandos realmente executados, navegador, URL, data e resultados.

| Cenário | Evidência / aceite |
| --- | --- |
| Home e galeria em 320, 390, 768, 1024 e 1440 px | Capturas inspecionadas; sem overflow, recortes, logo sobreposta ou menu fora da tela. |
| Explorar com mouse, toque e teclado | Alinhamento visual correto; abre/fecha; Escape e foco funcionam; painel fechado não recebe Tab; todas as âncoras resolvem. |
| Zoom 200% e movimento reduzido | Conteúdo reflui, controles permanecem disponíveis e animação não impede uso. |
| Vídeo do canal | Comparar ID configurado, destino e origem da thumbnail; conferir imagem carregada e fallback com falha simulada. Verificação de “último vídeo” exige fonte externa datada. |
| Tutorial sem arquivo | Estado honesto, passos disponíveis, sem iframe vazio, link externo substituto ou erro de rede. |
| Tutorial com mídia de teste | Reprodução inline real, controles, poster correspondente e ausência de nova aba; remover fixture da configuração pública ao terminar. |
| Player/iframe | Nome acessível, percurso de foco, fechamento quando aplicável e interrupção de áudio. Resposta mockada não comprova reprodução real de provedor externo. |
| Avaliações | Testar resposta válida, vazia, erro e texto com marcação usando fixtures; nenhuma execução de HTML nem credencial exposta. Integração real só aprovada após consulta oficial bem-sucedida. |
| Galeria interna | Logo, retorno à home, filtros e lightbox funcionam; Escape e foco preservados. |
| Regressão | Seleção de produtos, carrossel, WhatsApp e páginas internas continuam funcionais; interceptar abertura de WhatsApp sem enviar mensagem real. |
| Console e rede | Ausência de erros de app e assets locais quebrados; falhas externas registradas separadamente, sem ocultá-las. |

Playwright complementa a inspeção visual e manual de teclado; não certifica sozinho acessibilidade integral. Conferir contraste, foco visível, ordem de títulos e nomes acessíveis dos controles alterados.

## Critérios finais de aceite

- [ ] Luna entregou mapa das seções e conteúdo confirmado/pendente.
- [ ] Explorar está alinhado e utilizável por teclado/toque em todos os tamanhos previstos.
- [ ] Vídeo do canal, link e thumbnail correspondem à mesma publicação verificada.
- [ ] Tutorial funciona dentro da página quando há arquivo; sem arquivo, pendência aparece claramente.
- [ ] Player atende ao contrato de acessibilidade e não deixa áudio tocando após fechamento.
- [ ] Marca da galeria corrigida sem regressões nas outras páginas.
- [ ] Avaliações usam fonte oficial ou curadoria manual identificada; nenhuma coleta insegura, dado fictício ou sincronização alegada sem implementação.
- [ ] Playwright foi executado, falhas corrigidas e cenários afetados reexecutados.
- [ ] Entrega inclui capturas, resultados, local de configuração e dependências ainda ausentes.

Este documento define o aceite; os itens permanecem pendentes até haver evidência de execução. Pendências de conteúdo ou acesso externo devem ser destacadas na entrega sem impedir as correções locais já autorizadas.
