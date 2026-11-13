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

    # 2. 檢查日文頁面中的繁中殘留與台灣市話區碼 (i18n leakage)
    ja_forbidden = [
        ("加工服務", "請替換為 '加工サービス'"),
        ("鈞翔實業", "日文請使用日文漢字 '鈞翔実業'"),
        ("高規格防水密封", "請替換為日文 '高気密防水シール'"),
        ("(02)", "外語版電話/傳真請一律使用國際區碼 '+886-2-'"),
        ("tel:02", "外語版 tel: 連結請一律使用 'tel:+8862'"),
        ("台灣", "日文版請使用日文漢字 '台湾'"),
        ("新莊", "日文版請使用日文漢字 '新荘'"),
        ("版權所有", "日文版請使用 'All Rights Reserved.'"),
        ("技術知識庫", "日文版請使用 '技術知識ベース'"),
        ("閱讀全文", "日文版請使用 '全文を読む'"),
        ("收起文章", "日文版請使用 '記事を閉じる'"),
        ("游標卡尺", "日文版請使用 'ノギス'"),
    ]
    # 日文未採用之繁體專用字集（排除 HTML 註解、data-value、_subject、繁中）
    strictly_tc_chars = set("灣莊區號權閱讀關實產證們錄專營壓體國廠處擊傳檔詢價擇發應變學與對為從還經點當將樣氣齒龍龜數游")
    for f in ja_html:
        with open(f, "r", encoding="utf-8") as fp:
            lines = fp.readlines()
        content = "".join(lines)
        for term, suggestion in ja_forbidden:
            count = content.count(term)
            if count > 0:
                print(f"❌ [日文版語言污染] {f} 出現 {count} 次 '{term}' -> {suggestion}")
                errors += 1
        for idx, line in enumerate(lines, 1):
            if "<!--" in line and "-->" in line:
                continue
            if 'data-value=' in line or '_subject' in line or 'hreflang="zh-TW"' in line:
                continue
            clean = line.replace("繁中", "")
            found = sorted(set(ch for ch in clean if ch in strictly_tc_chars))
            if found:
                print(f"❌ [日文版繁體字元殘留] {f}:{idx} 發現繁體字 {found} -> {line.strip()[:60]}")
                errors += 1

    # 3. 檢查英文頁面中的中文字元殘留與台灣市話區碼
    for f in en_html:
        with open(f, "r", encoding="utf-8") as fp:
            lines = fp.readlines()
        for idx, line in enumerate(lines, 1):
            if 'hreflang="zh-TW"' in line or 'lang="zh-TW"' in line or 'JSON-LD' in line or 'maps.google.com' in line:
                continue
            if '(02)' in line or 'tel:02' in line:
                print(f"❌ [英文版台灣市話殘留] {f}:{idx} 出現 '(02)' 或 'tel:02' -> 請改用 '+886-2-'")
                errors += 1
            clean = line.replace("繁中", "").replace("日本語", "")
            if re.search(r'[\u4e00-\u9fff]', clean):
                print(f"❌ [英文版中文字元殘留] {f}:{idx} -> {line.strip()[:60]}")
                errors += 1
            if 'OEM OEM' in line:
                print(f"⚠️ [英文版語法殘留] {f}:{idx} -> {line.strip()[:60]}")
                warnings += 1

    # 4. [Zero-Friction RFQ] 全站轉單四件套完整性檢查 (Phone / Email / Mobile Menu / RFQ Form)
    for f in all_html:
        if not is_public_page(f):
            continue
        with open(f, "r", encoding="utf-8") as fp:
            c = fp.read()
        if 'http-equiv="refresh"' in c:
            continue
        if "2203-9918" not in c and "22039918" not in c:
            print(f"❌ [轉單缺漏: 電話] {f} 缺少電話號碼 2203-9918")
            errors += 1
        if "andy_hsu@jun-hsiang.com.tw" not in c:
            print(f"❌ [轉單缺漏: 信箱] {f} 缺少聯絡信箱 andy_hsu@jun-hsiang.com.tw")
            errors += 1
        if 'id="mobile-menu"' not in c:
            print(f"❌ [轉單缺漏: 手機選單] {f} 缺少 id=\"mobile-menu\"")
            errors += 1
        if 'id="nav-toggle"' in c:
            print(f"❌ [過期選單代碼] {f} 仍使用已廢棄之 id=\"nav-toggle\"，請替換為標準 hamburger")
            errors += 1
        m_nav = re.search(r'<nav\b[^>]*>.*?</nav>', c, re.S)
        if m_nav:
            nav = m_nav.group(0)
            if len(re.findall(r'<div\b', nav)) != len(re.findall(r'</div>', nav)):
                print(f"❌ [DOM 標籤不對稱] {f} 的 <nav> 內 <div> 開閉數量不一致")
                errors += 1
            if 'class="lang-switcher"' not in nav and 'class="lang-selector"' not in nav:
                print(f"❌ [缺漏電腦版語言切換器] {f} 的 <nav> 缺少 .lang-switcher 或 .lang-selector")
                errors += 1
        m_foot = re.search(r'<footer\b[^>]*>.*?</footer>', c, re.S)
        if m_foot:
            foot = m_foot.group(0)
            if len(re.findall(r'<div\b', foot)) != len(re.findall(r'</div>', foot)):
                print(f"❌ [DOM 標籤不對稱] {f} 的 <footer> 內 <div> 開閉數量不一致")
                errors += 1
        base = os.path.basename(f)
        if base.startswith("knowledge-"):
            for m_lang in re.finditer(r'<div class="(?:lang-dropdown|lang-switcher|mobile-lang-links)">(.*?)</div>', c, re.S):
                if base not in m_lang.group(1):
                    print(f"❌ [跨語系切換錯誤] {f} 的語言切換器未精準指向 {base}（禁止指向總覽頁 knowledge.html）")
                    errors += 1

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

    # 8. [Zero-Friction RFQ] 外語商業頁與獨立文章 100% 表單與一鍵複製信箱覆蓋檢查
    for f in en_html + ja_html:
        if not is_public_page(f):
            continue
        with open(f, "r", encoding="utf-8") as fp:
            c = fp.read()
        if 'http-equiv="refresh"' in c:
            continue
        if 'data-copy-email="andy_hsu@jun-hsiang.com.tw"' not in c:
            print(f"❌ [轉單缺漏: 一鍵複製信箱] {f} 缺少 data-copy-email=\"andy_hsu@jun-hsiang.com.tw\"")
            errors += 1
        if "contact.html" in c:
            print(f"❌ [死連結 404] {f} 包含不存在的 contact.html 連結（請改用 #rfq-section 或 index.html#contact）")
            errors += 1
        if os.path.basename(f) == "knowledge.html":
            continue
        if "formsubmit.co/jojo.li888@msa.hinet.net" not in c or 'type="file"' not in c:
            print(f"❌ [轉單缺漏: 內嵌帶圖詢價表單] {f} 缺少 formsubmit.co 內嵌表單或 type=\"file\" 上傳欄位")
            errors += 1

    # 9. [GSC Indexing Guard] 外語版標準首頁連結統一與空白膨脹檢查
    for f in en_html + ja_html:
        if not is_public_page(f):
            continue
        with open(f, "r", encoding="utf-8") as fp:
            c = fp.read()
        if 'http-equiv="refresh"' in c:
            continue
        if re.search(r'href="(?:index\.html(?:#[^"]*)?|\.\./(?:en|ja)/index\.html(?:#[^"]*)?)"', c):
            print(f"❌ [Canonical 網址分裂] {f} 仍使用非標準首頁連結 href=\"index.html\"，請改為 \"./\" 或 \"../en/\" / \"../ja/\"")
            errors += 1
        if re.search(r'\n(?:[ \t]*\n){5,}', c):
            print(f"❌ [HTML 空白行膨脹] {f} 包含連續超過 5 行的空白換行，會稀釋 Code-to-Text Ratio")
            errors += 1

    # 10. [Resend / reCAPTCHA 必達保證] 所有知識庫文章表單必須掛載 g-recaptcha
    for f in all_html:
        if not is_public_page(f):
            continue
        if not os.path.basename(f).startswith("knowledge-"):
            continue
        with open(f, "r", encoding="utf-8") as fp:
            c = fp.read()
        if 'http-equiv="refresh"' in c:
            continue
        if 'id="general-submit-btn"' in c and 'g-recaptcha' not in c:
            print(f"❌ [發信斷路: 缺漏 reCAPTCHA] {f} 缺少 g-recaptcha，將跳過 EmailJS/Resend 發信")
            errors += 1

    print("------------------------------------------")
    if errors == 0 and warnings == 0:
        print(f"🎉 檢查完成！全站 {len(all_html)} 個頁面 100% 通過極速審計（0 錯誤、0 警告）！")
    else:
        print(f"檢測結果：{errors} 個錯誤，{warnings} 個警告。")


if __name__ == "__main__":
    audit()
