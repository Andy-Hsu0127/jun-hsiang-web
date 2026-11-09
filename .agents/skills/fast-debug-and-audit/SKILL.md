---
name: fast-debug-and-audit
description: Rapid root-cause debugging, fast file indexing, and multilingual static site consistency auditing. Prevents slow network-drive scans and eliminates guess-based debugging.
---

# Fast Debug & Code Audit Protocol (極速除錯與代碼審計規則)

本規則專為本工作區（Windows 網路磁碟環境 `P:\tets`、三語靜態網站 91 個 HTML 頁面）制定，**所有 AI 代理人除錯時必須強制執行，違者視為嚴重低效**。

---

## 🔴 規則一：嚴禁在網路磁碟執行慢速全域遞迴搜尋 (Zero Slow Recursive Scans)

- **痛點根源**：本專案位於 `P:` 槽網路磁碟。使用 PowerShell `Get-ChildItem -Recurse` 或 `Select-String` 遍歷數千個檔案時，每次 SMB 網路往返需要 3～5 分鐘，嚴重拖垮效率。
- **強制規範**：
  - ❌ **絕對禁止**：`Get-ChildItem -Recurse`、慢速全盤 grep。
  - ✅ **必須使用**：
    1. **`git grep -n "關鍵字"`**（直接讀取 Git 本機索引，0.2 秒完成）。
    2. **極速 Python 記憶體串流掃描**（`tools/fast_audit.py`，0.5 秒完成全站 91 個 HTML 掃描）。

---

## 🔴 規則二：系統化除錯三步法 (Systematic Debugging Protocol)

遇到使用者回報 Bug（如「畫面文字有中文」、「功能沒反應」）時，必須遵守 3 步驟：
1. **截圖/現象 10 秒精準提取**：直接從截圖提取「唯一關鍵詞」（例如 `加工服務`），立即執行 `git grep` 查出源頭。禁止反覆猜測或探索無關檔案。
2. **Git 歷史追溯（Git Blame / Log -S）**：使用 `git log -S "關鍵字" -n 3 --oneline` 找出是哪次 commit 造成的污染，5 秒釐清前因後果。
3. **單點修復並回報**：一律以 targeted 腳本統一修正，並在 30 秒內跑驗證斷言確認結果。

---

## 🛠️ 內建極速診斷工具：`tools/fast_audit.py`

執行指令：
```bash
python tools/fast_audit.py
```

### 工具自動檢查項目：
1. **多語系污染檢測（i18n Leakage）**：
   - 檢查 `ja/*.html` 是否誤植繁中詞彙（`加工服務`、`鈞翔實業`、`聯絡我們`、`版權所有` 等嚴格繁中專用字 `體`、`處`、`開`、`實`、`製`）。
   - 檢查 `en/*.html` 是否誤植中文字元（除繁中 slug 連結外）。
   - 檢查 `en/` 與 `ja/` 是否殘留台灣本地市話格式（如 `(02)`、`tel:02`、傳真 `(02)`），海外頁面一律強制為國際碼 `+886-2-2203-9918` 與 `tel:+886222039918`。
2. **過期資源與雙版本檢查**：
   - 檢查是否有人重新引入 `.min.js` 或 `.min.css`。
3. **導覽列與品牌一致性**：
   - 確保日文全部使用 `鈞翔実業`。
   - 確保英文全部使用 `Jun-Hsiang`。
   - 確保繁中全部使用 `鈞翔實業`。
4. **B2B 轉單路徑完整性（Zero-Friction RFQ Check）**：
   - 確保全站頁面均包含廠方直通電話（`2203-9918`）與直通 Email（`jojo.li888@msa.hinet.net`）。
   - 確保行動版具備完整的 `#hamburger` 與 `#mobile-menu` 導覽結構。
   - 檢查並禁止殘留舊版孤立的 `#nav-toggle` 按鈕，防止 JS 事件綁定衝突與排版錯位。
