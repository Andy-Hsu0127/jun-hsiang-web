# REFACTOR_HANDOFF.md — 鈞翔官網程式碼整理交接文件

> 建立日期：2026-10-13
> 目的：降低「修改後沒生效／找 BUG 耗時」問題。
> 接手的 AI 模型：**開始前必須先讀 `.agents/AGENTS.md` 與 `.agents/skills/website_seo/SKILL.md`**，所有規則（品牌名、禁止自動重定向、禁止 `transition: all`、效能零容忍、禁止 DFM／回覆時限字樣、禁止捏造數據）全部適用。
> 一次只做一個步驟，每步完成後 commit，並向使用者回報實際結果（不可誇大）。

---

## 0. 已查證的現況（2026-10-13 實測，非推測）

- 網站：純靜態 HTML，GitHub Pages 從**repo 根目錄**部署（有 `CNAME`、`.nojekyll`）。**沒有** `package.json`、沒有建置流程。
- 頁面數：根目錄（繁中）33 個 `.html`、`en/` 29 個、`ja/` 29 個。
- 共用資源：
  - `js/main.js`（1,153 行，約 49KB，最後修改 2026-10-12）
  - `js/main.min.js`（約 48KB，最後修改 **2026-08-28**，已過期）
  - `css/style.css`（約 78KB，最後修改 2026-10-12）
  - `css/style.min.css`（約 73KB，最後修改 **2026-08-28**，已過期）
  - 其他：`css/critical.css`、`js/animations.js`、`js/counter.js`、`js/floating-sidebar.js`、`js/particles*.js`、`js/rfq-attribution.js`
- 引用統計：`css/style.css` 69 處、`css/style.min.css` 18 處、`js/main.js` 81 處、`js/main.min.js` 4 處。

### 🔴 核心問題：雙版本漂移
以下頁面引用了**過期的 `.min` 檔**，所以 2026-08-28 之後對 `main.js`／`style.css` 的所有修正（包含 commit `b2d31c0` 語言下拉選單、知識庫文章即時顯示）**在這些頁面上都沒有生效**：

| 頁面 | 引用的過期檔 |
|---|---|
| `index.html`、`en/index.html`、`ja/index.html` | `main.min.js` + `style.min.css` |
| `knowledge-silicone-metal-bonding-failure.html` | `main.min.js` |
| `knowledge-automotive-wire-harness-seals.html`（ZH/EN/JA） | `style.min.css` |
| `knowledge-large-shot-lsr-molding.html`（ZH/EN/JA） | `style.min.css` |
| `knowledge-lsr-liquid-silicone.html`（ZH/EN/JA） | `style.min.css` |
| `knowledge-lsr-silicone-supplier-taiwan.html`（ZH/EN/JA） | `style.min.css` |
| `knowledge-lsr-silicone-vs-hcr.html`（ZH/EN/JA） | `style.min.css` |

`.min` 檔幾乎沒有壓縮效益（只省 1～5KB），保留只會造成漂移風險。

---

## 🚫 禁止事項（先前計劃中已判定錯誤的作法）

1. **禁止**把網站檔案搬到 `site/` 或任何子資料夾 → 會改變全站 URL、破壞 GitHub Pages 部署與 SEO。
2. **禁止**把 `main.js`／`style.css` 拆成多個 `<script>`／`<link>` 分別載入 → 增加 HTTP 請求數，違反 PageSpeed 規則。
3. **禁止**在沒有使用者同意前引入 npm／建置工具。
4. **禁止**變更任何頁面的 `<title>`、`canonical`、`og:url`、`hreflang`、JSON-LD、文案內容（本次只做結構整理）。
5. **禁止**刪除或搬移 git 已追蹤的網站資源（圖片、影片、HTML）。

---

## 步驟 1（最優先）：消除 `.min` 雙版本

1. 在上表所有 HTML 中：
   - `css/style.min.css` → `css/style.css`
   - `js/main.min.js` → `js/main.js`
   - 保留原本的相對路徑前綴（`en/`、`ja/` 頁面可能是 `../css/...`），保留原有屬性（`defer`、`media`、`onload`、`preload` 等），只改檔名。
   - 若 `<head>` 中有 `<link rel="preload" href="...min...">` 也要一起改。
   - 若有 `?v=` 版本參數，統一更新為新值（例如 `?v=20261013`）以破除瀏覽器快取。
2. 驗證：在整個 repo 搜尋 `style.min.css` 與 `main.min.js`，結果必須為 **0 筆**（排除本文件）。
3. 刪除 `js/main.min.js` 與 `css/style.min.css`（`git rm`）。
4. **風險提示**：三語首頁會從 8 月版程式碼切換為 10 月版，首頁行為可能改變。必須本機開啟檢查（`python -m http.server 8000`）：
   - Hero 輪播切換與圖片延遲載入
   - 導覽列、手機漢堡選單、語言下拉選單（桌機 + 手機寬度）
   - RFQ 詢價表單／彈窗
   - 瀏覽器 Console 無錯誤
5. Commit：`refactor(assets): unify all pages on main.js/style.css and remove stale .min files`

## 步驟 2：在 `main.js` 與 `style.css` 內加入分區目錄（不拆檔）

1. 先完整閱讀 `js/main.js`，**依實際程式碼**辨識功能區塊（不可憑猜測）。目前只有少量註解（約第 301、319、1129 行）。
2. 檔案最上方加入目錄註解，例如：
   ```js
   /* ============ TABLE OF CONTENTS ============
    * [S1] Navbar & mobile menu ........ search "[S1]"
    * [S2] Language dropdown ........... search "[S2]"
    * [S3] Hero carousel / lazy bg ..... search "[S3]"
    * ...（依實際內容填寫）
    * =========================================== */
   ```
   並在每個區塊開頭加 `// ===== [S1] Navbar & mobile menu =====`。
3. **只加註解，不改任何邏輯、不調整程式碼順序。** 用 `git diff` 確認差異只有註解行。
4. `css/style.css` 同樣處理（`/* ===== [C1] Base / variables ===== */` 等）。
5. Commit：`docs(code): add section index comments to main.js and style.css`

## 步驟 3：`.gitignore` 排除雜訊

在 `.gitignore` 追加（先確認這些檔案沒被 git 追蹤：`git ls-files <path>`）：
```
*.log
.pytest_tmp/
.codex-stage/
.dfm-v2-*/
.toolmaker-*/
.vision-*/
auto-cad-app-*/
pytest-*/
scratch/
option_a_corrected_preview/
```
**不要刪除**這些檔案（可能是使用者其他專案的 CAD／DFM 工作資料），只做 ignore。
Commit：`chore: ignore local logs and tool work directories`

## 步驟 4（需先取得使用者同意，另案規劃）：共用 HTML 元件

- 導覽列、頁尾、RFQ 彈窗在 91 個頁面各自複製。
- 可行方案：寫一支 Python 腳本 `tools/sync_partials.py`，以 `<!-- PARTIAL:nav:start -->` … `<!-- PARTIAL:nav:end -->` 標記，從 `partials/nav.zh.html`、`nav.en.html`、`nav.ja.html` 同步替換內容。輸出仍為靜態 HTML（不影響 SEO／效能）。
- 風險高（會改動全部頁面），必須先提方案給使用者確認，先用 1～2 頁試行，並檢查 `<div>`／`<section>` 標籤是否平衡。

---

## 回報格式（每步完成後）

- 改了哪些檔案（列出清單）
- 驗證指令與實際輸出（例如 grep 0 筆）
- 本機目視檢查結果；沒檢查的項目要明說「未驗證」
- 已知風險與待使用者確認事項
