# Plano da Rodada 3 — depoimentos, conteúdo em vídeo e navegação

**Responsável pelo planejamento:** Luna  
**Orquestração prevista:** Astra  
**Execução prevista:** Terra  
**Escopo:** planejar a próxima melhoria da home da Dolce Vita Di Sandi sem editar arquivos do app nesta etapa.

## 1. Objetivo

Evoluir a home para que ela apresente prova social verdadeira, conteúdo em vídeo e uma navegação completa sem transformar o header em uma lista cansativa de links. A rodada também deve manter o caráter artesanal, o carregamento leve, a acessibilidade e o fluxo de pedido pelo WhatsApp.

O plano parte da estrutura atual da home, que já contém as âncoras `#doces`, `#galeria`, `#ingredientes`, `#historia`, `#videos`, `#ocasioes`, `#temporada`, `#como-pedir`, `#clientes`, `#duvidas` e `#contato`.

## 2. Depoimentos: fonte, consentimento e arquitetura

### 2.1 O que pode e não pode ser obtido de cada fonte

| Fonte | Serve para obter depoimentos? | Como usar com segurança |
|---|---|---|
| Google Business Profile / Perfil da Empresa no Google | Sim. As avaliações públicas do perfil da doceria podem ser selecionadas para exibição, com link para a avaliação original. | Conferir se o perfil é realmente da Dolce Vita, copiar o texto sem alterar o sentido, registrar nome/foto exibidos e guardar a URL da avaliação. Pedir autorização adicional se houver uso promocional de foto ou identificação além do que está público. |
| Google Analytics | Não. Analytics mede visitas e eventos; não é uma base de comentários nem fornece avaliações de clientes. | Não usar Analytics como origem de depoimentos. Se for instalado futuramente, revisar a política de privacidade e consentimento conforme a configuração adotada. |
| WhatsApp / mensagens de clientes | Sim, mediante autorização explícita. | Pedir permissão para publicar o texto, definir se o nome será completo, primeiro nome, iniciais ou bairro, e confirmar se fotos/prints também podem ser usados. |
| Formulário próprio | Sim, e é a fonte mais controlável para novos relatos. | Criar campo de texto, identificação opcional, pedido/evento e checkbox separado autorizando publicação. Não publicar automaticamente: deixar em estado “aguardando aprovação”. |
| Instagram, YouTube e outras redes | Possivelmente, mas comentários não devem ser republicados automaticamente. | Solicitar autorização ao autor e guardar a resposta. Usar o link da publicação original quando apropriado. |

### 2.2 Recomendação

Começar com uma arquitetura híbrida:

1. importar manualmente de 3 a 6 avaliações reais do Google Business Profile;
2. solicitar novos relatos pelo WhatsApp ou por formulário curto;
3. publicar somente depoimentos aprovados pela Sanderly;
4. mostrar uma chamada “Ver todas as avaliações no Google” apontando para o perfil oficial;
5. manter a origem e a data de revisão em um arquivo de dados interno, mesmo que esses campos não apareçam na tela.

Não criar depoimentos de exemplo apresentados como reais. Enquanto não houver relatos autorizados, usar o bloco como convite (“Conte como foi sua experiência”) ou ocultá-lo, em vez de preencher com texto fictício.

### 2.3 Modelo de dado recomendado

Manter os depoimentos separados do HTML, em JSON local ou em uma constante de dados:

```json
{
  "id": "depoimento-001",
  "quote": "Texto autorizado pelo cliente.",
  "authorLabel": "Marina, Sorocaba",
  "source": "Google Business Profile",
  "sourceUrl": "URL-da-avaliacao-ou-do-perfil",
  "approvedAt": "AAAA-MM-DD",
  "permission": "publico-ou-autorizado",
  "status": "published"
}
```

Campos privados, como telefone, nome completo não aprovado ou conversa integral, não devem ir para o arquivo público. Para um volume maior, migrar esse fluxo para um painel protegido; não usar o navegador como banco de aprovação.

### 2.4 Conteúdo que precisa ser confirmado pela família

- URL oficial do Perfil da Empresa no Google;
- quais avaliações podem ser exibidas;
- nome, iniciais ou bairro permitidos para cada cliente;
- autorização para foto, avatar, print ou imagem do pedido;
- canal para receber novos depoimentos;
- pessoa responsável por aprovar, editar apenas formatação e remover relatos;
- prazo para retirada de um depoimento quando o cliente pedir.

## 3. Reorganização da header sem poluição visual

### 3.1 Princípio

Não colocar todas as 11 seções como links horizontais. O header deve continuar reconhecível em desktop e utilizável em telas estreitas. A marca leva ao início, quatro links levam aos destinos principais e um menu “Explorar” agrupa o conteúdo secundário. O CTA de encomenda fica sempre visível.

### 3.2 Estrutura proposta

| Elemento | Destino/conteúdo |
|---|---|
| Logo “Dolce Vita Di Sandi” | `#inicio` |
| Doces | `#doces` |
| Nossa história | `#historia` |
| Galeria | `#galeria` |
| Explorar | menu agrupado: `#ingredientes`, `#videos`, `#ocasioes`, `#temporada`, `#como-pedir`, `#clientes`, `#duvidas` |
| CTA “Encomendar” | `#contato` ou abertura do fluxo de seleção/WhatsApp |
| Seleção | modal “Minha seleção”, preservando o contador atual |

No mobile, “Explorar” deve ser um botão/disclosure acessível, não um submenu que só funciona com hover. Ao escolher uma âncora, fechar o menu e preservar a rolagem suave. Em páginas internas, manter “Voltar ao site” e um CTA curto, sem replicar a navegação completa da home.

### 3.3 Regras de interação

- usar links reais para as âncoras, com `scroll-behavior: smooth` apenas quando o usuário não solicitou redução de movimento;
- manter `scroll-padding-top`/`scroll-margin-top` compatível com a altura real do header;
- permitir teclado, Escape e clique fora para fechar o menu;
- indicar foco e estado aberto com `aria-expanded` e `aria-controls`;
- não capturar wheel, touch ou Page Down para fabricar uma rolagem artificial;
- atualizar o estado visual do grupo ativo apenas se isso não gerar falsa precisão durante a rolagem;
- validar que cada link aponta para um ID existente.

## 4. Thumbnail da seção “06 / DA COZINHA PARA A TELA”

### Componente previsto

Transformar o cartão atual de vídeo em um bloco editorial com:

- thumbnail real do vídeo escolhido do canal oficial;
- botão/play sobreposto com nome acessível;
- título e descrição do vídeo;
- duração apenas se confirmada, sem inventar metadados;
- link para o YouTube em nova aba como fallback;
- `loading="lazy"`, dimensões reservadas e imagem comprimida para evitar salto de layout.

### Dados necessários

- URL ou ID do vídeo específico que representará a seção;
- confirmação de que o vídeo pode ser destacado;
- thumbnail oficial ou autorização para capturar/usar uma imagem do vídeo;
- título e descrição aprovados;
- decisão entre abrir o YouTube ou incorporar o vídeo em modal.

A opção mais resiliente é armazenar uma thumbnail local em `Assets` e manter o link externo. Se houver modal incorporado, carregar o iframe somente após o clique, preferencialmente com `youtube-nocookie.com`, botão de fechar, foco controlado e alternativa “Assistir no YouTube”. Não depender de uma chamada não autenticada ao YouTube para montar a home.

## 5. Thumbnail clicável em “Como pedir com carinho”

Adicionar entre o título/explicação e os três passos um card de tutorial com:

- imagem/poster local provisório;
- sobreposição “Assistir como pedir”;
- texto informando que é uma simulação do pedido no site;
- `data-video-url` ou campo de configuração preparado para receber a URL quando o vídeo do Recordly estiver pronto;
- modal de vídeo reutilizando a mesma infraestrutura do bloco do YouTube, mas com conteúdo configurável;
- fallback visual e textual caso a URL ainda esteja vazia: “Vídeo em breve — veja os passos abaixo”.

O poster não deve fingir ser uma gravação pronta. Enquanto o Recordly não for produzido, usar uma imagem neutra da interface ou uma arte explicitamente marcada como “prévia”. O vídeo deve explicar escolha do produto, quantidade/data, revisão da mensagem e envio manual pelo WhatsApp; não deve sugerir que o site confirma sozinho o pedido.

## 6. Crédito do desenvolvedor

O local mais estratégico é o rodapé, na linha legal secundária, com baixo destaque e sem competir com WhatsApp, políticas ou marca:

`Site desenvolvido por Enrico`.

Se houver portfólio ou GitHub público aprovado, transformar o texto em link externo com `target="_blank"` e `rel="noopener noreferrer"`. Se não houver URL confirmada, deixar texto simples. O crédito deve ter contraste suficiente, foco visível e texto acessível; não inserir watermark sobre fotos, hero ou CTA.

Opcionalmente, incluir também uma linha discreta na página de políticas, mas não repetir o crédito em todas as seções.

## 7. Riscos e mitigação

| Risco | Mitigação |
|---|---|
| Publicar avaliação sem autorização ou fora de contexto | Manter status de aprovação, origem, data e registro da autorização; oferecer remoção. |
| Confundir Google Analytics com avaliações | Documentar que Analytics é medição, não fonte de comentários; usar Perfil da Empresa no Google para reviews. |
| Header ficar apertado ou cobrir seções | Agrupar links em “Explorar”, testar 320/390/768/1440 px e usar âncoras com offset. |
| Thumbnail externa quebrar ou ficar desatualizada | Copiar poster otimizado para o projeto e manter link externo como alternativa. |
| Iframe pesar a página ou criar problema de privacidade | Carregar somente após clique, usar domínio privacy-enhanced, botão de saída e fallback para YouTube. |
| Vídeo do Recordly ainda não existir | Estado “em breve” real, sem player quebrado nem thumbnail enganosa. |
| Animação prejudicar acessibilidade | Respeitar `prefers-reduced-motion`, manter controles nativos e não esconder o conteúdo atrás do movimento. |
| Crédito do desenvolvedor parecer anúncio | Colocar apenas no rodapé, com hierarquia visual secundária e sem CTA adicional. |
| Texto do depoimento ficar desatualizado | Guardar `approvedAt`, revisar periodicamente e criar processo simples de remoção. |

## 8. Ordem de execução

1. **Luna:** confirmar este contrato, fontes de depoimento, IDs de navegação e pendências de conteúdo.
2. **Astra:** transformar o plano em especificação visual/interativa, incluindo estados desktop, mobile, teclado, modal e reduced motion.
3. **Terra:** implementar dados, header agrupado, bloco de depoimentos, thumbnails, modal de vídeo, crédito e estilos.
4. **Validação:** testar com Playwright em 320, 390, 768 e 1440 px; conferir navegação, foco, modais, links externos e falhas de imagem/URL.

## 9. Critérios de aceite

### Depoimentos

- [ ] Nenhum texto publicado é fictício ou apresentado como avaliação real sem origem.
- [ ] Cada depoimento publicado tem fonte, data de revisão e autorização/condição de publicação registrada.
- [ ] Existe link para o Perfil da Empresa no Google, quando a URL for confirmada.
- [ ] Google Analytics não é tratado como fonte de depoimentos.
- [ ] O bloco vazio ou pendente tem estado honesto e CTA para enviar relato.

### Header e rolagem

- [ ] Todas as seções relevantes estão acessíveis pelo menu “Explorar” ou pelos links principais.
- [ ] Não há overflow horizontal nem links encobertos pelo header.
- [ ] Menu funciona com teclado, Escape, foco visível e toque.
- [ ] `prefers-reduced-motion` desativa rolagem/animações não essenciais.

### Vídeos

- [ ] A seção 06 mostra uma thumbnail real ou um estado de conteúdo pendente claramente identificado.
- [ ] O clique abre o vídeo certo ou o YouTube correto; não abre um player quebrado.
- [ ] O tutorial de “Como pedir” aceita a URL futura do Recordly sem nova alteração estrutural.
- [ ] Modal tem nome acessível, fechamento por Escape, foco adequado e fallback externo.

### Rodapé

- [ ] O crédito “Site desenvolvido por Enrico” aparece uma vez, em posição discreta.
- [ ] O crédito não desloca políticas, contato, logo ou CTA em telas pequenas.

### QA geral

- [ ] Playwright não acusa erros de console, imagens quebradas ou links internos sem destino.
- [ ] Não há overflow em 320, 390, 768 e 1440 px.
- [ ] O fluxo de seleção continua abrindo mensagem revisável no WhatsApp, sem enviar automaticamente.
- [ ] O site continua legível quando JavaScript falha, ao menos para navegação e conteúdo essencial.

## 10. Pendências para liberar a implementação

- URL do Perfil da Empresa no Google;
- lista inicial de avaliações autorizadas;
- URL/ID do vídeo que receberá thumbnail na seção 06;
- poster ou vídeo da simulação no Recordly;
- URL de portfólio/GitHub do desenvolvedor, se o crédito for clicável;
- confirmação de que “Site desenvolvido por Enrico” é o texto desejado.

