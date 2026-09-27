# Plano da Rodada 5 — fotos editadas, vídeo próprio e segurança

## Objetivo

Atualizar o site com cópias locais somente das fotos editadas de produtos fornecidas em Downloads, sem apagar ou mover os arquivos originais, substituir referências antigas com mapeamento explícito e preparar o tutorial de pedido para um vídeo próprio, embutido por `<video>` e configurável sem YouTube.

## Inventário e regras de assets

- Origem: `D:\[HD] Gerais\[HD] Downloads\[HD]\Downloads`.
- Destino: `Client/Public/Src/Assets/rodada-5/produtos-editados/`.
- Copiar apenas arquivos identificados como fotos editadas de produtos; não copiar executáveis, arquivos de projeto, vídeos ou imagens de fundo.
- Não apagar, mover ou sobrescrever os arquivos de Downloads.
- Manter nomes seguros e estáveis no destino, com um manifesto de origem, destino e produto associado.
- Confirmar visualmente a correspondência entre produto e foto antes de publicar; não inferir produto apenas pelo nome quando o arquivo for ambíguo.

## Mapeamento inicial

| Produto | Arquivo editado esperado | Uso |
|---|---|---|
| Brigadeiro | `brigadeiro-editado.png` | card, galeria e seleção |
| Camafeu de morango | `camafeu-morango-editada.png` | card, galeria e seleção |
| Camafeu de uva | `camafeu-uva-editada.png` | card, galeria e seleção |
| Camafeu de nozes | `camafeu-nozes.png` | card, galeria e seleção |
| Pão de mel | `pao-de-mel-editado.png` | carrossel e card |
| Torta Holandesa | `torta-holandesa-editada.png` | carrossel/galeria e card |
| Cookies recheados | `cookies-editada.png` | card, se a foto representar o item |
| Bolos e tortas adicionais | manter somente se confirmados no cardápio | galeria, sem promover automaticamente a produto |

O arquivo exato e a associação final devem ser registrados em `manifesto-produtos-editados.json`. Fotos anteriores permanecem no projeto apenas se não forem substituídas nesta rodada; as referências ativas devem apontar para os novos arquivos.

## Tutorial de pedido

Trocar o iframe/URL do YouTube por um player HTML5 genérico:

```html
<video controls playsinline preload="metadata" poster="...">
  <source src="/caminho/configuravel/video-pedido.mp4" type="video/mp4">
</video>
```

A fonte deve ficar em um único atributo/configuração documentado, com estado “vídeo em breve” quando o arquivo ainda não existir. Não usar thumbnail do YouTube, autoplay com som, scraping ou player externo. Poster, legenda/transcrição e nome do arquivo serão preenchidos quando o vídeo próprio for entregue.

## Auditoria de segurança — Sol

Verificar:

- chaves, tokens, e-mails, telefones e dados pessoais expostos em HTML, JS, JSON, logs e metadados;
- links externos com `https`, `target="_blank"` e `rel="noopener noreferrer"`;
- iframes, origens permitidas, permissões e ausência de conteúdo remoto desnecessário;
- formulários: validação, escape, consentimento e ausência de envio automático inesperado;
- WhatsApp: texto codificado, número correto e nenhum dado sensível persistido sem necessidade;
- CSP, cabeçalhos, `.htaccess`, robots e arquivos de backup/zip expostos;
- imagens e vídeos: caminhos existentes, tipos permitidos, tamanhos e ausência de upload público;
- páginas de privacidade/reembolso: placeholders, dados desatualizados e afirmações que precisam de confirmação jurídica.

## Critérios de aceite

- Nenhum arquivo original de Downloads foi alterado.
- Apenas fotos editadas de produtos estão no novo destino.
- Cada produto ativo aponta para uma foto coerente ou fica sem foto, nunca com imagem de outro produto.
- O tutorial não contém `youtube.com`, `youtube-nocookie.com` ou link de canal.
- O player genérico não carrega mídia inexistente nem inicia sozinho.
- Auditoria não encontra segredo ou dado pessoal indevido no bundle público.
- `node --check`, `git diff --check`, validação local e Playwright passam em desktop e mobile.
