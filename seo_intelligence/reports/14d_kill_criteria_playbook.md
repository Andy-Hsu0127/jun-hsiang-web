# 🛡️ 鈞翔實業「矽膠代工」14 天 SEO Kill Criteria 作戰手冊 (正式作戰版)

**生效日期**: 2026-09-14  
**負責單位**: 鈞翔實業 SEO 作戰組  
**戰略目標**: 以最快速度取得商業實效，在 3～4 天判斷 Google 是否接受訊號、7 天判定問題核心、14 天未見領先指標則直接淘汰無效假設 (Pivot)。拒絕被動死等 30 天，拒絕無證據宣稱。

---

## 一、核心原則：不是 14 天保證進前 30，而是「嚴格控制試錯成本」

Google 官方明確指出：重新抓取可能需要數天至數週，Request Indexing 亦不保證立刻重新收錄。因此：
1. **「尚未重新抓取 (Not yet recrawled)」與「抓取後無反應 (Recrawled with no response)」必須嚴格分開判讀**。
2. **Search Console 的 24 小時 Preliminary Data** 可作為快速監控領先訊號，但絕不以單日微幅波動（如 72 名跳到 84 名）作為改版依據。
3. **低曝光詞的平均排名本來就會劇烈跳動**，禁止因單日跳動隨意改動頁面。
4. **禁止頻繁重複點擊 Request Indexing**（Google 官方說明重複提交不會加快處理速度）。

---

## 二、固定的 10 組核心商業查詢矩陣 (Two-Tier Query Cluster)

絕不單盯「矽膠代工」（因目前僅 2 次曝光，屬於極容易被 GSC 抽樣忽略的統計雜訊）。全隊固定監控以下 10 組詞：

| 層級分類 | 監控查詢詞 (Query) | 角色與判定邏輯 | 目標著陸頁 (Target Landing Page) |
| :--- | :--- | :--- | :--- |
| **戰略核心 (Tier 1)** | **矽膠代工** | **最終戰略商業 KPI**（接單終極標的） | 首頁 https://www.jun-hsiang.com.tw/ |
| **核心工廠 (Tier 2)** | 矽膠代工廠 | Leading Indicator（實體工廠採購意圖） | 首頁 / |
| **核心工廠 (Tier 2)** | 矽膠工廠 | Leading Indicator（製造商開發意圖） | 首頁 / |
| **核心工廠 (Tier 2)** | 矽膠製造商 | Leading Indicator（廠商資質搜尋） | 首頁 / |
| **商業委託 (Tier 2)** | 矽膠 OEM | Leading Indicator（客製委託代工） | 首頁 / |
| **商業委託 (Tier 2)** | 客製矽膠 | Leading Indicator（客製化需求） | 首頁 / |
| **商業委託 (Tier 2)** | 矽膠開模 | Leading Indicator（模具開發前期需求） | 首頁 / 或 /service.html |
| **專精製程 (Tier 2)** | LSR 代工 | Leading Indicator（高階液態射出採購） | 首頁 / 或 /service.html |
| **專精製程 (Tier 2)** | 液態矽膠代工 | Leading Indicator（高潔淨/高精密需求） | 首頁 / 或 /service.html |
| **專精製程 (Tier 2)** | 矽膠射出 | Leading Indicator（成型工藝搜尋） | 首頁 / 或 /service.html |

> **判定鐵律**：只要整個 Commercial Cluster 整體曝光次數與進池數量上揚，即證明 Google 演算法已開始認定鈞翔為「具備代工製造能力的實體工廠」。

---

## 三、管理層每日唯一追蹤的 6 個健康與進展指標

每天只看這 6 個指標，不浪費時間看 30 個雜訊數據：

| 每日指標 | 觀測來源 | 核心用途與判定 |
| :--- | :--- | :--- |
| **1. Homepage Last Crawl** | GSC 網址審查 | Google 是否已吃到 09/14 新版 Title / H1 |
| **2. Google-selected canonical** | GSC 網址審查 | Google 認定之標準網址是否為 / |
| **3. Cluster Impressions** | GSC 成效報告 | 10 組商業詞的總曝光次數是否開始上升 |
| **4. Cluster Query Count** | GSC 查詢清單 | 10 組商業詞中有幾個開始出現在首頁曝光中 |
| **5. Landing Page** | GSC 網頁分頁 | Google 到底把「矽膠代工」分配給首頁還是知識庫文章 |
| **6. Position Distribution** | GSC / 戰情面板 | 統計進入 Top 100 / Top 50 / Top 30 / Top 20 的詞數 |

---

## 四、14 天滾動式作戰排程 (Rolling Sprint Schedule)

### Day 0 — 基準鎖定 (2026-09-14)
- **已完成**：Intervention #1（首頁 Title / H1 / Hero 對齊「矽膠代工廠」已部署，commit 4abf759）。
- **已執行**：GSC 送出首頁網址審查 ➔ 要求建立索引（僅送一次）。
- **Baseline 鎖定**：保存 7 天、28 天、90 天 GSC 基準資料。
- **作戰原則**：所有後續變動必須記錄於 Change Log，但**不進行全面停工的 Change Freeze**（平行推進 Track B/C/D/E）。

---

### Day 1～3 — 抓取檢驗門檻 (Crawl Gate)
這三天不以排名論成敗，專注檢驗技術通道：
- 🟢 **CONTINUE (繼續推進)**：URL Inspection 顯示 Google 已重新抓取，且新版 Title/H1 已收錄、canonical 正常、DOM 渲染無誤 ➔ 宣告 Intervention #1 正式生效，進入訊號觀察。
- 🟡 **HOLD (等待抓取)**：Google 尚未重爬 ➔ 不判定策略成敗，耐心等待；此期間平行推進 Track D (同業深度研究)、Track E (外部工商黃頁登錄)。
- 🔴 **KILL TECHNICAL ISSUE (技術緊急事故)**：若發現 canonical 異常、Google-selected canonical 不是 /、或出現 noindex / 5xx 錯誤 ➔ **立刻停止一切排名推論，判定為 P0 Technical Incident，優先修復技術缺陷！**

---

### Day 3～4 — 戰術複盤 #1 (Tactical Review #1)
由 GSC 成效資料回答以下 4 個問題：
1. **A. 首頁是否開始取得商業查詢詞？**
   - 若開始出現「矽膠代工廠」「矽膠工廠」「客製矽膠」等曝光 ➔ 🟢 **加碼**！代表方向正確，保留 Relevance，準備攻 Authority。
2. **B. Impressions 上升，但 Position 停在 60～90 名？**
   - 🟢/🟡 **繼續並加碼**！代表 Google 在測試此頁，但信任度不足。立即啟動 3～5 條 Contextual Internal Links 與真實工廠外部引用。
3. **C. 首頁無反應，但 Knowledge 頁面大量吃下代工詞？**
   - 🟡 **PIVOT WARNING**！啟動 Search Intent Audit，評估 Google 是否將當前查詢判定為「指南比較型」，決定是否以內文錨點導向首頁或升級 Service landing page。
4. **D. 完全零變化（且確認已 recrawl）？**
   - 🟡 **提前在 Day 4 啟動 Intervention #2**（站內脈絡連結），不乾等 14 天。

---

### Day 4～6 — 介入手段 #2 (Intervention #2: Contextual Internal Links)
精準部屬 3～5 條高品質自然長句內文錨點（嚴禁 30 篇機械灌字）：
- knowledge-silicone-factory-guide.html ➔ [客製化矽膠代工製造服務](/)
- knowledge-solid-vs-lsr.html ➔ [矽膠成型代工服務](/)
- knowledge-silicone-overmolding-bonding.html ➔ [矽膠異材結合製造](/)
- 寫入 Change Log，追蹤後續影響。

---

### Day 7 — 決策節點 #1 (Decision Gate #1)
管理層的第一個重大決策點。不問「排第幾」，問**「Google 是否已加深對商業意圖的認可？」**：

| Day 7 狀態 | 判定信號 | 戰術決策 |
| :--- | :---: | :--- |
| Query coverage ↑ + Impressions ↑ + 首頁為主頁 | 🟢 | **加碼推進** |
| Impressions ↑ + Position 穩定前進 | 🟢🟢 | **強力加碼**，深化站內支援 |
| Impressions ↑，但 Position 紋風不動 | 🟡 | 關聯性已過關，**全力轉攻外部權威 (Authority Sprint)** |
| 首頁與 Knowledge 頁面互相稀釋曝光 | 🟡 | 執行 Intent / 站內拓撲修正 |
| Knowledge 頁面大幅領先首頁 | 🟡 | 重新評估是否將重心轉為專屬 Commercial Landing Page |
| Google 已重爬，但 Cluster 完全 0 反應 | 🔴 | **Kill「單靠首頁意圖即可突圍」的假設**，轉向整體架構作戰 |
| 發現任何 Technical 錯誤 | 🔴 | 停止內容 SEO，立即修復 Technical |

---

### Day 7～10 — 外部權威攻堅 (Authority Sprint)
若確認關聯性已有，但排名受限於權重，資源全面轉向外部真實實體建設（拒絕任何買賣垃圾外鏈）：
1. **Google 商家檔案 (GBP)**：校正官方公司名稱、工廠地址、電話、官網、類別（橡膠製品製造商）、上傳真實廠房照片。
2. **台灣製造業真實 B2B 名錄**：台灣經貿網 (Taiwantrade)、文筆天天網、台灣黃頁、中華黃頁、公協會名錄，建立一致性 NAP。

---

### Day 10～11 — 戰術複盤 #2 (Tactical Review #2)
檢視 Commercial Query Coverage 的滲透階梯：
- **情境一**：Top 100 = 8 組、Top 50 = 3 組、Top 30 = 1 組 ➔ 🟢 **明確突破**！即使「矽膠代工」本身還在 60 名，也代表整個叢集已全面前進。
- **情境二**：Top 100 = 8 組、Top 50 = 0 組 ➔ 🟡 **Relevance OK / Authority Weak**，持續鞏固外部權威。
- **情境三**：Top 100 仍只有 1 組且毫無動靜 ➔ 🔴 **Strategy Pivot**，逆向分析 SERP 前 20 名是否 90% 為獨立型錄頁，評估建立專屬 /silicone-oem/。

---

### Day 14 — 終極裁決門檻 (Kill Gate)
第 14 天絕不允許「再觀察看看」，必須做出明確裁決：

`	ext
                               【Day 14 裁決】
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         ▼                            ▼                            ▼
   🟢 CONTINUE / SCALE            🟡 PIVOT                      🔴 KILL
  - Cluster 覆蓋明顯增加       - 首頁有曝光但卡在50~100+      - 14天商業詞完全無新增曝光
  - 首頁成為主力 Landing        - 關聯性具備但信任不足         - 首頁未被 Google 接受為主力
  - 多詞進入 Top 50 / Top 30   - 轉為 80% Authority Sprint   - 徹底推翻「首頁單一頁面」假設
  ➔ 啟動真實 DFM 製造證據深化    ➔ 停止修改首頁文案             ➔ 啟動專屬 Landing Page 拓撲重構
`

---

## 五、一句話核心總結

> **「3～4 天看 Google 有沒有接受訊號；7 天判斷 Relevance 還是 Authority 問題；14 天沒有 Commercial Query Coverage 改善，就殺掉 Landing Page 假設並重新研究 SERP。」**