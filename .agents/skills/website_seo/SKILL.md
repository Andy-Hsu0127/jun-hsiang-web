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

### 4. 異材結合技術（矽膠包塑膠與金屬）
* **Anchor ID / ID**: `silicone-overmolding`
* **Title (ZH)**: 《矽膠包塑膠與金屬（異材結合）：如何確保緊密黏合、絕不脫膠的關鍵技術》
* **Title (EN)**: 《Silicone Overmolding on Plastics and Metals (Multi-Material Bonding): Key Technologies to Ensure Tight Adhesion without Delamination》
* **Title (JA)**: 《シリコーンのプラスチック・金属インサート成形（異材結合）：強固な密着を確保し、剥離を防ぐための核心技術》
* **Category**: `tech`
* **Key Topics**: Overmolding, Insert molding, Primer adhesion, Physical anchor effect.

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

### 9. 極端耐油與化學溶劑環境下的特種橡膠選擇
* **Anchor ID / ID**: `viton-vs-fvmq`
* **Title (ZH)**: 《極端耐油與化學溶劑環境下的特種橡膠選擇：氟橡膠（Viton）與氟矽橡膠（FVMQ）性能與應用對比》
* **Title (EN)**: 《Selecting Specialty Elastomers for Extreme Oil and Chemical Solvent Environments: Viton (FKM) vs. Fluorosilicone (FVMQ)》
* **Title (JA)**: 《極端な耐油・化学溶劑環境における特殊ゴムの選定：フッ素ゴム（Viton）とフルオロシリコーン（FVMQ）の特性と応用比較》
* **Category**: `tech`
* **Key Topics**: Viton, FKM, FVMQ, Fluorosilicone, Chemical resistance, Rubber-to-metal bonding.
