import glob, html, json, os, re

# Deterministic Category & Industry mapping by slug
META_MAP = {
    "index.html": ("process", ["general", "industrial", "med_food", "auto"], "矽膠代工 橡膠代工 LSR HCR 開模 OEM custom silicone parts manufacturer 台湾 シリコーン ゴム 成形"),
    "service.html": ("process", ["general", "industrial", "auto", "med_food"], "LSR 液態射出 固態熱壓 異材包膠 包鐵 包塑膠 自潤矽膠 compression injection overmolding 射出成形 圧縮成形 インサート成形"),
    "products_list.html": ("product", ["general", "industrial", "uav_3c", "auto"], "產品目錄 O型環 導電按鍵 防振腳墊 密封圈 保護套 O-ring keypad gasket seal feet 製品一覧 キーパッド パッキン"),
    "knowledge.html": ("material", ["general"], "技術知識庫 選型指南 案例 technical knowledge base 技術知識ベース"),
    "knowledge-ai-server-drone.html": ("product", ["semi_ai", "uav_3c"], "AI伺服器 無人機 散熱 防振 導熱矽膠 server UAV drone thermal damping サーバー ドローン 放熱"),
    "knowledge-automotive-waterproof-connector.html": ("product", ["auto"], "車載 防水插座 連接器 IP69K LSR 雙色包膠 automotive connector waterproof socket 車載 防水コネクタ"),
    "knowledge-automotive-wire-harness-seals.html": ("product", ["auto"], "車用 線束 防水栓 SWS 自潤矽膠 wire harness single wire seal plug ワイヤーハーネス 防水シール"),
    "knowledge-conductive-keypad.html": ("product", ["uav_3c", "industrial", "med_food"], "導電按鍵 碳粒 電阻 行程 彈力 按鍵設計 conductive silicone keypad tactile carbon pill 導電性 キーパッド"),
    "knowledge-food-grade-silicone-fda.html": ("material", ["med_food"], "食品級 FDA LFGB SGS 鉑金矽膠 21 CFR 177.2600 food grade migration 食品グレード"),
    "knowledge-industrial-vibration-feet.html": ("product", ["industrial"], "防振腳墊 避震腳 緩衝墊 載重 硬度 anti-vibration feet mount damping 防振脚 ゴム脚"),
    "knowledge-industrial-vibration-pad.html": ("product", ["industrial"], "重工業 避震腳墊 矽膠包鐵 撕裂強度 heavy-duty vibration pad rubber to metal bonding 重工業 防振 金属焼付"),
    "knowledge-large-shot-lsr-molding.html": ("process", ["industrial", "med_food"], "大射出量 厚肉 大重量 LSR 脫泡 large shot thick wall degassing 大容量 厚肉 気泡"),
    "knowledge-lsr-liquid-silicone.html": ("process", ["med_food", "auto", "uav_3c"], "LSR 液態矽膠 射出成型 LIM 白金催化 liquid silicone rubber injection molding 液状シリコーン 射出成形"),
    "knowledge-lsr-silicone-supplier-taiwan.html": ("process", ["general", "med_food", "auto"], "LSR 供應商 廠商挑選 冷流道 supplier cold runner メーカー選定"),
    "knowledge-lsr-silicone-vs-hcr.html": ("process", ["general", "industrial", "med_food"], "LSR vs HCR SSR 液態 固態 熱壓 比較 模具費 high consistency rubber compression 比較"),
    "knowledge-medical-lsr-mask.html": ("product", ["med_food"], "醫療級 呼吸面罩 矽膠墊片 ISO 10993 FDA medical grade mask respiratory cushion 医療用 マスク"),
    "knowledge-oring-seal-custom-mold.html": ("product", ["industrial", "semi_ai", "auto"], "O型環 防水圈 密封件 客製開模 AS568 JIS B2401 O-ring seal gasket custom mold Oリング シール"),
    "knowledge-rubber-factory-guide.html": ("process", ["industrial", "auto"], "橡膠工廠 橡膠代工 NBR EPDM Viton 橡膠包鐵 rubber factory bonding ゴム工場"),
    "knowledge-self-bonding-lsr-guide.html": ("process", ["auto", "uav_3c", "med_food"], "自黏型 LSR 免底塗 塑膠包膠 PC PA PBT self-bonding primerless overmolding 自己接着性 プライマーレス"),
    "knowledge-self-lubricating-silicone.html": ("material", ["auto", "med_food", "industrial"], "自潤矽膠 吐油 析油 降低插拔力 self-lubricating oil-bleeding 自己潤滑性 オイルブリード"),
    "knowledge-semiconductor-silicone-seal.html": ("material", ["semi_ai"], "半導體 面板 FPD 無塵室 低逸氣 耐電漿 semiconductor cleanroom low outgassing plasma 半導体 低アウトガス"),
    "knowledge-shore-hardness-guide.html": ("material", ["general", "industrial", "med_food"], "矽膠硬度 Shore A 蕭氏硬度 10度 30度 50度 70度 80度 hardness durometer 硬度 ショアA"),
    "knowledge-silicone-factory-guide.html": ("process", ["general", "industrial"], "矽膠工廠 矽膠代工 挑選指南 開模費用 silicone factory guide OEM シリコーン工場"),
    "knowledge-silicone-metal-bonding-failure.html": ("material", ["industrial", "auto"], "矽膠包金屬 脫膠 剝離 噴砂 底塗 ASTM D429 delamination bonding failure primer 剥離 接着対策"),
    "knowledge-silicone-overmolding-bonding.html": ("process", ["industrial", "auto"], "矽膠包鐵 鋁 銅 不鏽鋼 異材結合 物理錨固 rubber to metal bonded parts aluminum steel brass 金属焼付"),
    "knowledge-silicone-overmolding.html": ("process", ["auto", "uav_3c", "industrial"], "矽膠包塑膠 異材包膠 PC PA PBT insert molding overmolding plastic metal インサート成形"),
    "knowledge-solid-vs-lsr.html": ("process", ["general", "industrial"], "固態矽膠 熱壓 LSR 射出 差異 製程選擇 solid silicone compression vs LSR 固形シリコン"),
    "knowledge-uav-silicone-parts.html": ("product", ["uav_3c"], "無人機 避震球 防水圈 起落架 UAV drone gimbal damping ball waterproof ring ドローン 防振ボール"),
    "knowledge-viton-vs-fvmq.html": ("material", ["semi_ai", "auto", "industrial"], "Viton FKM FVMQ 氟橡膠 氟矽膠 耐油 耐酸鹼 耐化學溶劑 fluorosilicone chemical resistance フッ素ゴム フルオロシリコーン"),
}

def clean_title(t):
    t = html.unescape(re.sub(r"\s+", " ", t).strip())
    for sep in (" | ", "｜", " — ", " - 鈞翔"):
        if sep in t:
            parts = t.split(sep)
            if any(b in parts[-1] for b in ("鈞翔", "Jun-Hsiang")):
                t = sep.join(parts[:-1]).strip()
    return t

def build_lang(prefix):
    items = []
    for fn in sorted(glob.glob(f"{prefix}*.html")):
        base = os.path.basename(fn)
        if base.startswith(("google", "seo_dashboard", "demo-")) or base == "404.html":
            continue
        c = open(fn, encoding="utf-8").read()
        if 'http-equiv="refresh"' in c:
            continue
        tm = re.search(r"<title>(.*?)</title>", c, re.S)
        dm = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)["\']', c) or \
             re.search(r'<meta[^>]+content=["\']([^"\']*)["\'][^>]+name=["\']description["\']', c)
        title = clean_title(tm.group(1)) if tm else base
        desc = html.unescape(dm.group(1).strip()) if dm else ""
        if len(desc) > 110:
            desc = desc[:107].rstrip() + "..."
        cat, ind, kw = META_MAP.get(base, ("material", ["general"], ""))
        url = "./" if base == "index.html" else base
        items.append({
            "u": url,
            "t": title,
            "d": desc,
            "c": cat,
            "i": ind,
            "k": kw,
        })
    return items

out = {
    "zh": build_lang(""),
    "en": build_lang("en/"),
    "ja": build_lang("ja/"),
}

os.makedirs("js", exist_ok=True)
with open("js/search-index.json", "w", encoding="utf-8", newline="\n") as fp:
    json.dump(out, fp, ensure_ascii=False, separators=(",", ":"))

size_kb = os.path.getsize("js/search-index.json") / 1024
print(f"Built js/search-index.json ({size_kb:.1f} KB): zh={len(out['zh'])}, en={len(out['en'])}, ja={len(out['ja'])}")
