import json
import sys
from pathlib import Path
from urllib.parse import urlparse, unquote
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parent.parent
if '--capture' in sys.argv:
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge')
        page = browser.new_page(viewport={'width':1440,'height':1000})
        page.goto('http://127.0.0.1:8000',wait_until='networkidle')
        page.evaluate('document.querySelectorAll("img").forEach(img => img.loading = "eager")')
        page.wait_for_function('Array.from(document.images).filter(i => i.hasAttribute("src")).every(i => i.complete && i.naturalWidth > 0)')
        page.wait_for_timeout(4500)
        for selector, filename in [('#Menu','menu-review'),('#Historia','story-review')]:
            page.evaluate('(selector) => window.scrollTo({top:document.querySelector(selector).offsetTop-98,behavior:"instant"})',selector)
            page.wait_for_timeout(800)
            page.screenshot(path=str(root / ('tools/'+filename+'.tmp.png')))
        page.screenshot(path=str(root / 'tools/full.tmp.png'),full_page=True)
        print('All storefront photographs loaded successfully.')
        browser.close()
    sys.exit(0)
missing = []
for path in (root / 'Client/Public/Src/Pages').glob('*.html'):
    soup = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
    for el in soup.select('[src], [href]'):
        value = el.get('src', el.get('href', ''))
        if value.startswith('/') and not (root / unquote(urlparse(value).path).lstrip('/')).exists():
            missing.append((path.name, value))
assert not missing, missing

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge')
    page = browser.new_page(viewport={'width':1440, 'height':1000}, device_scale_factor=1)
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto('http://127.0.0.1:8000', wait_until='networkidle')
    page.wait_for_timeout(4500)
    page.screenshot(path=str(root / 'tools/desktop.tmp.png'))
    page.screenshot(path=str(root / 'tools/full.tmp.png'), full_page=True)
    for name, count in [('classicos',4), ('chocolate',6), ('celebrar',5), ('todos',9)]:
        page.locator(f'[data-filter="{name}"]').click()
        assert page.locator('.menu-item:visible').count() == count, name
    page.locator('.gallery-botao').first.click()
    assert page.locator('#lightbox').is_visible()
    old = page.locator('#lightbox-img').get_attribute('src')
    page.keyboard.press('ArrowRight')
    assert old != page.locator('#lightbox-img').get_attribute('src')
    page.keyboard.press('Escape')
    assert not page.locator('#lightbox').is_visible()
    page.locator('.submit-button').click()
    assert page.locator('#nome').get_attribute('aria-invalid') == 'true'
    page.locator('#nome').fill('Teste de visual')
    page.locator('#item').select_option(label='Bombom de morango')
    page.evaluate('window.open = (url) => { window.testOrderUrl = url; return null; }')
    page.locator('.submit-button').click()
    assert 'wa.me/5515991291842' in page.evaluate('window.testOrderUrl')
    assert 'Bombom%20de%20morango' in page.evaluate('window.testOrderUrl')
    for width in [320,390,768,1024,1440]:
        page.set_viewport_size({'width':width,'height':900})
        page.goto('http://127.0.0.1:8000',wait_until='networkidle')
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'Overflow {width}'
        if width == 390:
            page.screenshot(path=str(root / 'tools/mobile.tmp.png'),full_page=True)
            page.locator('#menu-open-button').click()
            page.wait_for_timeout(350)
            assert page.locator('#menu-open-button').get_attribute('aria-expanded') == 'true'
            assert page.evaluate('document.activeElement.id') == 'menu-close-button'
            page.keyboard.press('Shift+Tab')
            assert page.evaluate('document.activeElement.closest(".nav-cta") !== null')
            page.keyboard.press('Escape')
            assert page.locator('#menu-open-button').get_attribute('aria-expanded') == 'false'
    for name in ['cardapio','galeria','politica-de-privacidade','politica-de-reembolso']:
        for width in [390,1440]:
            page.set_viewport_size({'width':width,'height':900})
            page.goto('http://127.0.0.1:8000/Client/Public/Src/Pages/'+name+'.html', wait_until='networkidle')
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'{name} overflow {width}'
        if name == 'galeria':
            before = page.locator('.gallery-item:not(.oculto)').count()
            page.locator('#carregar-mais').click()
            assert page.locator('.gallery-item:not(.oculto)').count() == before + 48
    page.emulate_media(reduced_motion='reduce')
    page.goto('http://127.0.0.1:8000',wait_until='networkidle')
    assert page.locator('.hero-photo img').evaluate('(el)=>getComputedStyle(el).transform') == 'none'
    assert not errors, errors
    context = browser.new_context(java_script_enabled=False, viewport={'width':390,'height':900})
    plain = context.new_page()
    plain.goto('http://127.0.0.1:8000')
    assert plain.locator('.menu-item:visible').count() == 9
    browser.close()
print(json.dumps({'status':'PASS','checks':['local assets','filters','lightbox and keyboard','form validation and WhatsApp URL without sending','home widths 320–1440','all inner pages mobile and desktop','gallery load more','reduced motion','content without JavaScript','no JavaScript errors']}))
