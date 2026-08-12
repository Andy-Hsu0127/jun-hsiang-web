# LSR SEO 優化待辦事項（Backlog）
*記錄日期：2026-07-16*
*狀態：待執行 - 適合由 AI 代理人批次完成*

---

## 背景說明

鈞翔實業官網（https://www.jun-hsiang.com.tw）目前 LSR 液態矽膠射出相關關鍵字排名在第 2 頁。
本文件記錄尚未完成的站內 SEO 優化任務，所有任務均為純程式碼修改，無需人工撰稿。

---

## 已完成（不需再做）

| 項目 | 完成日期 |
|---|---|
| LocalBusiness Schema 已存在於首頁 | 已在 index.html L117 |
| 首頁加入可見 FAQ 問答區塊 + FAQPage Schema | 2026-07-16 |
| knowledge-solid-vs-lsr.html 新增 FAQPage Schema | 2026-07-16 |
| service.html 加入延伸閱讀內鏈 | 2026-07-16 |
| 全站清除「0.03mm」與「0.05mm」等具體公差數字 | 2026-07-16 |
| knowledge-medical-lsr-mask.html 修正「無塵無污染」錯誤描述 | 2026-07-16 |
| 首頁 LSR 服務標題優化為含代工關鍵字 | 2026-07-16 |
| 中英日三語文章 CTA 按鈕 anchor 文字優化 | 2026-07-16 |

---

## 待執行任務一：products_list.html 新增可見 LSR 靜態介紹段落

### 問題說明
目前 products_list.html 中 LSR 產品的描述文字藏在 HTML data-desc 屬性內，由 JavaScript 動態顯示。
Google 對 data-* 屬性的索引權重極低。此任務目的是在 LSR 產品卡片群組的正上方加入一段實體可見的 HTML 靜態說明段落。

### 插入位置定位邏輯
1. 開啟 products_list.html
2. 搜尋第一個含有 LSR 字樣的 product-card 的父層容器（class="products-grid" 或類似）
3. 在第一個 LSR product-card 的正上方插入下方 HTML 區塊
4. 對 en/products_list.html 與 ja/products_list.html 執行相同邏輯（使用對應語言版本）
5. 完成後執行 git add, git commit -m "seo(products): add visible static LSR intro block to products_list pages", git push

### 繁體中文版插入 HTML
插入在第一個含 LSR 的 product-card 正上方：

<div class="lsr-intro-block" style="max-width: 720px; margin: 0 auto var(--space-8) auto; text-align: center; padding: 0 var(--space-4);">
  <h2 style="font-size: 1.3rem; font-weight: 700; color: var(--color-text-primary); margin-bottom: var(--space-3);">LSR 液態矽膠射出成型代工產品</h2>
  <p style="color: var(--color-text-secondary); font-size: 0.95rem; line-height: 1.8;">鈞翔實業提供 LSR 液態矽膠射出成型客製代工服務，適用於醫療器材密封件、精密電子防水圈、汽車防水插座密封件等高精度需求。我們以封閉式自動化製程確保製品品質穩定，並通過 ISO 9001 認證。如需 LSR 客製開模報價，歡迎填寫詢價表單聯繫我們。</p>
  <a href="service.html" style="display: inline-flex; align-items: center; gap: 8px; margin-top: var(--space-4); text-decoration: none; font-weight: 600; font-size: 0.9rem; padding: 10px 22px; background: var(--color-accent); color: #fff; border-radius: 4px;">了解 LSR 液態矽膠射出服務 →</a>
</div>

### 英文版插入 HTML（en/products_list.html）
<div class="lsr-intro-block" style="max-width: 720px; margin: 0 auto var(--space-8) auto; text-align: center; padding: 0 var(--space-4);">
  <h2 style="font-size: 1.3rem; font-weight: 700; color: var(--color-text-primary); margin-bottom: var(--space-3);">LSR Liquid Silicone Rubber Injection Molding Products</h2>
  <p style="color: var(--color-text-secondary); font-size: 0.95rem; line-height: 1.8;">Jun-Hsiang Enterprise provides custom LSR liquid silicone rubber injection molding OEM services, suitable for medical device seals, precision electronic waterproof O-rings, and automotive waterproof connector seals. ISO 9001 certified. Contact us for custom LSR tooling quotations.</p>
  <a href="../service.html" style="display: inline-flex; align-items: center; gap: 8px; margin-top: var(--space-4); text-decoration: none; font-weight: 600; font-size: 0.9rem; padding: 10px 22px; background: var(--color-accent); color: #fff; border-radius: 4px;">Learn about LSR Injection Molding Services →</a>
</div>

### 日文版插入 HTML（ja/products_list.html）
<div class="lsr-intro-block" style="max-width: 720px; margin: 0 auto var(--space-8) auto; text-align: center; padding: 0 var(--space-4);">
  <h2 style="font-size: 1.3rem; font-weight: 700; color: var(--color-text-primary); margin-bottom: var(--space-3);">LSR 液状シリコーンゴム射出成形・受託製造製品</h2>
  <p style="color: var(--color-text-secondary); font-size: 0.95rem; line-height: 1.8;">鈞翔実業はLSR液状シリコーンゴム射出成形の受託製造サービスを提供しています。医療機器用シール、精密電子機器防水Oリング、車載防水コネクターシール等の高精度用途に対応。ISO 9001認証取得済み。カスタム金型見積はフォームよりご連絡ください。</p>
  <a href="../service.html" style="display: inline-flex; align-items: center; gap: 8px; margin-top: var(--space-4); text-decoration: none; font-weight: 600; font-size: 0.9rem; padding: 10px 22px; background: var(--color-accent); color: #fff; border-radius: 4px;">LSR液状シリコーンゴム射出サービスの詳細 →</a>
</div>

---

## 待執行任務二：全站圖片 ALT 文字優化

### ALT 替換清單（全站三語版本均適用）

原始值 -> 替換值：
1. alt="液態矽膠射出技術 LSR" -> alt="LSR 液態矽膠射出成型機台生產現場 - 鈞翔實業 新北新莊精密矽橡膠代工廠"
2. alt="川連機械液態矽膠射出成型機" -> alt="川連機械精密 LSR 液態矽膠射出成型機 - 鈞翔實業"
3. alt="固態矽膠壓出技術" -> alt="固態矽膠真空熱壓成型製程 - 鈞翔實業 固態矽膠橡膠代工廠"
4. alt="2.5D 投影量測儀" -> alt="2.5D 光學投影量測儀 精密品管檢測 - 鈞翔實業 ISO 9001 認證"
5. alt="Chuan-Lien LSR Liquid Silicone Rubber Injection Molding Machine" -> alt="Chuan-Lien Precision LSR Liquid Silicone Rubber Injection Machine - Jun-Hsiang Enterprise Custom OEM Factory"
6. alt="LSR Liquid Silicone Rubber Injection Molding Technology" -> alt="LSR Liquid Silicone Rubber Injection Molding - Jun-Hsiang Enterprise OEM Factory, Xinzhuang, New Taipei"
7. alt="液狀シリコーンゴム射出成形技術 LSR" -> alt="LSR 液状シリコーンゴム射出成形設備 - 鈞翔実業 新北市新荘区精密シリコーン受託製造工場"

### 操作邏輯
1. 用 Python 腳本對全站根目錄、/en/、/ja/ 下的 HTML 檔案批次執行 str.replace
2. 完成後 git commit -m "seo(images): optimize alt text for LSR equipment and product images" 並 push

---

## 重要注意事項

- 禁止在任何頁面 head 中新增 window.location.href 自動轉向腳本
- 品牌名稱：繁中 = 鈞翔實業 / EN = Jun-Hsiang Enterprise / 日文 = 鈞翔実業
- 所有修改完成後須執行 git push origin main
- 禁止加入任何具體公差數字（如 0.03mm、0.05mm）
