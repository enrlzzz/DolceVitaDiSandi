/* Shared, progressively enhanced interactions. */
(() => {
  'use strict';
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href*="#"]');
    if (!link || event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const url = new URL(link.href, window.location.href);
    if (url.origin !== window.location.origin || url.pathname !== window.location.pathname || !url.hash) return;
    let target;
    try { target = document.querySelector(url.hash); } catch { return; }
    if (!target) return;
    event.preventDefault();
    target.scrollIntoView({ behavior: prefersReducedMotion.matches ? 'auto' : 'smooth', block: 'start' });
    history.pushState(null, '', url.hash);
  });

  // Internal gallery: lightbox includes newly revealed photos and never runs homepage code.
  const lightbox = $('#lightbox');
  if (lightbox) {
    let current = 0, origin = null;
    const buttons = () => $$('.gallery-item:not(.oculto) .gallery-botao');
    const show = index => { const all = buttons(); if (!all.length) return; current = (index + all.length) % all.length; const button = all[current], image = $('img', button); $('#lightbox-img').src = button.dataset.grande || image?.currentSrc || image?.src || ''; $('#lightbox-img').alt = image?.alt || ''; $('#lightbox-legenda').textContent = button.dataset.legenda || `Foto ${current + 1} de ${all.length}`; };
    const close = () => { if (lightbox.open) lightbox.close(); document.body.style.overflow = ''; origin?.focus(); };
    $$('.gallery-botao').forEach(button => button.addEventListener('click', () => { origin = document.activeElement; show(buttons().indexOf(button)); lightbox.showModal(); document.body.style.overflow = 'hidden'; }));
    $('#lightbox-fechar')?.addEventListener('click', close);
    $('#lightbox-anterior')?.addEventListener('click', () => show(current - 1));
    $('#lightbox-proximo')?.addEventListener('click', () => show(current + 1));
    lightbox.addEventListener('click', event => { if (event.target === lightbox) close(); });
    lightbox.addEventListener('close', () => { document.body.style.overflow = ''; });
    document.addEventListener('keydown', event => { if (!lightbox.open) return; if (event.key === 'Escape') close(); if (event.key === 'ArrowLeft') show(current - 1); if (event.key === 'ArrowRight') show(current + 1); });
  }
  $('#carregar-mais')?.addEventListener('click', () => { const hidden = $$('.gallery-item.oculto'); hidden.slice(0, 48).forEach(item => item.classList.remove('oculto')); const count = $('#galeria-mostrando'); if (count) count.textContent = String($$('.gallery-item:not(.oculto)').length); if (hidden.length <= 48) $('#carregar-mais-area')?.setAttribute('hidden', ''); });

  if (!$('.kapitana-home')) return;
  const menu = '/Client/Public/Src/Assets/otimizadas/menu/';
  const rodada2 = '/Client/Public/Src/Assets/rodada-2/';
  const rodada5 = '/Client/Public/Src/Assets/rodada-5/produtos-editados/';
  const products = [
    ['doces','Torta Holandesa','Camadas de creme, biscoito e chocolate.','torta-holandesa-editada.png', rodada5],
    ['doces','Pão de mel','Massa macia e cobertura de chocolate.','pao-de-mel-editado.png', rodada5],
    ['doces','Bombom Ferrero Rocher','Bombom crocante inspirado no clássico italiano, finalizado à mão.','camafeu-nozes.png', rodada5],
    ['cookies','Cookies recheados','Cookies recheados da casa para acompanhar a sua pausa.','cookies-editada.png', rodada5],
    ['doces','Brigadeiro','Doce artesanal da casa.','brigadeiro-editado.png', rodada5],
    ['doces','Camafeu de morango','Chocolate, creme e morango.','camafeu-morango-editada.png', rodada5],
    ['doces','Camafeu de uva','Camafeu artesanal com uva.','camafeu-uva-editada.png', rodada5],
    ['doces','Bolo de fubá','Bolo caseiro com goiabada.','bolo-de-fuba-editado.png', rodada5],
    ['doces','Bolo fit','Uma opção especial da cozinha.','bolo-fit-editado.png', rodada5],
    ['doces','Bolo vulcão','Bolo generoso com cobertura cremosa.','bolo-vulcao-editado-2.png', rodada5],
    ['doces','Torta de morango','Torta artesanal com morangos.','torta-de-morango-editada.png', rodada5],
    ['doces','Paçoca','Doce de paçoca feito na cozinha.','pacoca-editada.png', rodada5]
  ].map(([category, name, description, image, base], id) => ({ id, category, name, description, image: base + image }));
  let filter = 'todos', selected = [];
  try { selected = [...new Set(JSON.parse(localStorage.getItem('dolce-vita-selection') || '[]').filter(id => Number.isInteger(id) && products[id]))]; } catch { selected = []; }
  const render = () => {
    const visible = products.filter(p => filter === 'todos' || p.category === filter);
    $('#products').innerHTML = visible.map(p => `<article class="product"><img src="${p.image}" alt="${p.name} da Dolce Vita Di Sandi" width="800" height="800" loading="lazy"><div><h3>${p.name}</h3><p>${p.description}</p></div><button type="button" data-product="${p.id}" aria-label="Ver ${p.name}">+</button></article>`).join('');
    $('#filter-status').textContent = `${visible.length} doces encontrados.`;
  };
  render();
  $$('.filters button').forEach(button => button.addEventListener('click', () => { filter = button.dataset.filter; $$('.filters button').forEach(item => item.setAttribute('aria-pressed', String(item === button))); render(); }));
  const productDialog = $('#product-dialog');
  $('#products').addEventListener('click', event => { const id = event.target.dataset.product; if (id === undefined) return; const p = products[Number(id)]; $('#dialog-body').innerHTML = `<img class="product-dialog-image" src="${p.image}" alt="${p.name}"><span class="eyebrow">SOB ENCOMENDA</span><h3 class="dialog-product-title" id="product-dialog-title">${p.name}</h3><p>${p.description}</p><button class="pill pink" data-add="${p.id}" type="button">Adicionar à seleção</button>`; productDialog.setAttribute('aria-labelledby', 'product-dialog-title'); productDialog.showModal(); });
  const updateCount = () => { $('#selection-count').textContent = selected.length; try { localStorage.setItem('dolce-vita-selection', JSON.stringify(selected)); } catch {} };
  const renderSelection = () => { const list = selected.map(id => products[id]); $('#selection-list').innerHTML = list.length ? list.map(p => `<div class="selection-row"><span>${p.name}</span><button data-remove="${p.id}">remover</button></div>`).join('') : '<p>Nenhum doce selecionado ainda.</p>'; $('#selection-whatsapp').href = `https://wa.me/5515991291842?text=${encodeURIComponent(list.length ? `Olá! Vi o site e queria conversar sobre: ${list.map(p => p.name).join(', ')}.` : 'Olá! Vi o site e queria conhecer os doces disponíveis.')}`; };
  document.addEventListener('click', event => { if (event.target.matches('[data-close]')) event.target.closest('dialog')?.close(); if (event.target.matches('[data-add]')) { const id = Number(event.target.dataset.add); if (!selected.includes(id)) selected.push(id); updateCount(); productDialog.close(); } if (event.target.matches('[data-remove]')) { selected = selected.filter(id => id !== Number(event.target.dataset.remove)); updateCount(); renderSelection(); } });
  $('#selection-button').addEventListener('click', () => { renderSelection(); $('#selection-dialog').showModal(); });
  const scenes = [
    { src: rodada5 + 'pao-de-mel-editado.png', caption: 'O carinho está nos detalhes.', alt: 'Pão de mel recheado com chocolate e doce de leite feito pela Sanderly.' },
    { src: rodada5 + 'torta-holandesa-editada.png', caption: 'Uma receita para compartilhar.', alt: 'Torta Holandesa feita artesanalmente pela Sanderly.' },
    { src: rodada5 + 'camafeu-nozes.png', caption: 'Pequenos detalhes, feitos à mão.', alt: 'Bombom Ferrero Rocher finalizado à mão pela Dolce Vita Di Sandi.' }
  ];
  let sceneIndex = 0;
  let carouselTimer;
  const carousel = $('.hero-carousel');
  const stopCarousel = () => { window.clearInterval(carouselTimer); carouselTimer = undefined; };
  const restartCarousel = () => { stopCarousel(); if (!prefersReducedMotion.matches) carouselTimer = window.setInterval(() => setScene(sceneIndex + 1), 5600); };
  const setScene = (index, { pause = false } = {}) => {
    sceneIndex = (index + scenes.length) % scenes.length;
    const scene = scenes[sceneIndex];
    const image = $('#hero-scene');
    image.classList.add('is-changing');
    window.setTimeout(() => { image.src = scene.src; image.alt = scene.alt; image.classList.remove('is-changing'); }, 170);
    $('#scene-caption').textContent = scene.caption;
    $$('[data-scene]').forEach((button, buttonIndex) => button.setAttribute('aria-pressed', String(buttonIndex === sceneIndex)));
    if (pause) stopCarousel(); else restartCarousel();
  };
  $('#hero-scene').src = scenes[0].src;
  $$('[data-scene]').forEach((button, index) => button.addEventListener('click', () => setScene(index, { pause: true })));
  $('[data-carousel="prev"]')?.addEventListener('click', () => setScene(sceneIndex - 1, { pause: true }));
  $('[data-carousel="next"]')?.addEventListener('click', () => setScene(sceneIndex + 1, { pause: true }));
  carousel?.addEventListener('mouseenter', stopCarousel);
  carousel?.addEventListener('mouseleave', restartCarousel);
  carousel?.addEventListener('focusin', stopCarousel);
  carousel?.addEventListener('focusout', event => { if (!carousel.contains(event.relatedTarget)) restartCarousel(); });
  carousel?.addEventListener('touchstart', event => { carousel.dataset.touchStart = event.changedTouches[0].clientX; }, { passive: true });
  carousel?.addEventListener('touchend', event => { const start = Number(carousel.dataset.touchStart); const delta = event.changedTouches[0].clientX - start; if (Math.abs(delta) > 45) setScene(sceneIndex + (delta < 0 ? 1 : -1), { pause: true }); }, { passive: true });
  carousel?.addEventListener('keydown', event => { if (event.key === 'ArrowLeft') setScene(sceneIndex - 1, { pause: true }); if (event.key === 'ArrowRight') setScene(sceneIndex + 1, { pause: true }); });
  restartCarousel();
  const tutorial = $('.tutorial-video');
  if (tutorial) {
    const sourceUrl = (tutorial.dataset.videoSrc || '').trim();
    const posterUrl = (tutorial.dataset.videoPoster || '').trim();
    const isExternalEmbed = /^https?:\/\//i.test(sourceUrl);
    if (sourceUrl && !isExternalEmbed) {
      const video = document.createElement('video');
      video.controls = true;
      video.playsInline = true;
      video.preload = 'metadata';
      video.setAttribute('aria-label', 'Tutorial de como fazer um pedido no site');
      if (posterUrl && !/^https?:\/\//i.test(posterUrl)) video.poster = posterUrl;
      const source = document.createElement('source');
      source.src = sourceUrl;
      source.type = 'video/mp4';
      video.appendChild(source);
      tutorial.replaceChildren(video);
    }
  }
  const ingredients = [['Chocolate','A cobertura intensa que dá presença à primeira mordida.'],['Creme','A camada cremosa que deixa a Torta Holandesa macia e inesquecível.'],['Biscoito','A base crocante que equilibra o creme e completa a receita.']];
  const showIngredient = index => { const [title, text] = ingredients[index]; $('#ingredient-copy').innerHTML = `<h3>${title}</h3><p>${text}</p>`; $$('[data-ingredient]').forEach(button => button.setAttribute('aria-pressed', String(Number(button.dataset.ingredient) === index))); };
  $$('[data-ingredient]').forEach(button => button.addEventListener('click', () => showIngredient(Number(button.dataset.ingredient)))); showIngredient(0);
  const pair = { chocolate: 'Uma vontade intensa pede chocolate. Que tal conversar sobre os doces da casa?', crocante: 'Para uma mordida crocante, os cookies podem acompanhar muito bem a sua pausa.', cafe: 'Café passado e um doce escolhido com calma: uma combinação para ficar mais um pouco.' };
  const renderPair = () => $('#pair-result').textContent = pair[$('input[name="mood"]:checked').value]; $$('input[name="mood"]').forEach(input => input.addEventListener('change', renderPair)); renderPair();
  $$('.home-gallery button').forEach(button => button.addEventListener('click', () => { $('#home-lightbox-image').src = button.dataset.gallerySrc; $('#home-lightbox').showModal(); }));
  $$('[data-occasion]').forEach(button => button.addEventListener('click', () => {
    const occasion = button.dataset.occasion;
    const message = `Olá! Quero conversar sobre doces para ${occasion}. Gostaria de saber as opções, quantidades e disponibilidade.`;
    window.open(`https://wa.me/5515991291842?text=${encodeURIComponent(message)}`, '_blank', 'noopener');
  }));
  $('#testimonial-form')?.addEventListener('submit', event => {
    event.preventDefault();
    const form = event.currentTarget;
    const name = form.elements.name.value.trim();
    const review = form.elements.text.value.trim();
    const message = `Olá! Quero enviar um depoimento para a Dolce Vita Di Sandi.\n\nNome: ${name}\nDepoimento: “${review}”\n\nAutorizo a publicação deste depoimento no site.`;
    $('#testimonial-feedback').textContent = 'Abrindo o WhatsApp para você revisar a mensagem...';
    window.open(`https://wa.me/5515991291842?text=${encodeURIComponent(message)}`, '_blank', 'noopener');
  });
  $$('.lab-photo [data-ingredient]').forEach((button, index) => button.setAttribute('aria-label', ingredients[index][0]));
  $('#selection-dialog').setAttribute('aria-labelledby', 'selection-dialog-title');
  $('#selection-dialog h2').id = 'selection-dialog-title';
  $('#home-lightbox').setAttribute('aria-label', 'Foto ampliada dos nossos doces');
  $$('dialog').forEach(dialog => {
    dialog.addEventListener('click', event => {
      const box = dialog.getBoundingClientRect();
      if (event.target === dialog && (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom)) dialog.close();
    });
  });
  updateCount();
})();
