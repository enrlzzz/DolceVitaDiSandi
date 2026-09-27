# Orquestração — rodada 3

Data: 20/09/2026. Responsável por este documento: Astra.
Status: contrato de execução e validação; testes ainda não executados nesta entrega documental.

## Escopo

Organizar a implementação de depoimentos, acesso às seções pelo header, thumbnail em “Da cozinha para a tela”, thumbnail para o futuro tutorial de pedido e crédito de desenvolvimento no footer. A execução inclui correção de bugs relacionados e validação com Playwright. Esta entrega de Astra altera somente este documento; não modifica o app.

Arquivos ativos observados: `Client/Public/Src/Pages/index.html`, `Client/Public/Src/Js/script.js` e `Client/Public/Src/Styles/editorial.css`. Há alterações preexistentes no workspace: preservar o trabalho, revisar o diff e coordenar a propriedade dos arquivos antes de editar.

## Ordem e contratos de passagem

| Etapa | Entrega | Condição de passagem |
| --- | --- | --- |
| Luna — planejamento | Mapa das seções, proposta de navegação, textos, origem dos depoimentos, vídeo e thumbnail confirmados, lacunas e fallbacks. | Cada conteúdo tem origem ou estado vazio definido; URL do canal não é tratada como URL de vídeo. |
| Astra — orquestração | Conciliar o plano de Luna com este contrato, distribuir arquivos e transformar requisitos em critérios verificáveis. | Terra recebe decisões consistentes sobre menu, dados configuráveis, estados sem conteúdo e testes. |
| Terra — execução | Implementar componentes, dados/configuração, responsividade e correções nos arquivos ativos; documentar como substituir conteúdo. | Diff revisado, verificações estáticas concluídas e localhost disponível para a validação. |
| Validação Playwright | Executar regressões e cenários desta rodada; registrar ambiente, resultados e capturas; devolver falhas a Terra. | Falhas bloqueadoras corrigidas e cenários afetados reexecutados. |

A execução do app já foi solicitada no pedido principal; este fluxo não exige nova aprovação para alterações locais dentro do escopo. Astra não deve assumir que um plano ou teste está concluído sem a entrega correspondente. Implementação em arquivos compartilhados tem um único responsável por vez. Falhas de conteúdo retornam a Luna; dúvidas de composição e prioridade retornam a Astra; bugs retornam a Terra.

## Decisões por componente

### Navegação completa

Inventariar os IDs reais antes de implementar. Foram observados `inicio`, `doces`, `galeria`, `ingredientes`, `historia`, `videos`, `ocasioes`, `temporada`, `como-pedir`, `clientes`, `duvidas` e `contato`. Todos devem ser alcançáveis pelo header, sem exigir que todos os links apareçam na mesma linha.

Proposta: marca → início; acessos principais para Doces, Como pedir e Contato; botão “Explorar” para as demais seções. No mobile, um menu expansível reúne todos os destinos com rótulos claros. Manter “Minha seleção” acessível. Usar links nativos para âncoras e botão nativo para expansão; não aplicar `role="menu"` a uma navegação comum sem implementar todo o padrão de teclado correspondente.

O botão de expansão expõe `aria-expanded` e `aria-controls`. Escape fecha o painel e devolve foco ao acionador; escolher um link fecha o painel. O painel fechado não mantém links na ordem de Tab. Compensar a altura real do header ao navegar, inclusive com zoom, e respeitar movimento reduzido. A navegação deve continuar útil com JavaScript indisponível.

### Depoimentos

Evoluir a seção `clientes` com área para depoimentos reais e uma ação para enviar relato pelo canal de contato existente. Separar exibição de avaliações e envio de um novo relato. No site estático, informar corretamente que o envio será concluído no WhatsApp; não simular publicação ou armazenamento em servidor.

Definir registros com ID estável, texto, nome de exibição aprovado, fonte, data opcional e URL da origem opcional. Guardar evidência de autorização e contato privado fora dos dados públicos do site. Usar texto simples ao renderizar conteúdo. Sem registros confirmados, apresentar convite honesto, sem estrelas, contadores ou comentários inventados.

Luna deve explicar no guia de preenchimento a diferença entre mensuração de visitas no Analytics e avaliações do Perfil da Empresa no Google. Verificar a documentação oficial antes de recomendar integração ou republicação automática. A rodada pode trabalhar com cadastro manual de relatos autorizados; integração com Google exige decisão própria sobre acesso, condições de uso e manutenção. Não extrair comentários automaticamente nem expor credenciais no navegador.

### Vídeos da cozinha

Adicionar thumbnail com proporção reservada, título e indicação clara de reprodução. Quando houver vídeo confirmado, thumbnail e CTA apontam para o mesmo vídeo. Uma foto editorial pode ser fallback, identificada pelo contexto, mas não deve ser apresentada como frame real de um vídeo desconhecido. Se só houver o canal, manter ação “Ver vídeos no YouTube”, sem prometer reprodução de um vídeo específico.

### Tutorial em “Como pedir”

Posicionar o cartão de vídeo entre a introdução e os passos, ou no centro da composição desktop, preservando ordem de leitura no mobile. Preparar uma configuração única para URL, título e thumbnail que Enrico preencherá com a gravação do Recordly.

Sem URL, mostrar estado “Vídeo em breve”. Caso a thumbnail permaneça clicável, a ação abre uma explicação acessível de indisponibilidade, sem player vazio, link `#`, reprodução falsa ou solicitação de rede inválida. Com URL válida, a mesma área abre o vídeo. Terra documenta o local exato para configurar e demonstra os dois estados com fixture de teste, sem publicar conteúdo fictício.

### Crédito no footer

Inserir “Desenvolvido por Enrico” na faixa inferior, junto ao copyright e separado dos links de políticas. Usar hierarquia secundária com contraste legível e quebra de linha no mobile. Só incluir link de portfólio quando houver URL fornecida ou confirmada; o nome pode ficar em texto simples. O crédito não deve ampliar excessivamente o footer ou competir com o contato da doceria.

## Critérios técnicos e segurança de vídeo

- Centralizar os dados configuráveis; documentar campos obrigatórios, opcionais e estados ausentes. Preservar seleção de produtos, carrossel, WhatsApp e internas.
- Analisar URLs com `URL`; permitir somente HTTPS e hosts explicitamente suportados. Comparar host exato, não substring: `youtube.com.exemplo.test` não é YouTube.
- Para YouTube, extrair e validar o ID de formatos suportados e construir a URL do player a partir dele. Rejeitar `javascript:`, `data:`, URLs inválidas, credenciais embutidas e HTML de iframe colado.
- Se aceitar vídeo local, limitar a caminhos e formatos previstos no projeto; não aceitar um caminho arbitrário como HTML. URLs rejeitadas caem no estado indisponível e não entram em `href`/`src`.
- Usar `textContent` para textos editáveis; não interpolar relatos, títulos ou URLs não validados em `innerHTML`.
- Links com nova aba usam `rel="noopener noreferrer"`. Player externo só é criado após ação explícita; sem autoplay com som ao carregar a página.
- Iframe tem título descritivo e permissões limitadas ao necessário. Fechar modal interrompe vídeo/áudio, remove o player e restaura o foco. Um vídeo local usa controles nativos.
- Thumbnail reserva dimensões, possui fallback de erro sem loop, carrega sob demanda abaixo da dobra e não causa salto de layout. Texto próximo e nome acessível explicam a ação; evitar leitura duplicada da mesma descrição.
- Se mudar o carregamento de serviços externos, registrar o comportamento real para revisão da política de privacidade. Não afirmar que o site é livre de conexões externas sem conferir a rede.
- Não instalar nova infraestrutura ou biblioteca para componentes que podem ser implementados no projeto estático. Não enviar mensagens, publicar avaliações ou criar pedidos reais durante os testes.

## Acessibilidade e responsividade

- Validar larguras de 320, 390, 768, 1024 e 1440 CSS px; conferir zoom de 200% e reflow equivalente a 320 px. Sem overflow horizontal, texto cortado ou ações sobrepostas.
- Navegar por Tab, Shift+Tab, Enter, Espaço e Escape conforme cada controle. Foco sempre visível; conteúdo de painel/modal fechado não recebe foco.
- Modal possui nome acessível, foco inicial adequado, contenção de foco enquanto aberto e retorno ao acionador. Não usar apenas clique no backdrop para fechar.
- Manter contraste de texto comum de pelo menos 4,5:1 e texto grande de 3:1; controles e indicadores essenciais distinguíveis do fundo. Planejar alvos de toque de pelo menos 44 × 44 CSS px.
- Respeitar `prefers-reduced-motion` em rolagem e animações. Hover não é a única forma de revelar informação ou ação.
- Manter títulos e landmarks coerentes, IDs únicos, labels nos campos e erros associados. Se houver formulário de relato, pedir apenas o necessário e deixar explícito o destino da mensagem.
- Tutorial futuro deve prever legendas ou transcrição; registrar essa pendência editorial enquanto a gravação não existe.

## Plano de validação Playwright

O projeto possui `tools/serve-local.py` e `tools/validate-kapitana.py`. O validador existente usa Playwright com canal `msedge`, cobre home e internas e aceita `--screenshots`. Terra deve revisar sua compatibilidade com o HTML final, sem remover verificações para esconder regressões. O sucesso dessa suíte isoladamente não comprova todos os cenários novos.

Sequência operacional proposta:

```powershell
# Em uma sessão de servidor, somente se a porta ainda não estiver em uso pelo projeto:
python tools/serve-local.py

# Em outra sessão:
node --check Client/Public/Src/Js/script.js
git diff --check
python tools/validate-kapitana.py --screenshots
```

Confirmar que `http://127.0.0.1:8000/` serve este projeto. Registrar navegador, viewport e comando realmente executados. Complementar a suíte com cenários focados nos novos componentes:

| Cenário | Resultado esperado |
| --- | --- |
| Header desktop/mobile e todos os destinos | Links resolvem IDs únicos; painel abre/fecha; destino visível sob header; foco não fica em painel oculto. |
| Depoimentos vazios e fixture com relato longo | Estado vazio honesto; conteúdo quebra corretamente; caracteres especiais preservados e marcação tratada como texto. |
| Envio de relato | URL de WhatsApp e mensagem codificada corretas; nenhuma mensagem realmente enviada. |
| Thumbnail da cozinha | Imagem válida ou fallback; ação corresponde a vídeo/canal configurado; falha de imagem simulada não quebra layout. |
| Tutorial sem URL, URL válida e URL inválida | Estado em breve, reprodução/link funcional e rejeição segura, respectivamente. Incluir tentativa com host enganoso e protocolo proibido. |
| Modal de vídeo, se implementado | Teclado, Escape, foco e interrupção do player corretos; nenhum iframe antes do clique. |
| Footer | Crédito discreto e legível; políticas funcionam; botão flutuante não cobre links. |
| Regressões | Filtros, seleção persistida, remoção, mensagem de pedido, carrossel, galeria e FAQ continuam operantes. |
| Rede e console | Zero erros de aplicação, assets locais ausentes ou requisições de vídeo malformadas. Falhas externas registradas separadamente. |
| Movimento reduzido e zoom | Conteúdo e ações disponíveis; sem animação imposta nem sobreposição. |

Usar interceptação/fixtures para testar URLs e conteúdo configurável sem depender de anúncios, consentimento ou disponibilidade do YouTube. Distinguir testes com rede simulada de reprodução externa realmente observada. Capturar home desktop/mobile e detalhes de menu, vídeos, depoimentos e footer; inspecionar visualmente as capturas. Captura produzida sem inspeção não vale como aceite visual. Automação não substitui a conferência manual de foco, leitura, contraste e composição.

## Checklist de aceite e handoff

- [ ] Plano de Luna reconciliado; fontes e lacunas documentadas.
- [ ] Todas as seções acessíveis pelo header e navegação responsiva aprovada.
- [ ] Área de depoimentos e canal de envio implementados sem relatos fictícios.
- [ ] Thumbnail da cozinha aplicada com destino e fallback corretos.
- [ ] Tutorial central preparado e estados com/sem vídeo verificados.
- [ ] Crédito de Enrico inserido, sem link de portfólio inventado.
- [ ] URLs de vídeo validadas; nenhuma credencial ou HTML arbitrário publicado.
- [ ] Teclado, foco, contraste, movimento reduzido e reflow conferidos.
- [ ] Regressões funcionais e cenários novos executados via Playwright.
- [ ] Capturas inspecionadas; bugs encontrados corrigidos e retestados.
- [ ] Guia informa onde preencher depoimentos, fontes, thumbnails, vídeo Recordly e portfólio.
- [ ] Relatório lista arquivos alterados, comandos, resultados e pendências editoriais reais.

Bloqueiam o aceite: regressão de pedidos, links quebrados, perda de acesso por teclado, execução de conteúdo arbitrário, overflow que esconda ações ou reprodução prometida sem conteúdo. Vídeo Recordly e depoimentos ainda não fornecidos são pendências editoriais compatíveis com aceite técnico quando seus estados vazios estão corretos. Entregar o endereço do localhost somente após verificar que está respondendo. Não declarar testes aprovados ou deploy realizado sem evidência.
