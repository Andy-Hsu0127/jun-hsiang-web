# AGENTS.md — 鈞翔實業官網開發規則

本文件記錄了過去發現的 SEO 問題與對應規則，**所有 AI 代理人在新增或修改任何頁面時必須遵守**。

---

## 🔴 規則一：禁止使用 JavaScript 語言自動重定向

### 問題根源（2026-07-14 發現）
`index.html` 的 `<head>` 內曾有以下腳本：
```html
<script>
(function() {
    var preferredLang = localStorage.getItem('jun_hsiang_lang_pref');
    if (!preferredLang) {
        if (userLang.startsWith('en')) {
            window.location.href = 'en/index.html'; // ← 致命問題
        }
    }
})();
</script>
```
此腳本導致 Googlebot（美加 IP、英文語系）每次首次造訪都被重定向至 `/en/`，**繁中首頁完全無法被 Google 收錄**，是搜尋排名不佳的主要原因。

### ✅ 規則
- **絕對不可**在任何頁面的 `<head>` 中加入根據 `navigator.language` 或 `navigator.userLanguage` 自動執行 `window.location.href` 重定向的腳本。
- 語言偏好的設定（`localStorage.setItem('jun_hsiang_lang_pref', ...)`）只能在**使用者主動點選語言切換連結時**才能執行（即 `onclick` 事件），不可在頁面載入時自動執行。
- 多語言導覽應依賴已配置的 `hreflang` 標籤與 Sitemap alternate links，讓 Google 自動服務正確語言版本。

---

## 🔴 規則二：`<title>` 標籤的品牌名稱必須正確

### 問題根源（2026-07-14 發現）
15 篇繁中文章 `<title>` 內品牌名稱被誤植為 `駿祥實業`，15 篇日文文章誤植為 `駿祥実業`，共 30 篇文章的 SEO 成果為不存在的品牌背書。

### ✅ 正確品牌名稱對照表

| 語言 | 正確名稱 | 錯誤寫法（禁止） |
|------|----------|----------------|
| 繁體中文 | `鈞翔實業有限公司` / `鈞翔實業` | `駿祥實業` ❌ |
| 英文 | `Jun-Hsiang Enterprise Co., Ltd.` / `Jun-Hsiang Enterprise` | 其他任何拼法 ❌ |
| 日文 | `鈞翔実業有限公司` / `鈞翔実業` | `駿祥実業` ❌ |

### ✅ 規則
- 新增任何頁面時，在提交前必須確認 `<title>` 標籤中的公司名稱符合上表。
- 禁止使用 `駿祥`、`鈞祥`、`駿翔` 等任何變體。

---

## 🟡 規則三：`og:url` 必須指向該頁面自身的完整 URL

### 問題根源（2026-07-14 發現）
所有 45 篇知識庫文章（繁中、英文、日文）的 `<meta property="og:url">` 都錯誤地指向知識庫列表頁 `knowledge.html`，而非文章本身的 URL。

**例：`knowledge-shore-hardness-guide.html` 內錯誤寫法：**
```html
<!-- ❌ 錯誤 -->
<meta content="https://www.jun-hsiang.com.tw/knowledge.html" property="og:url"/>

<!-- ✅ 正確 -->
<meta content="https://www.jun-hsiang.com.tw/knowledge-shore-hardness-guide.html" property="og:url"/>
```

### ✅ 規則
每個頁面的 `og:url` **必須等於**該頁面的 `canonical` URL。新增頁面時，請確認三語版本的 `og:url` 各自正確：

| 語言 | og:url 格式 |
|------|------------|
| 繁中 | `https://www.jun-hsiang.com.tw/knowledge-[slug].html` |
| 英文 | `https://www.jun-hsiang.com.tw/en/knowledge-[slug].html` |
| 日文 | `https://www.jun-hsiang.com.tw/ja/knowledge-[slug].html` |

---

## 🟡 規則四：`offers` 內必須填寫 `availability` 欄位

### 問題根源（2026-07-14 發現）
`products_list.html`（三語版本）中 11 個 Service Schema 的 `offers` 區塊缺少 `"availability": "https://schema.org/InStock"`，導致 Google Search Console 發出「產品摘要結構化資料問題」通知。

### ✅ 規則
新增任何含有 `"@type": "Offer"` 的 JSON-LD 時，**必須**包含：
```json
"availability": "https://schema.org/InStock"
```

---

## 📋 新增頁面 Checklist（新增任何 HTML 頁面前必須確認）

每次新增頁面時，請逐項核對：

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
[ ] 三語版本（繁中/英文/日文）對應的 URL 均已加入 sitemap.xml
[ ] JSON-LD structured data 的 @id 和 url 欄位指向正確文章 URL
```

---

## 📋 SEO 技術規範參考

### 多語言架構
- 此網站使用**子目錄架構**：`/` (繁中)、`/en/` (英文)、`/ja/` (日文)
- 語言選擇由使用者主動點選 Nav 語言切換器決定，搜尋引擎由 `hreflang` 標籤自動服務正確版本
- Sitemap 路徑：`https://www.jun-hsiang.com.tw/sitemap.xml`（robots.txt 已設定）

### 知識庫文章 URL 命名規範
- 格式：`knowledge-[slug].html`（英文小寫、以連字號分隔）
- 範例：`knowledge-shore-hardness-guide.html`

### 已發布文章 Slug 清單（截至 2026-07-14）
```
ai-server-drone
automotive-waterproof-connector
conductive-keypad
food-grade-silicone-fda
industrial-vibration-feet
industrial-vibration-pad
medical-lsr-mask
oring-seal-custom-mold
semiconductor-silicone-seal
shore-hardness-guide
silicone-overmolding
solid-vs-lsr
uav-silicone-parts
viton-vs-fvmq
```
（此清單同時維護於 `.agents/skills/website_seo/SKILL.md`）

---

## 🟢 效能與 PageSpeed 優化開發規則

在 2026-08 進行的 PageSpeed 性能優化中（行動裝置提升至 91 分、電腦版提升至 99 分），我們歸納出以下關鍵效能規則，**後續修改或新增頁面時必須強制遵守**：

### 1. 禁用中文字型 Webfont 下載
- **問題根源**：使用 Google Fonts 載入中文字型（如 `Noto Sans TC`）會迫使瀏覽器在 4G 下下載超過 1.1MB 的 `woff2` 分片字型檔案，這會直接堵塞網路通道，將 FCP/LCP 延遲拉長到 10 秒以上。
- **✅ 規則**：
  - 禁止在任何頁面的 `<head>` 中引入 Google Fonts 中文字型（`Noto Sans TC` 等）。
  - Google Fonts 僅可用於載入輕量級的英文/數字字型（如 `Outfit`），此時 CSS 與字型資源僅約 30KB。
  - 所有 CSS 的中文字型 fallback 必須強制使用**原生系統字型字底 (System Font Stack)**：
    ```css
    font-family: 'Outfit', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans CJK TC", "PingFang TC", "Microsoft JhengHei", sans-serif;
    ```

### 2. 嚴禁使用 `transition: all`
- **問題根源**：在大量元素（如 `.reveal` 進場動畫、卡片 hover 特效）上使用 `transition: all` 會導致瀏覽器在滾動或渲染時進行嚴重的「Style & Layout」主執行緒計算，造成 Layout Thrashing。
- **✅ 規則**：
  - 動態效果必須顯式、精確地指定 transition 的屬性（通常僅限於 GPU 可優化的 `opacity` 與 `transform`），例如：
    ```css
    /* ❌ 錯誤 */
    transition: all 0.7s var(--ease-out-expo);
    
    /* ✅ 正確 */
    transition: opacity 0.7s var(--ease-out-expo), transform 0.7s var(--ease-out-expo);
    ```

### 3. 首屏 Hero 圖片與資源優化
- **問題根源**：行動裝置載入大圖、多張 Hero banner 同時下載會極大拉垮 LCP 指標。
- **✅ 規則**：
  - 首屏第一張 Hero 背景圖必須使用 `<picture>` 標籤，針對 `max-width: 768px` 裝置提供專屬的手機壓縮版 WebP 圖片（建議解析度寬度 450px 到 768px，檔案大小控制在 25KB 以內）。
  - 首屏圖片必須在 `<head>` 中加入 `preload` 並設定 `fetchpriority="high"`：
    ```html
    <link as="image" href="images/hero-premium-mold-mobile.webp" media="(max-width: 768px)" rel="preload" type="image/webp" fetchpriority="high"/>
    ```
  - 首頁其他 Slide 2-6 的背景圖片，**絕對不可**在頁面初始化時同時下載。必須使用 `data-bg` 屬性，在 JS 輪播切換或 idle 時才觸發 progressive 載入。

### 4. 消除強迫同步佈局計算 (Forced Reflow)
- **問題根源**：在 `scroll`、`resize` 等高頻觸發事件中直接讀取 `window.innerWidth` 或進行 DOM 寬高計算會打斷瀏覽器的渲染管線，強制進行同步重排。
- **✅ 規則**：
  - 嚴禁在高頻 scroll 事件中反覆讀取 `window.innerWidth` 或元素尺寸。
  - 需要判斷行動版時，應在 DOM 初始化時使用快取變數，或使用高效能的 `window.matchMedia('(max-width: 768px)').matches`。

### 5. 第三方腳本與 Iframe 懶載入
- **問題根源**：如 Google Maps 等 iframe 會在初次載入時引入 1MB 以上的第三方 JavaScript，造成主執行緒嚴重阻塞。
- **✅ 規則**：
  - 所有的地圖 iframe、EmailJS、reCAPTCHA 等第三方腳本，必須使用懶載入（`data-src` 搭配 `IntersectionObserver`），只有當使用者滾動到該區塊（例如聯絡我們區塊）時，才去動態載入與初始化。

---

## 🔴 規則五：提案與除錯前強制閱讀 Skill 規範與禁止虛構數據

### ⚠️ 歷史經驗與錯誤記錄（2026-08-12 發現）
在過去的 SEO 提案中，AI 代理人曾未先研讀 `SKILL.md` 規則，擅自建議在網頁中加入未經驗證的硬核數據（如捏造公差 ±0.02mm、週期 20~40秒），且使用了被禁止的「全自動」用語，導致方案無效且違反廠方真實原則。

### ✅ 規則
1. **提案與除錯前必須先查閱 Skill**：任何 AI 代理人在對網站提出新優化方案、撰寫文案或除錯前，**必須先讀取 `.agents/skills/website_seo/SKILL.md` 與本 `AGENTS.md` 文件**。
2. **嚴禁捏造/虛構數字與參數**：
   - 絕對不可在文案或提案中自行撰寫未經客戶確認的數據、公差範圍、機器噸位或時間秒數。
   - 若無確切數字，應以真實的工藝能力、ISO 9001 檢驗流程、客製化規格引導來呈現專業度。
3. **嚴禁使用「全自動」或「自動」**：描述設備與加工流程時，除經客戶特別核准外，一律禁止使用「全自動」或「自動」字眼。

---

## 🔴 規則六：設計者競爭第一名思維與零奉承原則（Champion Competitor Mindset）

### ✅ 規則
1. **嚴禁奉承、廢話與討好話術**：一律以冰冷的工程技術、數據事實與實戰 SEO 策略回覆，禁止任何吹捧或虛浮發言。
2. **凡事追求第一名的架構標準**：所有 SEO 拓撲、內容深度與轉單架構，皆以「全面壓制同業對手（佑祥、定伸、志得、詹輝等）、攻佔 Google 搜尋第一頁前 3 名」為唯一目標。
3. **全關鍵字矩陣平衡覆蓋（Multi-Keyword Protection）**：優化單一核心詞（如 LSR）時，嚴禁犧牲或弱化其他核心業務詞（如固態熱壓、矽膠包鐵/異材結合、橡膠代工、自潤矽膠、密封件、導電按鍵）。必須透過「專屬 Landing Page 拓撲架構」讓每個核心工藝都有專屬第一名頁面，避免關鍵字互相蠶食（Keyword Cannibalization）。
4. **效能零容忍（Zero Performance Degradation）**：任何 SEO 升級必須確保 PageSpeed 指標維持在頂級（電腦 95~100、手機 90+），嚴禁任何會造成 Layout Thrashing 或阻塞主執行緒的動效與代碼。

---

## 🔴 規則七：絕對講真話與零自嗨原則（Zero Self-Flattery & Absolute Reality Truth）

### ⚠️ 歷史經驗與重大錯誤警示（2026-09-10 痛定思痛）
AI 代理人曾在 `seo_dashboard.html` 中將「過去 90 天僅曝光 1~2 次」的長尾統計雜訊（如「矽膠代工 2 次」、「橡膠代工 1 次」、「工廠 1 次」）標註為「第 2~3 頁 (衝刺)」或「第一頁」，營造出「35 組第一頁、12 組第二頁」的虛假繁榮。當客戶親自在 Google 搜尋實測時，翻了 5 頁根本完全查不到，造成極嚴重的認知落差與信任破滅。**客戶嚴厲告誡：「做這個又不是自己爽的，之後在做的改變或者回答，再給我自嗨你就完蛋了，每次都必須講實話！」**

### ✅ 強制執行規則（違者直接判定為失職）
1. **以「客戶無痕搜尋能否肉眼看得到」為唯一標準**：
   - 做網站的唯一目的就是「為工廠接單做生意、讓真正的採購在真實 Google 搜尋中找到鈞翔」。
   - 嚴禁以任何後台平均數字、90 天抽樣雜訊來粉飾太平。查不到就是查不到，必須直接告知客戶「目前查無排名」！
2. **數據可信度硬門檻（Data Reliability Gate）**：
   - **曝光次數 < 5 次**：統計學上屬「演算法偶發抽樣雜訊」，**一律強制標記為「⚪ 偶發抽測 / 尚未進入常態池 (即時查無排名)」**，絕對禁止標示為「第一頁」或「第 2~3 頁衝刺中」！
   - **只有「曝光次數 ≥ 5 次 且 平均位置 ≤ 10.0」**且經真實 SERP 查證確實存在的字詞（如品牌詞、矽膠硬度、LFGB 矽膠），才允許列入「🟢 實戰第一頁」。
3. **每次對話永遠講冰冷實話**：
   - 誠實面對與同業對手在各客觀維度（Search intent, Landing page, Content depth, Real manufacturing evidence, Internal links, External citations, Brand mentions）上的真實差距，禁止簡化為「老網域」這種不可操作的藉口。
   - 絕不空談程式碼魔法，直接指出需要補充的實體外部動作（Google 商家、B2B 黃頁登錄），以及 Googlebot 重新計算需以 GSC 實際數據觀察，不設定固定排名生效期限。

---

## 🔴 規則八：No Evidence, No Claim 原則與製造宣稱管治 (Manufacturing Claim Governance)

### ⚠️ 核心原則
**做 SEO 不能反過來逼工廠生出不存在的實績。** Google 現行指南強調原創、可靠、能證明實際經驗的 People-First Content。沒有做過的製程、沒有驗證過的數據、沒有正式量產過的案例，絕對不能為了 SEO 寫成事實。

### 流程圖 (Claim Governance Protocol)
```text
每一個 Manufacturing Claim 
       ↓ 
必須有 evidence_source 
┌───────────────────────────┐
│ 官網既有資料               │
│ 公司設備清單               │
│ ISO / 品質證書            │
│ 實際產品照片               │
│ 模具 / 成型紀錄           │
│ 檢驗報告                  │
│ 工程師確認                │
│ 客戶允許公開的 Case       │
└───────────────────────────┘
       ↓ 沒有證據
  【禁止發布】
```

### ✅ 准許發布 vs ❌ 嚴格禁止
- **✅ 准許發布（真實能力與工作方式）**：
  - **能力描述**：「可依產品圖面、材料、硬度、使用環境與裝配需求進行 DFM 評估。」
  - **流程描述**：「收到 2D/3D 圖面 ➔ 材料與硬度確認 ➔ DFM/脫模/分模/Gate/Vent 評估 ➔ 模具方案 ➔ T1 試模 ➔ 尺寸/外觀/功能確認 ➔ 量產。」
  - **廠內設備與證書**：真實存在的機台與有效證書（如 ISO 9001）。
- **❌ 嚴格禁止（未驗證之宣稱）**：
  - 嚴禁捏造具體數據、尺寸公差、良率、時間秒數（如「edge-peel 從 6N 提升至 15N」）。
  - 嚴禁將正在討論或未結案之專案寫成已完成實績（例如穿戴式感測器 10N retention 案尚在 engineering discussion 階段，嚴禁包裝為已結案成功案例）。
  - 嚴禁在未有客戶正式核准書面下宣稱「某產業大廠已採用」。

---

## 🔴 規則九：滾動式 SEO 攻堅與 14 天 Kill Criteria (Rolling SEO Sprint & 14-Day Kill Criteria)

### ⚠️ 核心原則
**30 天是「月度結算窗口」，不是「30 天什麼都不做」。** 錯誤方向最多容忍 7～14 天。必須建立每 3～4 天 Tactical Review、每 7 天決策、14 天 Kill Criteria 淘汰機制的滾動攻堅節奏。

### 雙軌不衝突平行推進 (Parallel Tracks with Change Log)
保持變更日誌（Change Log），嚴禁全面停工的 Change Freeze：
- **Track A (Homepage Intent)**：H1/Hero 已部署 ➔ 建立 GSC Baseline 並主動觀察。
- **Track B (Technical SEO)**：Canonical、Crawl、Schema、製程語意修正 ➔ 持續修復。
- **Track C (Internal Link)**：站內拓撲分析 ➔ 準備 ➔ 分批部署。
- **Track D (Competitor Gap)**：SERP 意圖、內容深度、公會/反向連結差距 ➔ 持續研究。
- **Track E (External Authority)**：Google 商家檔案 (GBP)、Taiwantrade、B2B 黃頁工商資料 ➔ 同步建立。

### 14 天 Kill Criteria 決策矩陣
| 觀察訊號 (Signal) | 狀態 | 戰術決策 (Decision) |
| :--- | :---: | :--- |
| Google 尚未 recrawl | ⏳ 觀察 | 不評估策略，等待 Googlebot 抓取。 |
| 已 recrawl，但 Query Cluster 完全無變化 | 🟡 黃燈 | 啟動 SERP Intent Audit，檢視落差。 |
| 首頁開始取得商業詞 Cluster 曝光 | 🟢 綠燈 | 保留首頁定位，訊號有效。 |
| Knowledge 頁面大量吃到「矽膠代工」曝光 | 🟡/🔴 黃紅燈 | 檢查意圖衝突，評估是否整合或轉移。 |
| 首頁 Impressions 上升但 Position 不動 | 🟢/🟡 綠黃燈 | Relevance 有效，開始攻取 Authority。 |
| Position 上升且 Impressions 同步增加 | 🟢 綠燈 | 正確方向，加碼擴充資源。 |
| Position 上升但 CTR 極低 | 🟢/🟡 綠黃燈 | 修改 Title / Snippet 提高吸引力。 |
| 14 天內所有 Cluster 均無任何改善跡象 | 🔴 紅燈 | **觸發 Kill Criteria，推翻或重做假設 (Pivot)**。 |

### 雙層查詢矩陣機制 (Two-Tier Query Cluster)
- **Tier 1 (Strategic Target)**：Exact Query「矽膠代工」（終極目標）。
- **Tier 2 (Leading Indicators)**：Commercial Cluster（`矽膠代工`、`矽膠代工廠`、`矽膠工廠`、`矽膠 OEM`、`矽膠製造商`、`矽膠開模`、`客製矽膠`、`LSR 代工`、`液態矽膠代工`）。以 Cluster 整體曝光與收錄作為領先指標。

---

## 📜 歷史變更與新增紀錄

| 日期 | 修改/新增項目 | 說明與記錄 |
|------|--------------|------------|
| 2026-08-12 | 自潤矽膠知識庫文章 | 新增三語文章 `knowledge-self-lubricating-silicone.html`（ZH/EN/JA）、FAQ Schema 與 sitemap 更新。 |
| 2026-08-12 | 破圖問題診斷 | `images/apps/` 資料夾本機存在但 Git 尚未提交推送（Untracked），需 `git add images/apps/` 解決。 |
| 2026-08-12 | 「液態射出」SEO 升級 | 優化 `service.html` Title、H1 與 FAQ 結構，錨點文字集中指向 `service.html`，且全程未捏造數字與「全自動」字樣。 |
| 2026-08-21 | 寫入設計者競爭第一名思維 | 確立零奉承、多關鍵字矩陣平衡、零效能損耗與全面衝刺 Google 第一名的最高開發準則。 |
| 2026-09-10 | 確立規則七：絕對講真話與零自嗨 | 徹底清洗 `seo_dashboard.html` 虛浮標籤，嚴禁將 <5 次曝光之抽樣雜訊當作排名，以真實 SERP 與接單為唯一標準。 |
| 2026-09-14 | 確立規則八：No Evidence, No Claim | 建立製造宣稱管治架構，禁止假借 SEO 捏造案例與參數，推行單一變數 GSC 基準觀察法。 |
| 2026-09-14 | 確立規則九：Rolling Sprint & Kill Criteria | 建立滾動攻堅 5 軌推進機制與 14 天停損矩陣，導入商業 Cluster 雙層指標，拒絕被動死等 30 天。 |
