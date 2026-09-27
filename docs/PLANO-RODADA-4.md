# Plano da Rodada 4 — navegação, vídeos, avaliações e consistência visual

**Responsável pelo planejamento:** Luna  
**Orquestração prevista:** Astra  
**Execução prevista:** Terra  
**Escopo desta etapa:** planejamento apenas. Nenhum arquivo do app deve ser alterado por Luna.

## 1. Objetivo

Corrigir os pontos de confusão percebidos na rodada anterior sem perder o caráter editorial da Dolce Vita Di Sandi:

- alinhar corretamente o item `Explorar` no header;
- separar visual e tecnicamente o último vídeo do canal do tutorial de pedido;
- manter o tutorial Recordly embutido na própria página;
- avaliar avaliações reais do Perfil da Empresa no Google sem inventar nem importar dados de forma insegura;
- reorganizar as seções para que a jornada da página fique clara;
- corrigir o conflito da logo na galeria interna;
- validar desktop, mobile, teclado, links, vídeo e ausência de erros no console com Playwright.

## 2. Decisões de produto

### 2.1 Header e “Explorar”

O header deve ter uma hierarquia curta:

1. marca apontando para `#inicio`;
2. links principais: `Doces`, `Nossa história` e `Galeria`;
3. menu `Explorar` contendo as seções secundárias;
4. CTA de pedido sempre visível.

O item `Explorar` não deve depender de espaçamento manual para parecer alinhado. O menu deve ser um componente único, com o rótulo e o ícone dentro do mesmo botão, alinhamento por `inline-flex`, altura consistente com os demais links e estado aberto acessível.

Critérios:

- mesma linha de base dos links vizinhos em desktop;
- área de toque mínima de 44px;
- menu fecha ao clicar fora, pressionar `Escape` ou escolher uma âncora;
- `aria-expanded`, `aria-controls` e foco visível atualizados corretamente;
- no mobile, o menu não pode ultrapassar a viewport nem ficar atrás do conteúdo.

### 2.2 Arquitetura da página

A ordem recomendada da home é:

1. hero/carrossel — identidade e produto principal;
2. doces — escolha rápida do cardápio;
3. ocasiões — descoberta por necessidade;
4. temporada — urgência e disponibilidade;
5. como pedir — redução de dúvida;
6. vídeo da cozinha — vínculo com a Sanderly;
7. tutorial de pedido — demonstração prática do fluxo;
8. galeria — prova visual;
9. história e ingredientes — confiança e origem;
10. avaliações — prova social;
11. dúvidas — objeções finais;
12. contato/CTA final.

O header deve apontar somente para os destinos mais úteis. As outras seções ficam dentro de `Explorar`, com rótulos compreensíveis e sem repetir o mesmo destino em vários lugares.

## 3. Vídeos: duas funções, dois componentes

### 3.1 “Da cozinha para a tela”

Esta seção representa o conteúdo público do canal. Deve exibir a thumbnail e o título do **último vídeo real do canal**, com link para o vídeo correto no YouTube.

Fonte preferencial:

- URL do vídeo mais recente confirmada manualmente pela família; ou
- feed/API oficial do YouTube em uma etapa futura.

Não usar uma thumbnail genérica do canal nem manter um link de vídeo diferente do texto exibido. A thumbnail, o título, o `href` e o `aria-label` precisam referir-se ao mesmo vídeo.

### 3.2 “Veja como fazer um pedido”

Esta seção deve conter um vídeo **embutido na própria página**, sem mandar a pessoa para o YouTube para assistir.

Implementação recomendada:

- usar `<iframe>` somente quando houver URL/embed real do Recordly;
- manter uma thumbnail de capa enquanto o vídeo não tiver URL confirmada;
- ao clicar na thumbnail, trocar a capa pelo player embutido ou abrir um `<dialog>` com o iframe;
- não iniciar áudio automaticamente;
- usar `loading="lazy"`, `title` descritivo e `allow="fullscreen; picture-in-picture"`;
- aplicar `referrerpolicy` adequada e não inserir scripts de terceiros desnecessários.

Se o Recordly gerar um arquivo local ou uma URL de vídeo própria, preferir o player HTML5 local/embutido. Se gerar somente uma URL pública, confirmar se ela permite incorporação. Até essa confirmação, exibir “Vídeo tutorial em breve” ou uma capa não interativa, sem apontar para o YouTube por engano.

## 4. Avaliações do Google Business Profile

### 4.1 O que é possível

O Google Analytics não fornece avaliações. Ele mede tráfego e eventos. As avaliações devem vir do Perfil da Empresa no Google, por exportação/manual, link oficial do perfil ou integração autorizada.

### 4.2 Estratégia segura para esta rodada

Começar com conteúdo curado manualmente:

1. confirmar a URL oficial do Perfil da Empresa da Dolce Vita Di Sandi;
2. selecionar de 3 a 6 avaliações públicas reais;
3. registrar texto, nome exibido, data, URL do perfil/avaliação e data de revisão;
4. publicar somente avaliações verificadas pela Sanderly;
5. incluir CTA “Ver todas as avaliações no Google” apontando para o perfil oficial;
6. se não houver avaliações confirmadas, mostrar convite para avaliar ou formulário de depoimento, nunca texto fictício.

Modelo público sugerido:

```json
{
  "id": "google-001",
  "quote": "Texto publicado na avaliação.",
  "authorLabel": "Nome exibido pelo Google",
  "rating": 5,
  "source": "Google Business Profile",
  "sourceUrl": "URL oficial",
  "reviewDate": "AAAA-MM-DD",
  "checkedAt": "AAAA-MM-DD",
  "status": "published"
}
```

Não armazenar no front-end telefone, e-mail, nome completo não aprovado, print privado ou conversa do cliente. Não automatizar scraping do Google. Para integração em escala, avaliar depois a API oficial, credenciais protegidas em servidor e revisão dos termos do Google.

### 4.3 Consentimento e remoção

Para avaliações públicas, manter o link de origem e não alterar o sentido do texto. Para WhatsApp, Instagram, YouTube ou formulário próprio, solicitar autorização explícita para publicação e definir se serão usados nome, iniciais, cidade, foto ou imagem do pedido. Deve existir um canal para pedir remoção ou correção.

## 5. Conflito da logo na galeria interna

Investigar se a galeria está carregando simultaneamente:

- a logo textual do template interno;
- a logo PNG oficial;
- estilos de `styles.css` e `interiors.css` com seletores concorrentes;
- uma imagem absoluta ou duplicada no mesmo canto.

Correção planejada:

- escolher um único componente de marca para páginas internas;
- manter a logo oficial em um único `<a>` dentro do header;
- remover duplicidade de imagem/texto ou ocultação que deixe elementos sobrepostos;
- conferir `position`, `z-index`, dimensões e `object-fit` em desktop e mobile;
- manter o link da marca apontando para a home;
- validar contraste e foco do link.

O arquivo da logo deve ser transparente e não receber fundo bege artificial. Se a arte oficial for escura demais para o header, usar uma versão visualmente adaptada por CSS ou colocá-la em uma área com contraste suficiente, sem adicionar uma “bolha” decorativa que pareça erro de composição.

## 6. Critérios de aceite

### Header

- `Explorar` alinhado verticalmente com todos os links;
- abertura, fechamento, teclado e clique fora funcionando;
- nenhum menu cortado em 320px, 390px, 768px e 1440px;
- todas as âncoras levam à seção correta com scroll suave.

### Vídeos

- thumbnail da seção da cozinha corresponde ao último vídeo real;
- link da thumbnail e título apontam para o mesmo vídeo;
- tutorial Recordly não aponta para o YouTube;
- tutorial permanece na página quando incorporado;
- fallback visual é honesto quando ainda faltar URL.

### Avaliações

- nenhum depoimento inventado;
- cada avaliação publicada tem origem e revisão identificáveis;
- CTA do Google aponta para o perfil oficial confirmado;
- formulário próprio mantém aprovação manual.

### Galeria

- uma única logo visível no canto superior esquerdo;
- sem sobreposição, piscada ou deslocamento ao carregar;
- logo acessível por teclado e responsiva.

### Qualidade

- Playwright em 320, 390, 768 e 1440px;
- console sem erros JavaScript;
- sem links quebrados, imagens ausentes ou overflow horizontal;
- teste de reduced motion;
- teste de foco por teclado;
- `git diff --check`, `node --check` e validação existente executados.

## 7. Dados que Terra deve pedir antes de publicar conteúdo real

- URL do Perfil da Empresa no Google;
- URL e título do último vídeo do canal;
- URL/embed ou arquivo final do vídeo Recordly;
- thumbnail autorizada do tutorial;
- avaliações selecionadas e autorização aplicável;
- confirmação da versão oficial transparente da logo.

Enquanto esses dados não forem entregues, Terra deve preservar placeholders identificados como tais, sem mascará-los como conteúdo real.
