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
silicone-manufacturer-guide
silicone-overmolding
solid-vs-lsr
uav-silicone-parts
viton-vs-fvmq
```
（此清單同時維護於 `.agents/skills/website_seo/SKILL.md`）
