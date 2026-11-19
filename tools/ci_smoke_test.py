import glob, json, re, sys
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8080"

def check_jsonld():
    checked = 0
    for pattern in ("*.html", "en/*.html", "ja/*.html"):
        for f in sorted(glob.glob(pattern)):
            if any(x in f for x in ("google", "seo_dashboard", "demo-")):
                continue
            c = open(f, encoding="utf-8").read()
            for m in re.finditer(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', c, re.S):
                checked += 1
                json.loads(m.group(1))
    json.loads(open("js/search-index.json", encoding="utf-8").read())
    print(f"OK: {checked} JSON-LD blocks + js/search-index.json valid.")

def run_browser_smoke():
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        page.on("pageerror", lambda err: errors.append(f"pageerror: {err}"))
        page.on("console", lambda msg: errors.append(f"console.{msg.type}: {msg.text}") if msg.type == "error" else None)

        # 1. ZH homepage
        r = page.goto(f"{BASE}/", wait_until="networkidle")
        assert r.status == 200
        assert page.locator("#tw-line-float-btn").is_visible(), "Missing Taiwan LINE button on /"
        assert page.locator("#site-search-trigger").is_visible(), "Missing search button on /"
        page.locator("#site-search-trigger").click()
        assert page.locator("#site-search-modal").is_visible(), "Search modal failed to open on /"
        page.locator("#site-search-close").click()

        # 2. EN homepage (LINE must be absent)
        r = page.goto(f"{BASE}/en/", wait_until="networkidle")
        assert r.status == 200
        assert page.locator("#tw-line-float-btn").count() == 0, "LINE button leaked onto /en/"
        assert page.locator("#us-eu-sourcing-guides a").count() == 7, "Missing US/EU hub links on /en/"
        page.locator("#site-search-trigger").click()
        assert page.locator("#site-search-modal").is_visible(), "Search modal failed to open on /en/"
        page.locator("#site-search-close").click()

        # 3. JA homepage (LINE must be absent)
        r = page.goto(f"{BASE}/ja/", wait_until="networkidle")
        assert r.status == 200
        assert page.locator("#tw-line-float-btn").count() == 0, "LINE button leaked onto /ja/"
        page.locator("#site-search-trigger").click()
        assert page.locator("#site-search-modal").is_visible(), "Search modal failed to open on /ja/"
        page.locator("#site-search-close").click()

        # 4. Top traffic ZH article
        r = page.goto(f"{BASE}/knowledge-shore-hardness-guide.html", wait_until="networkidle")
        assert r.status == 200
        assert page.locator("#tw-moq-trust-strip").is_visible(), "Missing trust strip on top ZH article"

        browser.close()

    if errors:
        print("Browser console/page errors:", errors)
        sys.exit(1)
    print("OK: Playwright smoke test passed across /, /en/, /ja/, and top article with 0 errors.")

if __name__ == "__main__":
    check_jsonld()
    run_browser_smoke()
