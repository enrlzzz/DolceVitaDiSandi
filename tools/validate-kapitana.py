"""Read-only browser audit for the Dolce Vita storefront.

Run: python tools/validate-kapitana.py [--screenshots]
Screenshots, when requested, go to tools/kapitana-captures/.
"""

import argparse
import json
from urllib.parse import parse_qs
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parent.parent
BASE = "http://127.0.0.1:8000/"
PAGES = ["", "Client/Public/Src/Pages/cardapio.html",
         "Client/Public/Src/Pages/galeria.html",
         "Client/Public/Src/Pages/politica-de-privacidade.html",
         "Client/Public/Src/Pages/politica-de-reembolso.html"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--screenshots", action="store_true")
    parser.add_argument("--internals-only", action="store_true", help="Skip the home page while its redesign is in progress")
    parser.add_argument("--home-only", action="store_true", help="Run only the new home page")
    args = parser.parse_args()
    captures = ROOT / "tools" / "kapitana-captures"
    if args.screenshots:
        captures.mkdir(exist_ok=True)
    findings = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="msedge")
        context = browser.new_context()
        page = context.new_page()
        page.on("pageerror", lambda error: findings.append({"kind": "js-error", "page": page.url, "detail": str(error)}))
        page.on("response", lambda response: findings.append({"kind": "http-error", "page": page.url, "detail": f"{response.status} {response.url}"}) if response.status >= 400 and response.url.startswith(BASE) else None)

        paths = PAGES[1:] if args.internals_only else PAGES[:1] if args.home_only else PAGES
        for path in paths:
            url = urljoin(BASE, path)
            widths = [(320, "mobile-320"), (390, "mobile-390"), (768, "tablet"), (1440, "desktop")] if not path else [(320, "mobile-320"), (390, "mobile-390"), (1440, "desktop")]
            for width, label in widths:
                page.set_viewport_size({"width": width, "height": 900})
                response = page.goto(url, wait_until="domcontentloaded")
                page.wait_for_timeout(400)
                if response.status >= 400:
                    findings.append({"kind": "page-error", "page": url, "detail": str(response.status)})
                overflow = page.evaluate("document.documentElement.scrollWidth > innerWidth + 1")
                if overflow:
                    culprits = page.evaluate("""() => ({width: innerWidth, scrollWidth: document.documentElement.scrollWidth, elements: Array.from(document.querySelectorAll('body *')).filter(el => el.getBoundingClientRect().right > innerWidth + 1).slice(0, 12).map(el => ({tag: el.tagName, className: typeof el.className === 'string' ? el.className : '', id: el.id, text: el.textContent.trim().slice(0, 65), right: Math.round(el.getBoundingClientRect().right), parent: el.parentElement?.className}))})""")
                    findings.append({"kind": "horizontal-overflow", "page": url, "detail": {"viewport": label, **culprits}})
                if args.screenshots:
                    name = path.rsplit("/", 1)[-1].replace(".html", "") or "home"
                    page.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(image => image.loading = 'eager')")
                    page.wait_for_function("Array.from(document.querySelectorAll('img[src]')).every(image => image.complete)", timeout=30000)
                    page.screenshot(path=str(captures / f"{name}-{label}.png"), full_page=True)

            soup = BeautifulSoup(page.content(), "html.parser")
            for element in soup.select("[href], [src], [srcset], [data-grande]"):
                values = [element.get("href"), element.get("src"), element.get("data-grande")]
                values += [item.strip().split(" ")[0] for item in element.get("srcset", "").split(",") if item.strip()]
                for value in filter(None, values):
                    parsed = urlparse(value)
                    if parsed.scheme or not value.startswith("/"):
                        continue
                    local = ROOT / unquote(parsed.path).lstrip("/")
                    if not local.is_file() and not (local.is_dir() and parsed.path == "/"):
                        findings.append({"kind": "missing-local-target", "page": url, "detail": value})

        if not args.internals_only:
            audit_home(page, findings, captures if args.screenshots else None)
        if not args.home_only:
            page.set_viewport_size({"width": 1440, "height": 900})
            page.goto(urljoin(BASE, PAGES[2]), wait_until="domcontentloaded")
            page.wait_for_timeout(400)
            try:
                audit_gallery(page, findings)
            except Exception as error:
                findings.append({"kind": "interaction", "page": page.url, "detail": str(error).splitlines()[0]})
        browser.close()
    unique = list({json.dumps(item, sort_keys=True, ensure_ascii=False): item for item in findings}.values())
    print(json.dumps({"status": "PASS" if not unique else "FAIL", "findings": unique}, ensure_ascii=False, indent=2))
    return int(bool(unique))


def audit_gallery(page, findings):
            initial = page.locator("#galeria .gallery-item:not(.oculto)").count()
            total = page.locator("#galeria .gallery-item").count()
            page.locator("#carregar-mais").click(timeout=2000)
            after = page.locator("#galeria .gallery-item:not(.oculto)").count()
            if after <= initial:
                findings.append({"kind": "interaction", "page": page.url, "detail": "Carregar mais did not reveal photos"})
            page.locator(".gallery-botao").first.click(timeout=2000)
            if not page.locator("#lightbox").is_visible():
                findings.append({"kind": "interaction", "page": page.url, "detail": "Lightbox did not open"})
            else:
                before = page.locator("#lightbox-img").get_attribute("src")
                page.keyboard.press("ArrowRight")
                if page.locator("#lightbox-img").get_attribute("src") == before:
                    findings.append({"kind": "interaction", "page": page.url, "detail": "ArrowRight did not advance lightbox"})
                page.keyboard.press("Escape")
                if page.locator("#lightbox").is_visible():
                    findings.append({"kind": "interaction", "page": page.url, "detail": "Escape did not close lightbox"})
            print(f"Gallery: {initial}/{total} initially, {after}/{total} after load more")


def audit_home(page, findings, captures):
    page.set_viewport_size({"width": 1440, "height": 1000})
    page.goto(BASE, wait_until="domcontentloaded")
    page.wait_for_timeout(500)

    def check(label, action):
        try:
            action()
        except Exception as error:
            findings.append({"kind": "home-interaction", "page": BASE, "detail": f"{label}: {str(error).splitlines()[0]}"})

    def scene_tabs():
        for index in range(3):
            tab = page.locator(f'[data-scene="{index}"]')
            tab.click()
            assert tab.get_attribute("aria-pressed") == "true", f"scene {index} inactive"
            assert page.locator("#hero-scene").get_attribute("src"), "scene image empty"
            assert page.locator("#scene-caption").inner_text().strip(), "scene caption empty"
    check("hero tabs", scene_tabs)

    def filters():
        counts = {}
        for name in ["todos", "doces", "cookies"]:
            button = page.locator(f'[data-filter="{name}"]')
            button.click()
            assert button.get_attribute("aria-pressed") == "true", f"filter {name} inactive"
            count = page.locator("#products > :visible").count()
            assert count > 0, f"filter {name} empty"
            counts[name] = count
        assert any(count < counts["todos"] for name, count in counts.items() if name != "todos"), counts
        page.locator('[data-filter="todos"]').click()
    check("product filters", filters)

    def product_dialog():
        product = page.locator('#products button[aria-label^="Ver "]').first
        product.click()
        assert page.locator("#product-dialog").is_visible(), "product modal closed"
        assert page.locator("#dialog-body").inner_text().strip(), "product modal empty"
        page.keyboard.press("Escape")
        assert not page.locator("#product-dialog").is_visible(), "Escape did not close product modal"
    check("product modal and keyboard", product_dialog)

    def ingredient_tabs():
        for index in range(3):
            page.locator(f'.ingredient-tabs [data-ingredient="{index}"]').click()
            assert page.locator(f'.ingredient-tabs [data-ingredient="{index}"]').get_attribute("aria-pressed") == "true"
            assert page.locator("#ingredient-copy").inner_text().strip(), f"ingredient {index} empty"
        page.locator('.lab-photo [data-ingredient="0"]').click()
        assert page.locator('.ingredient-tabs [data-ingredient="0"]').get_attribute("aria-pressed") == "true"
    check("ingredient tabs and hotspots", ingredient_tabs)

    def suggestions():
        results = []
        for mood in ["chocolate", "crocante", "cafe"]:
            page.locator(f'input[name="mood"][value="{mood}"]').check()
            value = page.locator("#pair-result").inner_text().strip()
            assert value, f"suggestion {mood} empty"
            results.append(value)
        assert len(set(results)) > 1, "suggestions never change"
    check("taste suggestions", suggestions)

    def selection():
        page.locator('#products button[aria-label^="Ver "]').first.click()
        assert page.locator("#product-dialog").is_visible(), "product modal did not open"
        page.locator('#product-dialog button:has-text("Adicionar")').click()
        count = int(page.locator("#selection-count").inner_text())
        assert count > 0, "selection count did not increase"
        page.reload(wait_until="domcontentloaded")
        assert int(page.locator("#selection-count").inner_text()) == count, "selection did not persist after reload"
        page.locator("#selection-button").click()
        assert page.locator("#selection-dialog").is_visible(), "selection modal closed"
        assert page.locator("#selection-list").inner_text().strip(), "selection list empty"
        href = page.locator("#selection-whatsapp").get_attribute("href")
        assert href and urlparse(href).netloc == "wa.me", f"invalid WhatsApp URL: {href}"
        assert parse_qs(urlparse(href).query).get("text"), "WhatsApp message missing"
        assert page.locator("#selection-list").inner_text().split("remover")[0].strip() in parse_qs(urlparse(href).query)["text"][0], "selected product missing from WhatsApp message"
        remove = page.locator('#selection-list [data-remove], #selection-list button[aria-label*="Remover"]')
        assert remove.count(), "remove control missing"
        remove.first.click()
        assert int(page.locator("#selection-count").inner_text()) < count, "selection count did not decrease"
        page.keyboard.press("Escape")
        assert not page.locator("#selection-dialog").is_visible(), "Escape did not close selection modal"
    check("selection add/remove/persistence/WhatsApp", selection)

    def gallery_lightbox():
        page.locator("[data-gallery-src]").first.click()
        assert page.locator("#home-lightbox").is_visible(), "photo modal closed"
        assert page.locator("#home-lightbox-image").get_attribute("src"), "photo source empty"
        page.keyboard.press("Escape")
        assert not page.locator("#home-lightbox").is_visible(), "Escape did not close photo modal"
    check("home gallery keyboard", gallery_lightbox)

    if captures:
        # Reference is 1440×1000. Keep a like-for-like hero capture for visual review.
        page.set_viewport_size({"width": 1440, "height": 1000})
        page.goto(BASE, wait_until="domcontentloaded")
        page.evaluate("document.querySelectorAll('img[src]').forEach(image => image.loading = 'eager')")
        try:
            page.wait_for_function("Array.from(document.querySelectorAll('img[src]')).every(image => image.complete && image.naturalWidth > 0)", timeout=30000)
        except Exception:
            broken = page.evaluate("Array.from(document.querySelectorAll('img[src]')).filter(image => !image.complete || !image.naturalWidth).map(image => image.src)")
            findings.append({"kind": "image-load", "page": BASE, "detail": broken})
        page.screenshot(path=str(captures / "home-reference-viewport.png"))
        page.screenshot(path=str(captures / "home-full-loaded.png"), full_page=True)
        reference = ROOT / "tools" / "reference.tmp.png"
        if not reference.is_file():
            findings.append({"kind": "visual", "page": BASE, "detail": "reference.tmp.png missing"})
        else:
            print(f"Visual review: {captures / 'home-reference-viewport.png'} versus {reference}")


if __name__ == "__main__":
    raise SystemExit(main())
