# Reformulação visual — setembro de 2026

Referência solicitada: https://www.youtube.com/watch?v=39IlNR-P3-Q

Foi consultada a descrição pública do vídeo, que apresenta um fluxo com Design
DNA, Frontend Design, Taste Skill e Scrollcraft, inspirado no site pear.no.
Não houve análise quadro a quadro nem instalação dessas skills. A adaptação
usa composição editorial e uma experiência de rolagem própria para a doceria.

## Direção visual

- Creme, chocolate e vinho; títulos em Playfair Display e texto em DM Sans.
- Abertura assimétrica, fotografia real do bombom em arco e selo artesanal.
- Nove doces organizados em uma vitrine com filtros de ocasião e ingredientes.
- História em quatro capítulos com retrato fixo durante a rolagem no desktop.
- Movimento discreto da fotografia, entradas progressivas e indicador de leitura.
- Mesma identidade no cardápio, galeria, formulário, rodapé e políticas.
- Conteúdo disponível sem JavaScript e respeito à preferência por menos movimento.

Os produtos, fotos, contatos e políticas vêm do projeto existente. Foram retirados
os espaços vazios de depoimentos; não foram criadas avaliações ou preços.
O formulário prepara o pedido para o WhatsApp e não envia mensagens sozinho.

## Prévia local

Na raiz do projeto: `python tools/serve-local.py`.

Abra http://127.0.0.1:8000/ e atualize a página após salvar alterações.
O servidor escuta somente em 127.0.0.1. Esta entrega não publica na Hostinger.

Estilos ativos: `Client/Public/Src/Styles/editorial.css`.
Interações: `Client/Public/Src/Js/script.js`.

As pastas `preview-dolce` e `index` não foram modificadas.

## Verificação

Conferido no Microsoft Edge: larguras de 320, 390, 768, 1024 e 1440 pixels;
filtros; galeria e carregamento de mais fotos; foco por teclado no menu móvel;
validação do formulário e URL do WhatsApp interceptada, sem envio; todas as
páginas internas no celular e desktop; preferência por menos movimento e
conteúdo sem JavaScript. Sem erros JavaScript ou referências locais ausentes.
As fotografias da página inicial carregaram e foram conferidas no navegador.

Para repetir: `python tools/check-redesign.py` (requer Playwright, BeautifulSoup
e Microsoft Edge instalados, além do servidor local em execução).
