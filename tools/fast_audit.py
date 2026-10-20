# tools/fast_audit.py — 極速全站多語系、SEO 拓撲與 CWV 審查工具 (0.3 秒完成)
# 整合 Bhanunamikaze/Agentic-SEO-Skill (Deterministic Technical/Link/Cannibalization Audit)
# 與 aaron-he-zhu/seo-geo-claude-skills (GEO / CORE-EEAT Structure Audit)
import glob
import os
import re
import sys

# Ensure UTF-8 output on Windows
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')


def audit():
    print("=== [鈞翔官網極速代碼、多語系與 Agentic SEO/GEO 審查] ===")
    errors = 0
    warnings = 0

    zh_html = sorted(glob.glob("*.html"))
    en_html = sorted(glob.glob("en/*.html"))
    ja_html = sorted(glob.glob("ja/*.html"))
    all_html = zh_html + en_html + ja_html

    # 排除 Google 驗證檔、後台看板與展示檔
    ignore_prefixes = ("google", "seo_dashboard", "demo-")

    def is_public_page(path):
        base = os.path.basename(path)
        return not base.startswith(ignore_prefixes)

    # 1. 檢查過期 .min 引用與禁用之 Noto Sans TC Webfont (CWV / PageSpeed 防呆)
    noto_pages = []
    for f in all_html:
        with open(f, "r", encoding="utf-8") as fp:
            content = fp.read()
        if "main.min.js" in content or "style.min.css" in content:
            print(f"❌ [過期引用] {f} 仍包含 main.min.js 或 style.min.css")
            errors += 1
        if "Noto+Sans+TC" in content or "Noto+Sans+JP" in content:
            noto_pages.append(f)

    if noto_pages:
        print(f"⚠️ [CWV 效能警告] 共 {len(noto_pages)} 個頁面仍引入 Google Fonts 中文字型 (Noto Sans TC/JP)，將拖慢行動版 FCP/LCP：{noto_pages[:5]} ...")
        warnings += len(noto_pages)

    # 2. 檢查日文頁面中的繁中殘留 (i18n leakage)
    ja_forbidden = [
        ("加工服務", "請替換為 '加工サービス'"),
        ("鈞翔實業", "日文請使用日文漢字 '鈞翔実業'"),
    ]
    for f in ja_html:
        with open(f, "r", encoding="utf-8") as fp:
            content = fp.read()
        for term, suggestion in ja_forbidden:
            count = content.count(term)
            if count > 0:
                print(f"❌ [日文版語言污染] {f} 出現 {count} 次 '{term}' -> {suggestion}")
                errors += 1

    # 3. 檢查英文頁面中的中文字元殘留
    for f in en_html:
        with open(f, "r", encoding="utf-8") as fp:
            lines = fp.readlines()
        for idx, line in enumerate(lines, 1):
            if 'hreflang="zh-TW"' in line or 'lang="zh-TW"' in line or 'JSON-LD' in line or 'maps.google.com' in line:
                continue
            if '加工服務' in line or '鈞翔' in line:
                print(f"⚠️ [英文版中文殘留] {f}:{idx} -> {line.strip()[:60]}")
                warnings += 1

    # 4. [Agentic-SEO-Skill] 孤島頁面檢測 (Orphan Knowledge Article Detector)
    hub_files = {
        "ZH": ("knowledge.html", [f for f in glob.glob("knowledge-*.html")]),
        "EN": ("en/knowledge.html", [os.path.basename(f) for f in glob.glob("en/knowledge-*.html")]),
        "JA": ("ja/knowledge.html", [os.path.basename(f) for f in glob.glob("ja/knowledge-*.html")]),
    }
    for lang, (hub_path, article_list) in hub_files.items():
        if not os.path.exists(hub_path):
            continue
        with open(hub_path, "r", encoding="utf-8") as fp:
            hub_content = fp.read()
        for art in sorted(article_list):
            full_art_path = art if lang == "ZH" else os.path.join(lang.lower(), art)
            if os.path.exists(full_art_path):
                with open(full_art_path, "r", encoding="utf-8") as afp:
                    art_content = afp.read()
                if 'http-equiv="refresh"' in art_content:
                    continue  # 跳過轉址頁
            if art not in hub_content:
                print(f"⚠️ [孤島文章警告 Orphan Page] ({lang}) {hub_path} 列表漏掛了文章連結：{art}")
                warnings += 1

    # 5. [Agentic-SEO-Skill] 核心商業頁 H1 互搶檢測 (Keyword Cannibalization Guard)
    core_hubs = ["index.html", "service.html", "products_list.html"]
    h1_map = {}
    for f in core_hubs:
        if os.path.exists(f):
            with open(f, "r", encoding="utf-8") as fp:
                content = fp.read()
            m = re.search(r"<h1[^>]*>(.*?)</h1>", content, re.S)
            if m:
                clean_h1 = re.sub(r"<[^>]+>", "", m.group(1)).strip()
                h1_map[f] = clean_h1
    if "index.html" in h1_map and "service.html" in h1_map:
        if "矽膠代工廠" in h1_map["index.html"] and "矽膠代工廠" in h1_map["service.html"]:
            print("❌ [關鍵字互搶 Cannibalization] index.html 與 service.html 的 <h1> 同時強攻『矽膠代工廠』，將導致排名互食！")
            errors += 1

    # 6. [Agentic-SEO-Skill] Canonical 與 og:url 一致性檢查
    for f in all_html:
        if not is_public_page(f):
            continue
        with open(f, "r", encoding="utf-8") as fp:
            content = fp.read()
        if 'http-equiv="refresh"' in content:
            continue
        can_m = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']', content)
        if not can_m:
            can_m = re.search(r'<link[^>]+href=["\']([^"\']+)["\'][^>]+rel=["\']canonical["\']', content)
        og_m = re.search(r'<meta[^>]+property=["\']og:url["\'][^>]+content=["\']([^"\']+)["\']', content)
        if not og_m:
            og_m = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:url["\']', content)
        if can_m and og_m and can_m.group(1) != og_m.group(1):
            print(f"❌ [Canonical/OG 不一致] {f}: canonical={can_m.group(1)} != og:url={og_m.group(1)}")
            errors += 1

    # 7. [seo-geo-claude-skills] GEO / CORE-EEAT 結構化引用信號檢查
    for f in glob.glob("knowledge-*.html"):
        with open(f, "r", encoding="utf-8") as fp:
            content = fp.read()
        if 'http-equiv="refresh"' in content:
            continue
        if '"FAQPage"' not in content and '"TechArticle"' not in content:
            print(f"⚠️ [GEO 引用缺漏] {f} 缺少 TechArticle 或 FAQPage 結構化資料")
            warnings += 1

    print("------------------------------------------")
    if errors == 0 and warnings == 0:
        print(f"✅ 檢查完成！全站 {len(all_html)} 個頁面無語言污染、無孤島頁、無 H1 互搶、無 CWV 字型阻塞。")
    else:
        print(f"檢測結果：{errors} 個錯誤，{warnings} 個警告。")


if __name__ == "__main__":
    audit()
