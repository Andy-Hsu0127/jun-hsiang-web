---
name: website_seo
description: Manage the website's SEO strategy, technical content generation, and article database to prevent duplicate topics.
---

# Website SEO Content & Article Database

This skill manages the SEO content writing workflow and maintains a historical list of all technical articles published on the Jun-Hsiang website (`index.html`, `knowledge.html`, etc.) in Traditional Chinese, English, and Japanese.

## Technical Article & Structured Data Guidelines
When writing or generating new technical articles, products, or services for the website:
1. **No Duplication**: Always consult the **Published Article Database** below. Do NOT write about a topic, material, or application that is already heavily covered.
2. **HTML Structure & Anchor ID**: Articles must be formatted as `<article class="article-card" id="[slug-id]" data-category="[tech|case]" data-tags="[tag1,tag2,...]">` HTML structures compatible with the custom JS filter in `knowledge.html`. The `id` attribute is mandatory and must be a unique, English url-safe slug corresponding to the article topic.
3. **Semantic Time Tag**: Every article card's date metadata must use a `<time>` tag with a valid `datetime` attribute:
   `發布日期：<time datetime="YYYY-MM-DD">YYYY-MM-DD</time>`
4. **JSON-LD Schema Updates**:
   - **Articles**: For each article added, insert a corresponding `TechArticle` or `Article` JSON-LD schema inside the `<head>` of the page. The `@id` and `url` fields of the schema must link directly to the anchor (e.g. `https://andy-hsu0127.github.io/jun-hsiang-web/knowledge.html#[slug-id]`).
   - **Products & Services**: New products in `products_list.html` must be appended to the JSON-LD `ItemList` schema. New services or FAQs in `service.html` must update the corresponding `Service` and `FAQPage` schemas.
5. **Multi-language Alignment**: Every new article/page must be written in **Traditional Chinese**, **English**, and **Japanese**, and inserted at the top of the respective HTML files in the root, `/en/`, and `/ja/` folders. Ensure translated schema metadata is also injected.
6. **Clean Code & Hash Routing**: Ensure the JS click event listener is preserved. Do not break the deep-linking hash routing logic in `knowledge.html` which auto-expands cards when landing via `#[slug-id]`.
7. **No "全自動" (Fully Automatic) wording**: Avoid "全自動" or "自動" in equipment/machinery descriptions unless specifically approved.
8. **No Fabricated / Unverified Specifications or Numbers**: Never invent or guess quantitative specifications (such as tolerances ±0.02mm, cycle times, machine tonnages) in proposals or article copy. Always stick to verified process capabilities, materials, ISO 9001 compliance, and custom engineering support.
9. **設計者競爭第一名思維與零奉承原則 (Champion Competitor Mindset & Zero Flattery)**:
   - **嚴禁奉承與廢話**：直接點出技術痛點與實質差距，禁止任何討好或罐頭話術。
   - **以競爭第一名為唯一標準**：SEO 架構、內容深度、轉換路徑必須全方位壓制同業對手（佑祥、定伸、志得、詹輝等），目標鎖定 Google 第一頁前 3 名。
   - **全關鍵字矩陣平衡覆蓋（Multi-Keyword Protection）**：優化單一詞（如 LSR）時，絕不犧牲其他核心詞（固態矽膠熱壓、異材結合包膠、橡膠代工、自潤矽膠、密封件）。必須透過「專屬 Landing Page 拓撲」讓每個核心工藝都有專屬第一名頁面，避免關鍵字蠶食（Keyword Cannibalization）。
   - **效能零容忍（Zero Performance Degradation）**：任何 SEO 或內容更新，必須確保 PageSpeed 電腦 95-100、手機 90+，嚴禁任何會拖慢速度的代碼。

---

## Published Article Database

### 1. 無人機精密矽橡膠零件設計指南
* **Anchor ID / ID**: `uav-silicone-parts`
* **Title (ZH)**: 《無人機精密矽橡膠零件設計指南：避震球、防水圈與起落架避震結構材料全解析》
* **Title (EN)**: 《UAV Precision Silicone & Rubber Components Design Guide: Vibration Dampers, Waterproof Rings, and Landing Gear Shock Absorption》
* **Title (JA)**: 《ドローン精密シリコーン・ゴム部品の設計ガイド：防振ボール、防水リング、および着陸装置用衝撃吸収システム材料解析》
* **Category**: `tech`
* **Key Topics**: Drones, Vibration Dampers (Gimbal balls), Waterproof O-rings, NBR, LSR, PU.

### 2. AI 伺服器與無人機關鍵應用
* **Anchor ID / ID**: `ai-server-drone`
* **Title (ZH)**: 《AI 伺服器與無人機的崛起：高階精密矽橡膠零件的關鍵應用與設計趨勢》
* **Title (EN)**: 《The Rise of AI Servers and UAVs: Critical Applications and Design Trends of High-End Precision Silicone Rubber Parts》
* **Title (JA)**: 《AIサーバーとドローン産業の台頭：高付加價值精密シリコーン・ゴム部品の重要応用と設計トレンド》
* **Category**: `tech`
* **Key Topics**: AI Servers, GPU cooling, Liquid cooling gaskets, Thermal Conductive Silicone (TIM), EMI shielding.

### 3. 固態熱壓與 LSR 液態射出製程對比
* **Anchor ID / ID**: `solid-vs-lsr`
* **Title (ZH)**: 《固態矽膠熱壓 vs. LSR 液態矽膠射出：如何選擇最適合的客製化製程？》
* **Title (EN)**: 《Solid Compression Molding vs. LSR Liquid Injection Molding: How to Choose the Best Custom Process?》
* **Title (JA)**: 《固形シリコーンゴム熱プレス vs. LSR液状シリコーンゴム射出成形：最適なカスタム製程の選定方法とは？》
* **Category**: `tech`
* **Key Topics**: Solid compression molding, LSR liquid injection molding, Tooling cost, Precision tolerances.

### 4. 矽膠包塑膠異材結合技術指南
* **Anchor ID / ID**: `silicone-overmolding`
* **Title (ZH)**: 《矽膠包塑膠（PC/PA工程塑膠包膠代工）：底塗化學鍵結與熱變形控制全解析》
* **Title (EN)**: 《Silicone Overmolding on Engineering Plastics (PC/PA): Primer Chemistry & Thermal Control》
* **Title (JA)**: 《シリコーンのエンジニアリングプラスチック（PC/PA）インサート成形：プライマー化学接着と熱変形制御》
* **Category**: `tech`
* **Key Topics**: 矽膠包塑膠, PC/PA包膠, Primer 化學鍵結, 低溫固化防變形, 模具防溢膠.

### 5. 導電矽膠按鍵設計指南
* **Anchor ID / ID**: `conductive-keypad`
* **Title (ZH)**: 《導電矽膠按鍵設計指南：電阻、行程與橡膠彈力規格全面解析》
* **Title (EN)**: 《Conductive Silicone Keypad Design Guide: In-Depth Analysis of Resistance, Travel, and Rubber Tactile Force Specifications》
* **Title (JA)**: 《導電性シリコンキーパッド設計ガイド：電気抵抗、キーストローク、およびゴム彈性仕様の徹底解説》
* **Category**: `tech`
* **Key Topics**: Conductive keypads, Contact resistance, Travel distance, Actuation force (click ratio).

### 6. 醫療級 LSR 液態矽膠呼吸面罩配件 (Case Study)
* **Anchor ID / ID**: `medical-lsr-mask`
* **Title (ZH)**: 《醫療級 LSR 液態矽膠呼吸面罩配件：高品質與精密的量產實踐》
* **Title (EN)**: 《Medical-Grade LSR Liquid Silicone Respiratory Mask Components: High-Quality and Precision Mass Production Practice》
* **Title (JA)**: 《医療用LSR液状シリコーン製呼吸マスク部品：高品質と精密成形における量産化の実績》
* **Category**: `case`
* **Key Topics**: Medical grade silicone, FDA compliance, LSR injection molding, Clean room standards.

### 7. 車載高精密防水插座 (Case Study)
* **Anchor ID / ID**: `automotive-waterproof-connector`
* **Title (ZH)**: 《車載高精密防水插座：LSR 雙色包膠 (Overmolding) 代工合作案》
* **Title (EN)**: 《Automotive High-Precision Waterproof Connectors: LSR Double-Shot Overmolding Custom Case Study》
* **Title (JA)**: 《車載用高精密防水ソケット：LSR 2色成形 (Overmolding) 受託製造事例》
* **Category**: `case`
* **Key Topics**: Automotive connectors, IP69K waterproof, Dual-shot overmolding, PA66 + LSR.

### 8. 工業重載避震腳墊 (Case Study)
* **Anchor ID / ID**: `industrial-vibration-pad`
* **Title (ZH)**: 《工業重載避震腳墊（矽膠包鐵件）：優化高撕裂強度物理黏合性能》
* **Title (EN)**: 《Industrial Heavy-Duty Anti-Vibration Pads (Rubber-to-Metal Bonding): Optimizing Physical Adhesion with High Tear Strength》
* **Title (JA)**: 《產業用重荷重防振ゴム脚（金属焼付接着）：高引き裂き強度と物理的接着性能の最適化》
* **Category**: `case`
* **Key Topics**: Heavy-duty machinery, Metal-to-rubber bonding, High tear strength, EPDM/NBR.

### 10. 自黏型液態矽膠（Self-Bonding LSR）射出成型技術指南
* **Anchor ID / ID**: `self-bonding-lsr-guide`
* **Title (ZH)**: 《自黏型液態矽膠（Self-Bonding LSR）射出成型技術指南：免底膠一體成型全解析》
* **Title (EN)**: 《Self-Bonding LSR Injection Molding Guide: Primerless Overmolding & Multi-Material Bonding Technology》
* **Title (JA)**: 《自己接着性LSR（Self-Bonding LSR）射出成形技術ガイド：プライマーレス一体成形全解析》
* **Category**: `tech`
### 11. 專業矽膠廠與矽膠代工廠選型指南
* **Anchor ID / ID**: `silicone-factory-guide`
* **Title (ZH)**: 《如何選擇專業矽膠廠與矽膠代工廠？從模具開發、LSR射出到品質檢驗全解析》
* **Title (EN)**: 《How to Choose a Professional Silicone Factory & OEM Manufacturer?》
* **Title (JA)**: 《専門的なシリコーン工場・シリコーンOEMメーカーの選定ガイド》
* **Category**: `tech`
* **Key Topics**: Silicone factory, Silicone OEM manufacturer, Solid compression molding vs LSR injection, Tooling cost.

### 12. 橡膠廠與橡膠代工廠採購指南
* **Anchor ID / ID**: `rubber-factory-guide`
* **Title (ZH)**: 《橡膠廠與橡膠代工廠採購指南：EPDM、NBR、Viton 材料選型與異材結合技術全解析》
* **Title (EN)**: 《Rubber Factory & OEM Manufacturer Procurement Guide: EPDM, NBR, Viton》
* **Title (JA)**: 《ゴム工場・ゴムOEM受託製造メーカー調達ガイド：EPDM、NBR、Viton》
* **Category**: `tech`
### 13. LSR液態矽膠全解析指南
* **Anchor ID / ID**: `lsr-liquid-silicone`
* **Title (ZH)**: 《LSR液態矽膠是什麼？液態矽膠射出成型製程、特性與客製化應用全解析》
* **Title (EN)**: 《What is LSR? Liquid Silicone Rubber Injection Molding, Properties & Custom Applications》
* **Title (JA)**: 《LSR（液状シリコーンゴム）とは？液状シリコーン射出成形、材料特性、カスタム応用まで徹底解説》
* **Category**: `tech`
* **Key Topics**: LSR, 液態矽膠射出, 雙色包膠, 醫療級矽膠, 川連精密射出.

### 14. 台灣 LSR 液態矽膠射出工廠選型指南
* **Anchor ID / ID**: `lsr-silicone-supplier-taiwan`
* **Title (ZH)**: 《台灣 LSR 液態矽膠射出工廠怎麼選？採購與代工廠評估指南》
* **Title (EN)**: 《How to Choose a Taiwan LSR Liquid Silicone Supplier & OEM Manufacturer?》
* **Title (JA)**: 《台湾LSR液状シリコーン射出成形メーカーの選定ガイド：調達と委託製造の評価基準》
* **Category**: `tech`
* **Key Topics**: LSR 矽膠, LSR 矽膠供應商, 液態矽膠代工廠, 台灣矽膠工廠.

### 15. LSR 液態矽膠 vs. HCR 熱硫化矽膠全方位對比
* **Anchor ID / ID**: `lsr-silicone-vs-hcr`
* **Title (ZH)**: 《LSR 液態矽膠 vs. HCR 熱硫化矽膠：材料特性、模具成本與成型工藝全方位對比》
* **Title (EN)**: 《LSR Liquid Silicone Rubber vs. HCR High Consistency Rubber: Materials, Tooling & Process Comparison》
* **Title (JA)**: 《LSR液状シリコーン vs. HCR熱硫化シリコーン：材料特性・金型コスト・成形工藝徹底比較》
* **Category**: `tech`
* **Key Topics**: LSR 矽膠, HCR 矽膠, 液態矽膠射出, 固態矽膠, 矽膠材料選型.

### 16. 自潤矽膠（出油膠）代工指南
* **Anchor ID / ID**: `self-lubricating-silicone`
* **Title (ZH)**: 《自潤矽膠是什麼？低摩擦出油膠密封件與汽車、醫療代工全解析》
* **Title (EN)**: 《What is Self-Lubricating Silicone? Low-Friction Seals for Automotive & Medical OEM》
* **Title (JA)**: 《自己潤滑性シリコーンとは？低摩擦シール・自潤シリコーン代行製造ガイド（自動車・医療向け）》
* **Category**: `tech`
* **Key Topics**: 自潤矽膠, 出油膠, Self-Lubricating Silicone, 低摩擦密封件, 汽車線束防水插塞, 醫療注射器密封件, HCR 熱固壓縮成型.

### 17. 矽膠包金屬異材結合代工指南
* **Anchor ID / ID**: `silicone-overmolding-bonding`
* **Title (ZH)**: 《矽膠包金屬代工（矽膠包鐵/鋁/銅件）：模具機械咬合、防溢膠與抗拉拔測試實務》
* **Title (EN)**: 《Silicone-to-Metal Bonding OEM (Iron/Aluminum/Copper): Mechanical Interlocking & Anti-Flash Tooling》
* **Title (JA)**: 《シリコーン金属焼き付け・インサート成形受託（鉄・アルミ・銅）：機械的アンカー効果とバリ防止金型実務》
* **Category**: `tech`
* **Key Topics**: 異材結合, 矽膠包金屬, 矽膠包鐵, 矽膠包鋁, 機械倒扣咬合, 模具防溢膠, 抗拉拔測試, ISO 9001.

### 18. 汽車與工業線束防水塞代工指南
* **Anchor ID / ID**: `automotive-wire-harness-seals`
* **Title (ZH)**: 《汽車與工業線束防水塞代工：自潤矽膠（出油膠）配方與模具開發實務》
* **Title (EN)**: 《Automotive & Industrial Wire Harness Seals OEM: Self-Lubricating Silicone Molding》
* **Title (JA)**: 《自動車・産業用ワイヤーハーネス防水プラグ受託製造：自己潤滑シリコーン配合と金型設計実務》
* **Category**: `tech`
* **Key Topics**: 線束防水塞, 自潤矽膠, 出油膠, Single Wire Seal, 穿孔插拔阻力, 多穴模具, ISO 9001.

### 19. 大劑量 LSR 液態矽膠射出成型代工指南
* **Anchor ID / ID**: `large-shot-lsr-molding`
* **Title (ZH)**: 《大劑量 LSR 液態矽膠射出成型代工：大克重、厚件製品防氣泡與模具開發實務》
* **Title (EN)**: 《Large-Shot LSR Liquid Silicone Injection Molding OEM: Thick-Wall & High-Weight Parts》
* **Title (JA)**: 《大容量 LSR 液状シリコーン射出成形受託製造：大重量・厚肉成形品の気泡対策と金型設計実務》
* **Category**: `tech`
* **Key Topics**: 大劑量射出, LSR厚件射出, 液態矽膠射出, 模具排氣, 真空抽氣, 大克重成型, ISO 9001.

---

## 🤖 SEO Content Copilot 工作流程

當使用者說「幫我以 [關鍵字] 生成 SEO 文章」或類似語句時，請依照以下步驟執行。**每一步都必須完成，不可跳過。**

---

### 執行步驟

#### STEP 1：競品搜尋分析
使用 `search_web` 工具，以使用者提供的關鍵字進行搜尋。
- 搜尋語言：繁體中文版本使用繁中關鍵字搜尋，同時搜尋英文和日文版本
- 目標：找出前 5 名競品的標題結構、涵蓋主題、使用者常見問題 (People Also Ask)
- 記錄競品使用的 H2 標題關鍵字（用於生成文章大綱）

#### STEP 2：防重複比對
比對以下已發布的文章 Slug 清單，確保新主題不與任何現有文章重複：
```
ai-server-drone, automotive-waterproof-connector, conductive-keypad,
food-grade-silicone-fda, industrial-vibration-feet, industrial-vibration-pad,
medical-lsr-mask, oring-seal-custom-mold, semiconductor-silicone-seal,
shore-hardness-guide, silicone-overmolding, solid-vs-lsr,
uav-silicone-parts, viton-vs-fvmq, self-bonding-lsr-guide, lsr-liquid-silicone,
lsr-silicone-supplier-taiwan, lsr-silicone-vs-hcr, self-lubricating-silicone,
silicone-overmolding-bonding, automotive-wire-harness-seals,
large-shot-lsr-molding
```
若主題重複，告知使用者並建議替代角度，不要繼續生成。

#### STEP 3：決定文章 Slug 與標題
- 依照「知識庫文章 URL 命名規範」生成英文 slug（全小寫、連字號分隔）
- 格式：`knowledge-[slug].html`
- 同時確定三語標題（繁中 / 英文 / 日文）

#### STEP 4：生成三語 HTML 文章頁面
讀取以下三個樣板檔案，以樣板為基礎替換所有 `{{PLACEHOLDER}}` 變數，分別生成三個 HTML 檔案：

| 語言 | 樣板路徑 | 輸出路徑 |
|------|---------|---------|
| 繁中 | `p:\tets\.agents\skills\website_seo\templates\article_template_zh.html` | `p:\tets\knowledge-[slug].html` |
| 英文 | `p:\tets\.agents\skills\website_seo\templates\article_template_en.html` | `p:\tets\en\knowledge-[slug].html` |
| 日文 | `p:\tets\.agents\skills\website_seo\templates\article_template_ja.html` | `p:\tets\ja\knowledge-[slug].html` |

**內容生成規範**：
- 文章必須包含 6～8 個主要段落（H2 或 article-section）
- 每段落至少 150 字
- 必須包含：前言、技術解析（2～3段）、應用場景、選型建議、FAQ（至少 3 題）、結尾 CTA
- 術語必須使用鈞翔實業的專業優勢（LSR液態射出、矽膠包膠、FDA醫療級、Viton/FVMQ耐油、ISO認證）
- 繁中版本 META description 120-160 字元
- 英文版本 META description 120-160 characters
- 日文版本 META description 適當長度

#### STEP 5：更新 sitemap.xml
在 `p:\tets\sitemap.xml` 的 `</urlset>` 標籤**之前**，插入以下格式的三語 URL 條目（以今天日期替換 `YYYY-MM-DD`）：

```xml
   <url>
      <loc>https://www.jun-hsiang.com.tw/knowledge-[slug].html</loc>
      <lastmod>YYYY-MM-DD</lastmod>
      <changefreq>monthly</changefreq>
      <priority>0.8</priority>
      <xhtml:link rel="alternate" hreflang="zh-TW" href="https://www.jun-hsiang.com.tw/knowledge-[slug].html"/>
      <xhtml:link rel="alternate" hreflang="en" href="https://www.jun-hsiang.com.tw/en/knowledge-[slug].html"/>
      <xhtml:link rel="alternate" hreflang="ja" href="https://www.jun-hsiang.com.tw/ja/knowledge-[slug].html"/>
   </url>
```

#### STEP 6：更新 SKILL.md 文章資料庫
在本 SKILL.md 的「Published Article Database」章節末尾，以相同格式新增新文章的記錄項目，包含：
- 編號（現有最大號碼 +1）
- Anchor ID / ID
- Title (ZH)、Title (EN)、Title (JA)
- Category（tech 或 case）
- Key Topics

#### STEP 7：完成報告
向使用者回報：
- ✅ 已建立的 3 個 HTML 檔案路徑
- ✅ sitemap.xml 已更新
- ✅ 已更新文章資料庫
- ⚠️ 提醒使用者手動確認 `knowledge.html` 三語版本的文章卡片是否需要插入（可參考 `templates/knowledge_card_template.html` 樣板）

---

### SEO 規範自我驗證 Checklist（在輸出每個 HTML 檔案前必須逐項確認）

```
[ ] <title> 品牌名稱正確（繁中：鈞翔實業 / EN：Jun-Hsiang Enterprise / 日文：鈞翔実業）
[ ] <meta charset="utf-8"> 存在
[ ] <meta name="viewport"> 存在
[ ] <meta name="description"> 已填寫，字數 120-160 字元
[ ] <link rel="canonical" href="https://www.jun-hsiang.com.tw/[該頁完整路徑]"/>
[ ] <meta property="og:url" content="..."/> 與 canonical 相同
[ ] <link rel="alternate" hreflang="zh-TW" href="..."/> 繁中對應 URL
[ ] <link rel="alternate" hreflang="en" href="..."/> 英文對應 URL
[ ] <link rel="alternate" hreflang="ja" href="..."/> 日文對應 URL
[ ] <link rel="alternate" hreflang="x-default" href="..."/> 指向繁中 URL
[ ] 頁面 <head> 內沒有任何 window.location.href 自動重定向腳本
[ ] JSON-LD @id 和 url 欄位指向正確文章 URL（非 knowledge.html）
[ ] JSON-LD inLanguage 與頁面語言一致（zh-TW / en / ja）
```

