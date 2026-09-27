/* =========================================================================
   Dolce Vita Di Sandi — interações do site
   Sem bibliotecas externas. Tudo é progressivo: se este arquivo não carregar,
   o site continua legível, navegável e vendável.
   ========================================================================= */
(function () {
    'use strict';

    var WHATSAPP = '5515991291842';

    /* ---------------------------------------------------------------------
       0. Perfil do aparelho — decide o quanto de movimento é seguro exibir
       --------------------------------------------------------------------- */
    var menosMovimento = window.matchMedia('(prefers-reduced-motion: reduce)');

    function aparelhoFraco() {
        var nav = window.navigator;
        var conexao = nav.connection || nav.mozConnection || nav.webkitConnection;
        if (conexao) {
            if (conexao.saveData) return true;
            if (/(^|-)2g$/.test(conexao.effectiveType || '')) return true;
        }
        if (typeof nav.deviceMemory === 'number' && nav.deviceMemory <= 2) return true;
        if (typeof nav.hardwareConcurrency === 'number' && nav.hardwareConcurrency <= 2) return true;
        return false;
    }

    var economia = aparelhoFraco();
    if (economia) document.body.classList.add('economia');

    function podeAnimar() {
        return !menosMovimento.matches && !economia;
    }

    /* ---------------------------------------------------------------------
       1. Menu mobile
       --------------------------------------------------------------------- */
    var abrir = document.querySelector('#menu-open-button');
    var fechar = document.querySelector('#menu-close-button');
    var navMenu = document.querySelector('#nav-menu');

    function alternarMenu(mostrar) {
        document.body.classList.toggle('show-mobile-menu', mostrar);
        if (abrir) abrir.setAttribute('aria-expanded', String(mostrar));
        if (mostrar && fechar) fechar.focus();
        else if (!mostrar && abrir) abrir.focus();
    }

    if (abrir) abrir.addEventListener('click', function () { alternarMenu(true); });
    if (fechar) fechar.addEventListener('click', function () { alternarMenu(false); });

    if (navMenu) {
        navMenu.addEventListener('click', function (e) {
            if (e.target.closest('.nav-link, .nav-cta a')) alternarMenu(false);
        });
        // ESC fecha o menu, e o foco não escapa dele enquanto está aberto
        document.addEventListener('keydown', function (e) {
            if (e.key !== 'Escape') return;
            if (document.body.classList.contains('show-mobile-menu')) alternarMenu(false);
        });
    }

    /* ---------------------------------------------------------------------
       2. Header que some ao descer e volta ao subir
       --------------------------------------------------------------------- */
    var header = document.querySelector('header');
    var ultimoY = window.scrollY;
    var travado = false;

    function aoRolar() {
        var y = window.scrollY;
        if (!header) return;
        header.classList.toggle('solido', y > 40);
        if (y < 120 || document.body.classList.contains('show-mobile-menu')) {
            header.classList.remove('escondido');
        } else if (y > ultimoY + 6) {
            header.classList.add('escondido');
        } else if (y < ultimoY - 6) {
            header.classList.remove('escondido');
        }
        ultimoY = y;
        travado = false;
    }

    window.addEventListener('scroll', function () {
        if (travado) return;
        travado = true;
        window.requestAnimationFrame(aoRolar);
    }, { passive: true });

    /* ---------------------------------------------------------------------
       3. Link ativo na navegação conforme a seção visível
       --------------------------------------------------------------------- */
    var secoes = document.querySelectorAll('main section[id]');
    var links = document.querySelectorAll('.nav-link[href^="#"]');

    if ('IntersectionObserver' in window && secoes.length) {
        var observadorNav = new IntersectionObserver(function (entradas) {
            entradas.forEach(function (entrada) {
                if (!entrada.isIntersecting) return;
                var id = entrada.target.id;
                links.forEach(function (link) {
                    var ativo = link.getAttribute('href') === '#' + id;
                    if (ativo) link.setAttribute('aria-current', 'true');
                    else link.removeAttribute('aria-current');
                });
            });
        }, { rootMargin: '-45% 0px -50% 0px' });
        secoes.forEach(function (s) { observadorNav.observe(s); });
    }

    /* ---------------------------------------------------------------------
       4. Revelar elementos ao entrar na tela (substitui GSAP/ScrollTrigger)
       --------------------------------------------------------------------- */
    var reveláveis = document.querySelectorAll('.revelar');

    function revelarTudo() {
        reveláveis.forEach(function (el) { el.classList.add('visivel'); });
    }

    if (!podeAnimar() || !('IntersectionObserver' in window)) {
        revelarTudo();
    } else {
        // Só a partir daqui é seguro esconder: o observador existe e vai revelar.
        document.documentElement.classList.add('com-reveal');
        // Rede de segurança: se em 4s algo tiver ficado para trás, mostra tudo.
        window.setTimeout(revelarTudo, 4000);
        var observador = new IntersectionObserver(function (entradas, obs) {
            entradas.forEach(function (entrada, i) {
                if (!entrada.isIntersecting) return;
                var el = entrada.target;
                el.style.transitionDelay = Math.min(i * 70, 280) + 'ms';
                el.classList.add('visivel');
                obs.unobserve(el);
            });
        }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });
        reveláveis.forEach(function (el) { observador.observe(el); });
    }

    /* ---------------------------------------------------------------------
       5. Cena 3D do herói — inclinação por mouse/giroscópio + saída no scroll
       Custo: zero biblioteca. Só atualiza duas variáveis CSS por quadro.
       --------------------------------------------------------------------- */
    // A cena do herói é deliberadamente estática: nada de inclinação pelo
    // mouse nem de balanço. O que dá profundidade é a luz e a sombra, não o
    // movimento. Mantemos apenas a saída suave no scroll.
    // Transição de saída: o herói se afasta e entrega a cena para "Sobre"
    var heroSection = document.querySelector('.hero-section');
    var cena = document.querySelector('#hero-cena');
    if (heroSection && cena && podeAnimar()) {
        var travadoHero = false;
        window.addEventListener('scroll', function () {
            if (travadoHero) return;
            travadoHero = true;
            window.requestAnimationFrame(function () {
                var altura = heroSection.offsetHeight || 1;
                var p = Math.min(1, Math.max(0, window.scrollY / altura));
                cena.style.opacity = String(1 - p * 0.9);
                cena.style.setProperty('--saida', p.toFixed(3));
                cena.style.translate = '0 ' + (p * -60).toFixed(1) + 'px';
                cena.style.scale = String(1 - p * 0.12);
                travadoHero = false;
            });
        }, { passive: true });
    }

    /* ---------------------------------------------------------------------
       6. Lightbox da galeria — teclado, ESC e setas
       --------------------------------------------------------------------- */
    var lightbox = document.querySelector('#lightbox');
    var lbImg = document.querySelector('#lightbox-img');
    var lbLegenda = document.querySelector('#lightbox-legenda');
    var botoesGaleria = Array.prototype.slice.call(
        document.querySelectorAll('.gallery-item:not(.oculto) .gallery-botao'));
    var indiceAtual = 0;
    var origemFoco = null;

    function fonteDe(botao) {
        var img = botao.querySelector('img');
        // data-grande aponta para a versão de visualização (1100px).
        // Sem ela, cai para a miniatura que o navegador já baixou.
        var grande = botao.getAttribute('data-grande');
        if (!img) return { src: grande || '', alt: '' };
        return {
            src: grande || img.currentSrc || img.src,
            alt: img.alt || ''
        };
    }

    function mostrar(indice) {
        if (!botoesGaleria.length) return;
        indiceAtual = (indice + botoesGaleria.length) % botoesGaleria.length;
        var botao = botoesGaleria[indiceAtual];
        var dados = fonteDe(botao);
        lbImg.src = dados.src;
        lbImg.alt = dados.alt;
        var legenda = botao.getAttribute('data-legenda');
        if (!legenda) {
            legenda = 'Foto ' + (indiceAtual + 1) + ' de ' + botoesGaleria.length
                + ' — ' + dados.alt;
        }
        lbLegenda.textContent = legenda;
    }

    function abrirLightbox(indice) {
        if (!lightbox || !lightbox.showModal) return false;
        origemFoco = document.activeElement;
        mostrar(indice);
        lightbox.showModal();
        document.body.style.overflow = 'hidden';
        return true;
    }

    // Restaura a página. Não depende do evento 'close' do <dialog>: em alguns
    // navegadores ele não dispara, e a página ficaria travada sem rolagem.
    function restaurarPagina() {
        document.body.style.overflow = '';
        if (lbImg) lbImg.src = '';
        if (origemFoco && origemFoco.focus) origemFoco.focus();
        origemFoco = null;
    }

    function fecharLightbox() {
        if (!lightbox) return;
        if (lightbox.open) lightbox.close();
        restaurarPagina();
    }

    if (lightbox) {
        lightbox.addEventListener('close', restaurarPagina);

        // Clique fora da imagem fecha
        lightbox.addEventListener('click', function (e) {
            if (e.target === lightbox || e.target.tagName === 'DIV') fecharLightbox();
        });

        document.querySelector('#lightbox-fechar').addEventListener('click', fecharLightbox);
        document.querySelector('#lightbox-anterior').addEventListener('click', function () {
            mostrar(indiceAtual - 1);
        });
        document.querySelector('#lightbox-proximo').addEventListener('click', function () {
            mostrar(indiceAtual + 1);
        });

        lightbox.addEventListener('keydown', function (e) {
            if (e.key === 'ArrowLeft') { e.preventDefault(); mostrar(indiceAtual - 1); }
            if (e.key === 'ArrowRight') { e.preventDefault(); mostrar(indiceAtual + 1); }
            // Fechamos o ESC na mão para garantir que a rolagem volte
            if (e.key === 'Escape') { e.preventDefault(); fecharLightbox(); }
        });
    }

    function ligarBotoesGaleria() {
        botoesGaleria.forEach(function (botao, i) {
            if (botao.dataset.ligado) return;
            botao.dataset.ligado = '1';
            botao.addEventListener('click', function () {
                indiceAtual = Array.prototype.indexOf.call(botoesGaleria, botao);
                abrirLightbox(indiceAtual < 0 ? i : indiceAtual);
            });
        });
    }

    ligarBotoesGaleria();

    /* ---------------------------------------------------------------------
       6b. "Carregar mais" da página com todas as fotos
       Os itens já vêm no HTML (bom para busca); só ficam ocultos até o
       visitante pedir, para a primeira pintura ser leve.
       --------------------------------------------------------------------- */
    var botaoMais = document.querySelector('#carregar-mais');

    if (botaoMais) {
        var LOTE = 48;
        var contador = document.querySelector('#galeria-mostrando');
        var area = document.querySelector('#carregar-mais-area');

        botaoMais.addEventListener('click', function () {
            var ocultos = document.querySelectorAll('.gallery-item.oculto');
            var quantos = Math.min(LOTE, ocultos.length);
            for (var i = 0; i < quantos; i++) {
                ocultos[i].classList.remove('oculto');
            }
            var visiveis = document.querySelectorAll('.gallery-item:not(.oculto)').length;
            if (contador) contador.textContent = String(visiveis);

            // A lista do lightbox precisa acompanhar o que está na tela
            botoesGaleria = Array.prototype.slice.call(
                document.querySelectorAll('.gallery-item:not(.oculto) .gallery-botao'));
            ligarBotoesGaleria();

            if (!document.querySelector('.gallery-item.oculto') && area) {
                area.hidden = true;
            }
        });
    }

    /* ---------------------------------------------------------------------
       7. Formulário de pedido -> mensagem pronta no WhatsApp
       Validação no cliente + honeypot. Não há backend: nada trafega para
       servidor nenhum, os dados vão direto para a conversa do WhatsApp.
       --------------------------------------------------------------------- */
    var form = document.querySelector('#form-pedido');

    function erro(campo, texto) {
        var alvo = document.querySelector('#erro-' + campo);
        var entrada = document.querySelector('#' + campo);
        if (alvo) alvo.textContent = texto || '';
        if (entrada) {
            if (texto) entrada.setAttribute('aria-invalid', 'true');
            else entrada.removeAttribute('aria-invalid');
        }
        return !texto;
    }

    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            var status = document.querySelector('#form-status');
            var mel = form.querySelector('#empresa');

            // Robô preencheu o campo escondido: descarta em silêncio.
            if (mel && mel.value.trim() !== '') {
                status.textContent = 'Não foi possível enviar. Tente pelo WhatsApp.';
                return;
            }

            var nome = form.querySelector('#nome').value.trim();
            var item = form.querySelector('#item').value;
            var quando = form.querySelector('#quando').value;
            var mensagem = form.querySelector('#mensagem').value.trim();

            var ok = true;
            ok = erro('nome', nome.length < 2 ? 'Escreva seu nome, por favor.' : '') && ok;
            ok = erro('item', !item ? 'Escolha o que você quer pedir.' : '') && ok;
            ok = erro('mensagem', mensagem.length > 800
                ? 'Mensagem muito longa — resuma em até 800 caracteres.' : '') && ok;

            if (quando) {
                var hoje = new Date();
                hoje.setHours(0, 0, 0, 0);
                var escolhida = new Date(quando + 'T00:00:00');
                ok = erro('quando', escolhida < hoje
                    ? 'Escolha uma data de hoje em diante.' : '') && ok;
            } else {
                erro('quando', '');
            }

            if (!ok) {
                status.textContent = 'Confira os campos destacados acima.';
                var primeiro = form.querySelector('[aria-invalid="true"]');
                if (primeiro) primeiro.focus();
                return;
            }

            var linhas = [
                'Olá, Sanderly! Vim pelo site 💗',
                '',
                'Nome: ' + nome,
                'Pedido: ' + item
            ];
            if (quando) {
                var partes = quando.split('-');
                linhas.push('Para: ' + partes[2] + '/' + partes[1] + '/' + partes[0]);
            }
            if (mensagem) linhas.push('Detalhes: ' + mensagem);

            var url = 'https://wa.me/' + WHATSAPP + '?text=' +
                encodeURIComponent(linhas.join('\n'));

            status.textContent = 'Abrindo o WhatsApp com o seu pedido pronto…';
            window.open(url, '_blank', 'noopener');
        });

        // Limpa o erro assim que a pessoa corrige o campo
        form.addEventListener('input', function (e) {
            if (e.target.id) erro(e.target.id, '');
        });
    }
})();
