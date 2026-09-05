# 🚀 Deploy automático: GitHub → Hostinger

## Primeiro, três correções de rota

Antes do passo a passo, três coisas que mudam o plano que você tinha em mente:

**1. Você NÃO precisa excluir o site da Hostinger.**
Excluir o site apaga também a configuração do domínio, o certificado SSL e os
e-mails ligados a ele. Dá muito mais trabalho para recuperar do que para
resolver. O que precisa ficar vazio é só a pasta `public_html` — o site em si
continua existindo.

**2. NÃO use "Web Node app" / "Aplicativo Node.js".**
Esse recurso é para sites que rodam um servidor JavaScript (Express, Next.js,
Nuxt). O nosso site é HTML, CSS e JavaScript puro, servido como arquivo
estático — não tem `package.json`, não tem build, não tem processo rodando.
Colocar num app Node deixaria o site **mais lento e mais frágil**, sem nenhum
ganho. O caminho certo é hospedagem estática comum + o recurso **GIT** do
hPanel.

**3. O deploy da Hostinger clona o repositório inteiro dentro de `public_html`.**
É por isso que existe o arquivo `.htaccess` na raiz deste projeto: ele faz o
`dolcevitadisandi.com.br/` servir o `Client/Public/Src/Pages/index.html` sem
que o visitante veja esse caminho. Sem esse arquivo, o site abriria uma lista de
pastas.

---

## ⚠️ Antes de começar: salve o PDF do cardápio

O arquivo **`Cardápio Oficial DolceVitaDiSandi.pdf`** está hoje só no servidor,
**não está no repositório**. Quando o deploy via Git começar, o conteúdo de
`public_html` passa a ser um espelho do GitHub — e tudo que não estiver no
repositório **some**.

Faça agora, nesta ordem:

1. Abra <https://dolcevitadisandi.com.br/Cardápio%20Oficial%20DolceVitaDiSandi.pdf>
   e salve o arquivo no computador.
2. Copie o PDF para a **raiz deste projeto** (a mesma pasta onde está o
   `README.md`).
3. Rode:

   ```bash
   git add "Cardápio Oficial DolceVitaDiSandi.pdf"
   git commit -m "chore: versiona o PDF do cardapio no repositorio"
   git push
   ```

Enquanto isso não for feito, o link "Baixar cardápio em PDF" vai quebrar depois
do primeiro deploy.

**Faça o mesmo com qualquer outro arquivo que exista no servidor e não no
repositório** (fotos soltas, arquivos de verificação do Google, etc.). Antes de
esvaziar a pasta, baixe um backup completo:
hPanel → **Arquivos → Gerenciador de arquivos** → selecione tudo dentro de
`public_html` → **Compactar** → baixe o `.zip`.

---

## Passo a passo

### 1. Backup e limpeza do `public_html`

1. hPanel → **Arquivos → Gerenciador de arquivos**.
2. Entre em `public_html`.
3. Selecione tudo (inclusive arquivos ocultos como `.htaccess`) → **Compactar**
   → baixe o `.zip` para o computador. Esse é o seu plano B.
4. Agora apague **o conteúdo** de `public_html` — a pasta continua existindo,
   só fica vazia. O Git se recusa a clonar numa pasta que já tem arquivos.

> Não mexa em `Websites → Excluir site`. Isso é o que você **não** quer fazer.

### 2. Conectar o repositório

1. hPanel → **Websites** → clique em **Gerenciar** no `dolcevitadisandi.com.br`.
2. Menu lateral → **Avançado → GIT**.
3. Preencha:
   - **Repositório**: `https://github.com/enrlzzz/DolceVitaDiSandi.git`
   - **Branch**: `main`
   - **Diretório**: deixe **em branco** (significa a raiz do `public_html`).
4. Clique em **Criar**.

Se o repositório for **privado**, a Hostinger mostra uma **chave SSH pública**
nessa mesma tela. Copie ela e cole em:
GitHub → repositório → **Settings → Deploy keys → Add deploy key**
(marque só leitura, não precisa de permissão de escrita).
Nesse caso, use a URL SSH no campo repositório:
`git@github.com:enrlzzz/DolceVitaDiSandi.git`.

### 3. Primeiro deploy manual

Ainda na tela do GIT, o repositório aparece listado com um botão
**Implantar / Deploy**. Clique nele e aguarde. Depois abra
<https://dolcevitadisandi.com.br/> e confira se o site subiu.

### 4. Ligar o deploy automático a cada `git push`

1. Na tela do GIT, clique em **Auto Deployment** (ou "Implantação automática").
   A Hostinger gera uma **URL de webhook**. Copie ela.
2. GitHub → repositório → **Settings → Webhooks → Add webhook**:
   - **Payload URL**: cole a URL da Hostinger
   - **Content type**: `application/json`
   - **Secret**: deixe vazio (a Hostinger não usa)
   - **Which events**: `Just the push event`
   - Deixe **Active** marcado → **Add webhook**
3. Faça um `git push` qualquer e volte na tela do webhook no GitHub. Em
   **Recent Deliveries** deve aparecer uma entrega com ✅ e resposta `200`.

Pronto: a partir daí, todo `git push` na `main` atualiza o site sozinho em
alguns segundos.

---

## Conferência final (5 minutos)

Depois do primeiro deploy, abra e teste:

- [ ] `https://dolcevitadisandi.com.br/` — a home abre direto, sem lista de pastas
- [ ] O cadeado de HTTPS aparece e `http://` redireciona para `https://`
- [ ] `https://dolcevitadisandi.com.br/cardapio` — URL limpa funciona
- [ ] Link "Baixar cardápio em PDF" abre o PDF (só depois de versionar o PDF)
- [ ] Rodapé → as duas políticas abrem
- [ ] Botão do WhatsApp abre a conversa com a mensagem pronta
- [ ] Abra no celular e confira o menu hambúrguer
- [ ] `https://dolcevitadisandi.com.br/robots.txt` e `/sitemap.xml` respondem

---

## Depois que estiver no ar

1. **Google Search Console** — <https://search.google.com/search-console>:
   adicione a propriedade do domínio, valide (a Hostinger permite validar por
   registro DNS TXT) e envie o `sitemap.xml`. É o que faz o Google indexar as
   páginas novas.
2. **Perfil da Empresa no Google** — <https://business.google.com>: cadastre a
   Dolce Vita Di Sandi como doceria em Sorocaba, com o mesmo telefone e nome que
   estão no site. É a ação de maior retorno para busca local.
3. **HSTS**: depois de uma semana com HTTPS estável, descomente a linha
   `Strict-Transport-Security` no `.htaccess`.

---

## Se der problema

| Sintoma | Causa provável | Solução |
| --- | --- | --- |
| Abre uma lista de pastas | `.htaccess` não subiu ou `mod_rewrite` desligado | Confirme que o `.htaccess` está na raiz do `public_html`; abra chamado na Hostinger pedindo `mod_rewrite` |
| Erro 500 | Alguma diretiva do `.htaccess` não é suportada no plano | Comente o bloco `<IfModule mod_headers.c>` e teste de novo |
| Git recusa clonar | `public_html` não está vazia | Apague o conteúdo restante, inclusive arquivos ocultos |
| `push` não atualiza o site | Webhook não configurado ou falhando | GitHub → Settings → Webhooks → Recent Deliveries: veja o erro e reenvie |
| CSS não carrega | Deploy incompleto | Rode o deploy manual de novo pela tela do GIT |
| Imagens antigas aparecendo | Cache do navegador | `Ctrl + Shift + R` |
