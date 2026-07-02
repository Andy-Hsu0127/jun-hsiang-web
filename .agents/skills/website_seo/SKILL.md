---
name: website_seo
description: Manage the website's SEO strategy, technical content generation, and article database to prevent duplicate topics.
---

# Website SEO Content & Article Database

This skill manages the SEO content writing workflow and maintains a historical list of all technical articles published on the Jun-Hsiang website (`index.html`, `knowledge.html`, etc.) in Traditional Chinese, English, and Japanese.

## Technical Article Guidelines
When writing or generating new technical articles for the website:
1. **No Duplication**: Always consult the **Published Article Database** below. Do NOT write about a topic, material, or application that is already heavily covered.
2. **Format**: Articles must be formatted as `<article class="article-card" data-category="[tech|case]" data-tags="[tag1,tag2,...]">` HTML structures compatible with the custom JS filter in `knowledge.html`.
3. **Multi-language**: Every new article must be written in **Traditional Chinese**, **English**, and **Japanese**, and inserted at the top of the respective `knowledge.html` files.
4. **Clean Code & No Cache Collapsing**: Ensure the click event listener in the script is preserved so that clicking inside `.article-expanded-content` does not collapse the card.
5. **No "全自動" (Fully Automatic) wording**: Avoid "全自動" or "自動" in equipment/machinery descriptions unless specifically approved.

---

## Published Article Database

### 1. 無人機精密矽橡膠零件設計指南
* **Title (ZH)**: 《無人機精密矽橡膠零件設計指南：避震球、防水圈與起落架避震結構材料全解析》
* **Title (EN)**: 《UAV Precision Silicone & Rubber Components Design Guide: Vibration Dampers, Waterproof Rings, and Landing Gear Shock Absorption》
* **Title (JA)**: 《ドローン精密シリコーン・ゴム部品の設計ガイド：防振ボール、防水リング、および着陸装置用衝撃吸収システム材料解析》
* **Category**: `tech`
* **Key Topics**: Drones, Vibration Dampers (Gimbal balls), Waterproof O-rings, NBR, LSR, PU.

### 2. AI 伺服器與無人機關鍵應用
* **Title (ZH)**: 《AI 伺服器與無人機的崛起：高階精密矽橡膠零件的關鍵應用與設計趨勢》
* **Title (EN)**: 《The Rise of AI Servers and UAVs: Critical Applications and Design Trends of High-End Precision Silicone Rubber Parts》
* **Title (JA)**: 《AIサーバーとドローン産業の台頭：高付加價值精密シリコーン・ゴム部品の重要応用と設計トレンド》
* **Category**: `tech`
* **Key Topics**: AI Servers, GPU cooling, Liquid cooling gaskets, Thermal Conductive Silicone (TIM), EMI shielding.

### 3. 固態熱壓與 LSR 液態射出製程對比
* **Title (ZH)**: 《固態矽膠熱壓 vs. LSR 液態矽膠射出：如何選擇最適合的客製化製程？》
* **Title (EN)**: 《Solid Compression Molding vs. LSR Liquid Injection Molding: How to Choose the Best Custom Process?》
* **Title (JA)**: 《固形シリコーンゴム熱プレス vs. LSR液状シリコーンゴム射出成形：最適なカスタム製程の選定方法とは？》
* **Category**: `tech`
* **Key Topics**: Solid compression molding, LSR liquid injection molding, Tooling cost, Precision tolerances.

### 4. 異材結合技術（矽膠包塑膠與金屬）
* **Title (ZH)**: 《矽膠包塑膠與金屬（異材結合）：如何確保緊密黏合、絕不脫膠的關鍵技術》
* **Title (EN)**: 《Silicone Overmolding on Plastics and Metals (Multi-Material Bonding): Key Technologies to Ensure Tight Adhesion without Delamination》
* **Title (JA)**: 《シリコーンのプラスチック・金属インサート成形（異材結合）：強固な密着を確保し、剥離を防ぐための核心技術》
* **Category**: `tech`
* **Key Topics**: Overmolding, Insert molding, Primer adhesion, Physical anchor effect.

### 5. 導電矽膠按鍵設計指南
* **Title (ZH)**: 《導電矽膠按鍵設計指南：電阻、行程與橡膠彈力規格全面解析》
* **Title (EN)**: 《Conductive Silicone Keypad Design Guide: In-Depth Analysis of Resistance, Travel, and Rubber Tactile Force Specifications》
* **Title (JA)**: 《導電性シリコンキーパッド設計ガイド：電気抵抗、キーストローク、およびゴム弾性仕様の徹底解説》
* **Category**: `tech`
* **Key Topics**: Conductive keypads, Contact resistance, Travel distance, Actuation force (click ratio).

### 6. 醫療級 LSR 液態矽膠呼吸面罩配件 (Case Study)
* **Title (ZH)**: 《醫療級 LSR 液態矽膠呼吸面罩配件：高品質與精密的量產實踐》
* **Title (EN)**: 《Medical-Grade LSR Liquid Silicone Respiratory Mask Components: High-Quality and Precision Mass Production Practice》
* **Title (JA)**: 《医療用LSR液状シリコーン製呼吸マスク部品：高品質と精密成形における量産化の実績》
* **Category**: `case`
* **Key Topics**: Medical grade silicone, FDA compliance, LSR injection molding, Clean room standards.

### 7. 車載高精密防水插座 (Case Study)
* **Title (ZH)**: 《車載高精密防水插座：LSR 雙色包膠 (Overmolding) 代工合作案》
* **Title (EN)**: 《Automotive High-Precision Waterproof Connectors: LSR Double-Shot Overmolding Custom Case Study》
* **Title (JA)**: 《車載用高精密防水ソケット：LSR 2色成形 (Overmolding) 受託製造事例》
* **Category**: `case`
* **Key Topics**: Automotive connectors, IP69K waterproof, Dual-shot overmolding, PA66 + LSR.

### 8. 工業重載避震腳墊 (Case Study)
* **Title (ZH)**: 《工業重載避震腳墊（矽膠包鐵件）：優化高撕裂強度物理黏合性能》
* **Title (EN)**: 《Industrial Heavy-Duty Anti-Vibration Pads (Rubber-to-Metal Bonding): Optimizing Physical Adhesion with High Tear Strength》
* **Title (JA)**: 《産業用重荷重防振ゴム脚（金属焼付接着）：高引き裂き強度と物理的接着性能の最適化》
* **Category**: `case`
* **Key Topics**: Heavy-duty machinery, Metal-to-rubber bonding, High tear strength, EPDM/NBR.
