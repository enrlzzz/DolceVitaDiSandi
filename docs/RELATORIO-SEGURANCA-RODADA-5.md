# Relatório de segurança — rodada 5

Data: 20/09/2026

## Escopo validado

- HTML, CSS e JavaScript públicos.
- Links externos e abertura de novas abas.
- Player local do tutorial.
- Assets copiados da pasta Downloads.
- Formulário de depoimento enviado ao WhatsApp.
- Responsividade, console e fluxos principais via Playwright.

## Resultado

Nenhum segredo, token de API, chave privada ou credencial foi encontrado nos arquivos públicos do aplicativo. O telefone, e-mail e links sociais encontrados são dados de contato intencionalmente publicados pela marca, não credenciais.

Os links externos usados com `target="_blank"` incluem `rel="noopener"` nas páginas principais. O player da seção “Como pedir” usa apenas um arquivo local MP4; não há iframe, embed ou dependência do YouTube nesse tutorial.

## Achados e recomendações

| Severidade | Achado | Situação | Correção/recomendação |
| --- | --- | --- | --- |
| Baixa | `video-doceria.mp4` tem aproximadamente 24 MB | Funcional, mas pode pesar no primeiro carregamento | Gerar uma versão web otimizada, poster leve e carregar sob interação quando o tráfego crescer |
| Baixa | A thumbnail do último vídeo usa `i.ytimg.com` | Dependência externa pública, sem segredo | Manter por enquanto ou copiar uma thumbnail otimizada para os assets quando a identidade visual exigir controle total |
| Média futura | Avaliações do Google não são puxadas automaticamente | A seção aponta para a fonte oficial e evita scraping | Para sincronizar avaliações, usar Google Business Profile/Places com Place ID e backend seguro; nunca expor a chave no JavaScript |
| Média futura | Formulário de depoimento abre WhatsApp | Não grava dados no servidor e exige consentimento visual | Se virar banco de depoimentos, adicionar backend HTTPS, autenticação administrativa, consentimento registrado e rotina de exclusão |

## Validações executadas

- `node --check Client/Public/Src/Js/script.js`: aprovado.
- `python tools/validate-kapitana.py`: aprovado, sem findings.
- Playwright rodada 5: aprovado.
- Testado player HTML5 local, thumbnail do vídeo mais recente, contagem de produtos, console sem erros e viewport de 320 px sem overflow.
- `git diff --check`: sem erro de whitespace.

## Pendências seguras

1. Confirmar se `video-doceria.mp4` é o vídeo final da simulação ou substituir o arquivo pelo vídeo definitivo mantendo o mesmo caminho.
2. Criar poster do vídeo para evitar o carregamento imediato de um arquivo grande.
3. Se a integração automática de avaliações for desejada, obter o Place ID da ficha oficial e implementar a consulta exclusivamente em backend.
