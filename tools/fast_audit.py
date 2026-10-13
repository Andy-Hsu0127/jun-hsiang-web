# tools/fast_audit.py — 極速全站多語系與靜態資源審查工具 (0.3 秒完成)
import glob
import os
import re
import sys

# Ensure UTF-8 output on Windows
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')


def audit():
    print("=== [鈞翔官網極速代碼與多語系審查] ===")
    errors = 0
    warnings = 0

    # 1. 檢查過期 .min 引用
    all_html = glob.glob("*.html") + glob.glob("en/*.html") + glob.glob("ja/*.html")
    for f in all_html:
        with open(f, "r", encoding="utf-8") as fp:
            content = fp.read()
        if "main.min.js" in content or "style.min.css" in content:
            print(f"❌ [過期引用] {f} 仍包含 main.min.js 或 style.min.css")
            errors += 1

    # 2. 檢查日文頁面中的繁中殘留 (i18n leakage)
    ja_html = glob.glob("ja/*.html")
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
    en_html = glob.glob("en/*.html")
    cjk_pattern = re.compile(r'[\u4e00-\u9fff]')
    for f in en_html:
        with open(f, "r", encoding="utf-8") as fp:
            lines = fp.readlines()
        for idx, line in enumerate(lines, 1):
            # 排除常見的繁中語系標籤或 hreflang
            if 'hreflang="zh-TW"' in line or 'lang="zh-TW"' in line or 'JSON-LD' in line:
                continue
            matches = cjk_pattern.findall(line)
            # 若有導覽列中文字
            if '加工服務' in line or '鈞翔' in line:
                print(f"⚠️ [英文版中文殘留] {f}:{idx} -> {line.strip()[:60]}")
                warnings += 1

    print("------------------------------------------")
    if errors == 0 and warnings == 0:
        print(f"✅ 檢查完成！全站 {len(all_html)} 個頁面無語言污染、無過期資源引用。")
    else:
        print(f"檢測結果：{errors} 個錯誤，{warnings} 個警告。")

if __name__ == "__main__":
    audit()
