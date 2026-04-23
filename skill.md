# 🏭 鈞翔實業有限公司 — 公司形象網站 Skill 規劃
# 【方案 B】標準企業風格 — 業界主流 B2B 清晰佈局

> **目標**：以標準 B2B 傳產企業網站（如 Chieftech）的架構，打造一個穩重、極致清晰的公司形象網站
> **語言**：繁體中文  
> **風格定位**：工業科技感 × 乾淨實心板塊 × 穩重專業  
> **設計方向**：明亮主題（白色/淺藍）搭配實心且固定的 Navbar，移除會干擾閱讀的全域透明遮罩，還原本色照片。

---

## 📋 一、公司基本資訊

| 項目 | 內容 |
|------|------|
| **公司名稱** | 鈞翔實業有限公司 |
| **英文名稱** | Jun-Hsiang Enterprise Co., Ltd. |
| **成立時間** | 1991 年 8 月 1 日 |
| **產業類別** | 矽膠 / 橡膠製品成型代工廠 |
| **核心技術** | 真空熱壓、固態矽膠射出、LSR 液態矽膠射出 |
| **認證** | ISO 9001 |
| **開模經驗** | 30 年以上 |
| **地址** | 242 新北市新莊區新樹路 345 巷 3 號 |
| **電話** | (02) 2203-9918 |
| **傳真** | (02) 2206-6968 |
| **E-mail** | jojo.li888@msa.hinet.net
| **官網** | https://www.jun-hsiangs.com/ |

### 主要產品線
- 矽膠按鍵
- 防水圈 / O 型環
- 異材結合（矽膠 + 金屬、矽膠 + 塑膠、矽膠 + 玻璃）
- 矽膠包鐵
- 背膠腳墊
- 矽橡膠平板
- 汽車零件
- 電子零件
- 醫用矽膠
- 壁震橡膠
- 特殊原料（氟素矽膠、抗靜電矽膠、HNBR 等）
- 油封防水

---

## 🎨 二、品牌識別與設計規範（Design System）

### 2.1 設計核心理念

本網站自適應轉換至 **標準 B2B 企業型** 佈局，核心特點包括：

1. **實心區塊導覽列** — 取消透明毛玻璃，改為實心底色，保證 Logo 高對比且畫面不重疊。
2. **明亮純淨主題** — 摒棄深沉背景，以標準白色、淺灰色與深藍文字為主，強調傳統工業的務實感。
3. **清晰的橫幅輪播** — Banner 採用真實輪播 (Carousel)，高度調整為適當觀感 (如 70vh)，捨棄超暗遮罩。
4. **側邊欄產品分類** — 經典的左選單、右網格 (Sidebar Layout)，符合 B2B 採購買主操作習慣。
5. **獨立商品詳情 (Modal)** — 兼顧 SPA 順暢度，點擊商品開啟全螢幕詳細頁，保留完整麵包屑導航。
6. **消除橫向破圖** — 嚴格執行 `max-width` 限制與清晰的 Padding，拔除會造成右側白邊的 `100vw` 溢位特效。

### 2.2 色彩系統 (Color Tokens)

```css
:root {
    /* ---- 主色調（工業金 × 深海藍） ---- */
    --color-primary:        #1B3A5C;    /* 深海藍 - 穩重專業 */
    --color-primary-light:  #2A5A8C;    /* 淺海藍 */
    --color-primary-dark:   #0F2440;    /* 極深藍 */

    --color-accent:         #D4A843;    /* 工業金 - 品質與信任 */
    --color-accent-light:   #E8C86A;    /* 亮金 */
    --color-accent-dark:    #B08A2E;    /* 暗金 */

    /* ---- 輔助色 ---- */
    --color-success:        #2ECC71;    /* 成功綠 */
    --color-warning:        #F39C12;    /* 警示橙 */
    --color-info:           #3498DB;    /* 資訊藍 */

    /* ---- 中性色（深色主題） ---- */
    --color-bg-primary:     #0A0F1C;    /* 深色主背景 */
    --color-bg-secondary:   #111827;    /* 次要背景 */
    --color-bg-card:        #1A2332;    /* 卡片背景 */
    --color-bg-elevated:    #243044;    /* 浮層背景 */

    --color-text-primary:   #F1F5F9;    /* 主文字 */
    --color-text-secondary: #94A3B8;    /* 次要文字 */
    --color-text-muted:     #64748B;    /* 輔助文字 */

    --color-border:         rgba(255, 255, 255, 0.08);
    --color-border-hover:   rgba(212, 168, 67, 0.3);
}
```

### 2.3 漸層系統

```css
:root {
    --gradient-hero:        linear-gradient(135deg, #0A0F1C 0%, #1B3A5C 50%, #0F2440 100%);
    --gradient-accent:      linear-gradient(135deg, #D4A843 0%, #E8C86A 50%, #B08A2E 100%);
    --gradient-card:        linear-gradient(145deg, rgba(26, 35, 50, 0.8), rgba(15, 36, 64, 0.4));
    --gradient-overlay:     linear-gradient(180deg, rgba(10, 15, 28, 0) 0%, rgba(10, 15, 28, 0.95) 100%);
    --gradient-glass:       linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
}
```

### 2.4 字型系統 (Typography)

```css
:root {
    /* Google Fonts */
    --font-heading:    'Outfit', 'Noto Sans TC', sans-serif;
    --font-body:       'Inter', 'Noto Sans TC', sans-serif;
    --font-mono:       'JetBrains Mono', monospace;

    /* 字型尺寸（流式排版） */
    --text-display:    clamp(3rem, 6vw, 5.5rem);      /* 超大標題 */
    --text-h1:         clamp(2.25rem, 4vw, 3.75rem);   /* H1 */
    --text-h2:         clamp(1.75rem, 3vw, 2.75rem);   /* H2 */
    --text-h3:         clamp(1.25rem, 2vw, 1.75rem);   /* H3 */
    --text-body:       1rem;                            /* 內文 16px */
    --text-body-lg:    1.125rem;                        /* 大內文 18px */
    --text-small:      0.875rem;                        /* 小字 14px */
    --text-caption:    0.75rem;                         /* 註解 12px */

    /* 行高 */
    --leading-tight:   1.2;
    --leading-normal:  1.6;
    --leading-relaxed: 1.8;

    /* 字重 */
    --weight-regular:  400;
    --weight-medium:   500;
    --weight-semibold: 600;
    --weight-bold:     700;
    --weight-black:    900;
}
```

### 2.5 間距系統 (Spacing)

```css
:root {
    --space-1:   0.25rem;   /* 4px */
    --space-2:   0.5rem;    /* 8px */
    --space-3:   0.75rem;   /* 12px */
    --space-4:   1rem;      /* 16px */
    --space-5:   1.25rem;   /* 20px */
    --space-6:   1.5rem;    /* 24px */
    --space-8:   2rem;      /* 32px */
    --space-10:  2.5rem;    /* 40px */
    --space-12:  3rem;      /* 48px */
    --space-16:  4rem;      /* 64px */
    --space-20:  5rem;      /* 80px */
    --space-24:  6rem;      /* 96px */
    --space-32:  8rem;      /* 128px */

    --section-padding: clamp(4rem, 10vh, 8rem);
    --container-max:   1280px;
    --container-wide:  1440px;
}
```

### 2.6 圓角與陰影

```css
:root {
    /* 圓角 */
    --radius-sm:   0.375rem;   /* 6px */
    --radius-md:   0.75rem;    /* 12px */
    --radius-lg:   1rem;       /* 16px */
    --radius-xl:   1.5rem;     /* 24px */
    --radius-full: 9999px;

    /* 陰影 */
    --shadow-sm:       0 2px 8px rgba(0,0,0,0.15);
    --shadow-md:       0 4px 16px rgba(0,0,0,0.2);
    --shadow-lg:       0 8px 32px rgba(0,0,0,0.3);
    --shadow-xl:       0 16px 48px rgba(0,0,0,0.4);
    --shadow-glow:     0 0 30px rgba(212, 168, 67, 0.15);
    --shadow-glow-lg:  0 0 60px rgba(212, 168, 67, 0.25);
}
```

### 2.7 動效系統 (Animation Tokens)

```css
:root {
    /* 過渡時間 */
    --transition-fast:    150ms ease;
    --transition-normal:  300ms ease;
    --transition-slow:    500ms ease;
    --transition-smooth:  600ms cubic-bezier(0.16, 1, 0.3, 1);

    /* 緩動函數 */
    --ease-out-expo:   cubic-bezier(0.16, 1, 0.3, 1);
    --ease-in-out:     cubic-bezier(0.4, 0, 0.2, 1);
    --ease-spring:     cubic-bezier(0.34, 1.56, 0.64, 1);

    /* 捲動觸發動畫延遲（Stagger） */
    --stagger-1: 0ms;
    --stagger-2: 80ms;
    --stagger-3: 160ms;
    --stagger-4: 240ms;
    --stagger-5: 320ms;
}
```

---

## 🏗️ 三、網站架構 (Site Map)

```
首頁 (index.html) — 單頁式 SPA，平滑捲動導覽
│
├── [Section 1] Hero 主視覺         (#hero)
├── [Section 2] 關於鈞翔             (#about)
│   ├── 公司簡介
│   ├── 公司沿革（時間軸動畫）
│   └── 經營理念（四大卡片）
├── [Section 3] 服務技術             (#services)
│   ├── 固態矽膠壓出技術
│   └── 液態矽膠射出技術 (LSR)
├── [Section 4] 產品實現             (#products)
│   ├── 矽膠製品
│   ├── 油封防水
│   ├── 特殊橡/矽膠
│   └── 異材結合
├── [Section 5] 品質認證             (#quality)
│   └── ISO 9001 + 數字統計
├── [Section 6] 聯絡我們             (#contact)
│   ├── 聯絡表單
│   └── Google Map + 聯絡資訊
└── [Section 7] Footer
```

> **為什麼用單頁式？**  
> Webflow 最經典的展示型網站都是單頁式設計，透過捲動動畫串連各區段，  
> 讓使用者有「一次看完整個品牌故事」的沉浸體驗。

---

## 📄 四、各區塊詳細規劃

### 4.1 🔝 Navigation Bar（置頂導覽列）

**Webflow 特色設計**：
- 固定置頂，**毛玻璃**效果 (`backdrop-filter: blur(20px)`)
- 初始透明，捲動後漸變為半透明深色 + 下方微陰影
- Logo 左側，導覽連結右側
- **捲動方向偵測**：向下捲動時隱藏、向上捲動時顯示（Webflow 經典行為）
- 手機版：漢堡選單 + **全螢幕展開動畫**（左側滑入或淡入蓋滿）

**導覽項目**：
```
[Logo 鈞翔實業] ───────── 關於鈞翔 | 服務技術 | 產品實現 | 品質認證 | 聯絡我們
```

**Webflow 互動效果**：
- 連結 hover：金色底線**從左到右滑入**（`::after` pseudo-element + `scaleX(0→1)`）
- **當前區段自動高亮**（Intersection Observer 偵測各 section 可見性）
- Logo hover 微旋轉 + 光暈

---

### 4.2 🏠 Hero Section（首屏主視覺）

**Webflow 風格重點**：全螢幕 100vh 沉浸式，用動畫說故事

**佈局結構**：
```
┌─────────────────────────────────────────────────┐
│                                                 │
│   [動態粒子/幾何線條背景 Canvas]                    │
│                                                 │
│        ─── 鈞翔實業 ───                          │
│     專業矽膠 ‧ 橡膠製品 ‧ 30 年工藝傳承             │
│   ISO 9001 認證 ─ 液態矽膠射出 ‧ 固態矽膠壓出       │
│                                                 │
│     [了解更多]  [聯絡我們]                          │
│                                                 │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐            │
│  │  30+    │ │ISO 9001 │ │ 1000+  │            │
│  │  年經驗  │ │ 品質認證 │ │ 客製專案 │            │
│  └─────────┘ └─────────┘ └─────────┘            │
│                                                 │
│            ↓ 向下捲動探索                          │
└─────────────────────────────────────────────────┘
```

**Webflow 等級動效**：
1. 頁面載入 → 全螢幕深色遮罩 + Logo 淡入 → 遮罩向上**滑出**
2. 主標題「鈞翔實業」逐字或逐行 **淡入上移**（stagger 200ms）
3. 副標題延遲 400ms 淡入
4. CTA 按鈕延遲 600ms 從下方彈入（ease-spring）
5. 數據卡片延遲 800ms 從底部 **依序滑入**
6. 背景：深色漸層 + **動態粒子/幾何網格** 緩慢流動（Canvas 繪製）
7. 底部滾動提示：滑鼠圖標 + 箭頭 **上下呼吸動畫**

**CTA 按鈕設計**：
- 主按鈕：金色漸層填充，hover 時光暈擴散 + 微上移
- 次按鈕：透明邊框（ghost button），hover 時邊框變金色 + 背景微填充

---

### 4.3 📖 關於鈞翔 Section (#about)

**區段進場動畫**：金色短橫線從中心擴展 + 標題淡入上移

#### A. 公司簡介
**佈局**：左文字（60%）/ 右圖片（40%）
- Webflow 動效：文字從左淡入，圖片從右淡入，**時間錯開 200ms**
- 公司介紹段落（取自官網真實內容）
- 3 個**特色亮點卡片**（橫排，毛玻璃卡片）：

| 圖標 | 標題 | 描述 |
|------|------|------|
| 🔧 | 專業技術 | 30 年以上開模經驗，真空熱壓/射出/LSR 全方位 |
| 🏭 | 完整產線 | 真空熱壓 / 固態射出 / 液態射出一站式服務 |
| ✅ | 品質保證 | ISO 9001 國際認證，三不原則嚴格把關 |

#### B. 公司沿革（時間軸）
**Webflow 風格垂直時間軸**：
- 中央金色線條，**捲動時線條逐漸延伸**（`scaleY` 動畫）
- 左右交錯佈局，每個節點有**圓形標記（金色圓點）**
- 每個時間節點在**進入視窗時才亮起**（IntersectionObserver）

```
          │
    1991 ●── 鈞翔實業創立，投入矽膠橡膠製造領域
          │
          ●── 導入固態矽膠射出技術，提升產能
          │
          ●── 取得 ISO 9001 品質管理認證
          │
          ●── 引進 LSR 液態矽膠射出設備
          │
          ●── 擴廠升級，導入自動化製程
          │
    2024 ●── 持續精進，累積超過 1000+ 客製專案
          │
```

#### C. 經營理念
**佈局**：2×2 Grid，每張卡片為**毛玻璃效果**

| 英文標籤 | 中文標題 | 核心內容 |
|----------|----------|----------|
| **Friend** | 客戶是我們的夥伴 | 將每位客戶定位為合作夥伴，透過工程與設計先期討論，提供迅速報價 |
| **Honest** | 堅持誠信 | 不輕易承諾，一旦做出承諾定會不計代價全力以赴 |
| **Profession** | 矽、橡膠專業製造 | 專注矽橡膠技術（油壓/射出），帶給客戶多元化專業服務 |
| **Quality** | 品質保證 | 不製造、不接受、不流出不良品，品質至善、精益求精 |

**Webflow 動效**：
- 卡片 staggered fade-in（依序進場，間隔 100ms）
- 卡片 hover：**上浮 8px + 金色邊框光暈** + 背景亮度微增
- 英文標籤用 `--font-mono` 字型，大寫，金色

---

### 4.4 ⚙️ 服務技術 Section (#services)

**Webflow 特色**：**Zigzag 左右交錯圖文佈局**，區段之間用斜切 SVG 分割

#### 技術一：固態矽膠壓出技術
```
┌──────────────────────────────────┐
│  [技術圖片]     │     技術說明     │
│                │  ‧ 傳統成熟技術   │
│  (左側，        │  ‧ 適合大量生產   │
│   hover 微放大)  │  ‧ 模具成本較低   │
│                │  ‧ 適用產品列表   │
└──────────────────────────────────┘
```

#### 技術二：液態矽膠射出技術 (LSR)
```
┌──────────────────────────────────┐
│     技術說明     │  [技術圖片]     │
│  ‧ 精密成型技術   │                │
│  ‧ 自動化程度高   │  (右側，        │
│  ‧ 適合精密零件   │   hover 微放大)  │
│  ‧ 技術優勢列表   │                │
└──────────────────────────────────┘
```

**Webflow 動效**：
- 圖片：從左/右側**滑入 + 淡入**
- 文字：從對側**滑入 + 淡入**（時間錯開 150ms）
- 圖片 hover：`scale(1.03)` + 陰影加深
- 技術規格數字：**計數器動畫**（0 → 目標值）

---

### 4.5 🧊 產品實現 Section (#products)

**Webflow 特色**：**標籤式篩選 + 動態 Grid 佈局**

**分類標籤列**（居中，pill 樣式）：
```
[ 全部產品 ] [ 矽膠製品 ] [ 油封防水 ] [ 特殊橡/矽膠 ] [ 異材結合 ]
```
- 選中標籤：**金色填充 + 白色文字**
- 未選中：透明背景 + 灰色文字 + hover 金色邊框
- 切換時：產品卡片 **layout 動畫**（淡出→重排→淡入）

**產品卡片設計**（Glassmorphism 風格）：
```
┌─────────────────────┐
│                     │
│    [產品圖片]         │  ← hover 時微放大
│                     │
├─────────────────────┤
│  產品名稱            │
│  [分類標籤]          │  ← 小型 pill 樣式
│                     │
│  hover 時出現：       │
│  [查看詳情 →]        │  ← 金色連結
└─────────────────────┘
```

**Webflow 滑鼠跟隨光效**：
```javascript
// 卡片上的光效跟隨滑鼠位置
card.addEventListener('mousemove', (e) => {
    const rect = card.getBoundingClientRect();
    card.style.setProperty('--mouse-x', `${e.clientX - rect.left}px`);
    card.style.setProperty('--mouse-y', `${e.clientY - rect.top}px`);
});
// CSS: radial-gradient(circle at var(--mouse-x) var(--mouse-y), rgba(212,168,67,0.1), transparent)
```

**產品資料**：

| 分類 | 產品項目 |
|------|----------|
| 矽膠製品 | 矽膠導電按鍵、生活科技用品、電子零件矽膠、醫療矽膠、汽車零件矽膠、UV 表面改質 |
| 油封防水 | 防水圈、O-Ring、耐高溫墊圈、耐燃墊圈、耐酸鹼墊圈、抗靜電墊圈 |
| 特殊橡/矽膠 | 氟素矽膠、抗靜電矽膠、HNBR、特殊配方矽膠 |
| 異材結合 | 矽膠+金屬、矽膠+塑膠、矽膠+玻璃、矽膠包鐵 |

---

### 4.6 🏆 品質認證 Section (#quality)

**Webflow 特色**：居中排列 + **動態數字統計** + 脈衝光暈

**佈局**：
```
┌─────────────────────────────────────────┐
│          ─── 品質認證 ───                │
│                                         │
│     [ISO 9001 認證徽章]                  │
│      (脈衝光暈動畫)                      │
│                                         │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ │
│  │  30+   │ │ 99.8%  │ │ 1000+  │ │  50+  │ │
│  │ 年經驗  │ │ 良品率  │ │ 客製專案 │ │ 合作客戶│ │
│  └────────┘ └────────┘ └────────┘ └────────┘ │
│                                         │
│  ❌ 不製造不良品                          │
│  ❌ 不接受不良品   ← 逐一淡入動畫          │
│  ❌ 不流出不良品                          │
└─────────────────────────────────────────┘
```

**Webflow 動效**：
- ISO 徽章：**光暈脈衝動畫**（`box-shadow` 週期性擴散）
- 數字統計：**計數器動畫**（0 → 目標值，捲動觸發，duration 2s）
- 三不原則：逐一從左側**滑入淡入**（stagger 300ms）

---

### 4.7 📞 聯絡我們 Section (#contact)

**佈局**：左側聯絡表單（55%） / 右側資訊卡 + 地圖（45%）

#### 聯絡表單（Webflow 風格浮動標籤）：
```
┌─────────────────────────────┐
│  公司名稱                    │ ← focus 時 label 上浮 + 底線金色
│  ─────────────────────────  │
│  聯絡人                     │
│  ─────────────────────────  │
│  電話          E-mail       │ ← 雙欄
│  ────────     ────────     │
│  產品需求 [▼ 請選擇]         │ ← select 下拉
│  ─────────────────────────  │
│  留言內容                    │
│  ─────────────────────────  │
│  ─────────────────────────  │
│                             │
│       [✉ 送出詢問]           │ ← 金色漸層按鈕
└─────────────────────────────┘
```

#### 聯絡資訊卡（毛玻璃）：
```
┌─────────────────────────────┐
│  📍 242 新北市新莊區          │
│     新樹路 345 巷 3 號        │
│  📞 (02) 2203-9918           │
│  📠 (02) 2206-6968           │
│  ✉  andy_hsu@jun-hsiang...  │
│  🕘 週一至週五 08:00-17:00    │
├─────────────────────────────┤
│  [Google Maps 嵌入地圖]       │
│                             │
└─────────────────────────────┘
```

**Webflow 動效**：
- 表單欄位 focus：底線從中心**向兩側延伸**，變為金色
- label 上浮：`translateY(-24px)` + 字型縮小 + 顏色變金色
- 送出按鈕：hover 時漸層**位移動畫** + 光暈
- 送出成功：表單**淡出** → 成功訊息**淡入**（打勾動畫 ✓）

---

### 4.8 🦶 Footer

**佈局**：深色背景（比主背景更深），三欄式 + 底部版權

```
┌──────────────────────────────────────────────────┐
│  [Logo] 鈞翔實業      │  快速連結        │  聯絡資訊   │
│  專業矽膠橡膠製造      │  ‧ 關於鈞翔      │  📍 地址   │
│  30年工藝傳承         │  ‧ 服務技術      │  📞 電話   │
│                      │  ‧ 產品實現      │  📠 傳真   │
│                      │  ‧ 品質認證      │  ✉ E-mail │
│                      │  ‧ 聯絡我們      │           │
├──────────────────────────────────────────────────┤
│  © 2024 鈞翔實業有限公司 版權所有  │  [↑ 回到頂部]     │
└──────────────────────────────────────────────────┘
```

- 「回到頂部」按鈕：固定右下角，捲動超過一屏後才出現
- 連結 hover：金色 + 微右移動畫

---

## 🎬 五、全域 Webflow 動畫規範

### 5.1 捲動動畫系統（Scroll Animations）

使用 `IntersectionObserver` API 偵測元素進入視窗，觸發 CSS animation。
**這是 Webflow Interactions 2.0 的核心機制。**

| 動畫類型 | 觸發時機 | CSS 實現 |
|----------|----------|----------|
| `fade-in-up` | 元素進入視窗 | `opacity: 0→1`, `translateY(30px→0)` |
| `fade-in-left` | 元素進入視窗 | `translateX(-50px→0)` |
| `fade-in-right` | 元素進入視窗 | `translateX(50px→0)` |
| `scale-in` | 元素進入視窗 | `scale(0.9→1)` + `opacity(0→1)` |
| `stagger` | 父容器進入視窗 | 子元素依序延遲（80ms間隔） |
| `counter-up` | 元素進入視窗 | JS 數字遞增 0→目標值 |
| `line-grow` | 時間軸進入視窗 | `scaleY(0→1)` origin top |
| `glow-pulse` | 始終播放 | `box-shadow` 脈衝 |

### 5.2 微互動規範（Micro-interactions）

| 元素 | 觸發 | 效果 |
|------|------|------|
| **按鈕** | hover | 上移 2px + 光暈擴散 + `transform: scale(1.02)` |
| **按鈕** | hover (磁吸) | 微微向滑鼠方向偏移（JS） |
| **卡片** | hover | 上浮 8px + 陰影加深 + 邊框金色光暈 |
| **卡片** | mousemove | 光效跟隨滑鼠位置（radial-gradient） |
| **導覽連結** | hover | 金色底線從左到右滑入 |
| **圖片** | hover | `scale(1.03)` + `brightness(1.05)` |
| **表單欄位** | focus | 底線從中心向兩側延伸，變金色 |
| **Logo** | hover | 微旋轉 + 光暈 |

### 5.3 頁面載入序列（Page Load Sequence）

```
t=0ms      全螢幕深色遮罩顯示
t=300ms    Logo 在遮罩中央淡入
t=1200ms   遮罩向上滑出（600ms，ease-out-expo）
t=1400ms   Hero 主標題逐行淡入上移（stagger 200ms）
t=1800ms   Hero 副標題淡入
t=2000ms   CTA 按鈕從下方彈入（ease-spring）
t=2200ms   數據卡片依序滑入（stagger 100ms）
t=2500ms   導覽列從上方滑入
t=2800ms   滾動提示開始呼吸動畫
t=∞        其餘區段等待捲動觸發
```

---

## 📱 六、響應式設計斷點 (RWD Breakpoints)

```css
/* Mobile First 策略 */
/* 預設：手機直向 (< 640px) */
@media (min-width: 640px)  { /* 手機橫向 */ }
@media (min-width: 768px)  { /* 平板直向 */ }
@media (min-width: 1024px) { /* 平板橫向 / 小筆電 */ }
@media (min-width: 1280px) { /* 桌面 */ }
@media (min-width: 1536px) { /* 大螢幕 */ }
```

### 佈局適配規則：

| 斷點 | 導覽 | Grid 欄數 | 圖文佈局 | 時間軸 |
|------|------|-----------|---------|--------|
| < 640px | 漢堡選單 | 1 欄 | 堆疊 | 單側 |
| 640-768px | 漢堡選單 | 2 欄 | 堆疊 | 單側 |
| 768-1024px | 水平列 | 2-3 欄 | 並排 | 雙側 |
| 1024-1280px | 水平列 | 3-4 欄 | 並排 | 雙側 |
| > 1280px | 水平列 | 4 欄 | 並排 | 雙側 |

---

## 🔧 七、技術棧

| 類別 | 技術選擇 | 說明 |
|------|----------|------|
| **結構** | HTML5 | 語義化標籤（header, nav, main, section, article, footer） |
| **樣式** | Vanilla CSS | CSS Custom Properties + Grid + Flexbox + @keyframes |
| **互動** | Vanilla JavaScript | IntersectionObserver + Smooth Scroll + Canvas |
| **字型** | Google Fonts | Outfit（標題）+ Inter（內文）+ Noto Sans TC（中文） |
| **圖標** | Lucide Icons (CDN) | 輕量 SVG 圖標庫 |
| **圖片** | AI 生成 | 使用 `generate_image` 工具產出所有所需圖片 |
| **動畫** | CSS + JS | `@keyframes` 定義 + `IntersectionObserver` 觸發 |
| **粒子背景** | Canvas API | 純 JS Canvas 繪製動態粒子系統 |
| **地圖** | Google Maps Embed | iframe 嵌入 |
| **部署** | 靜態檔案 | 可直接在本地用 Live Server 預覽 |

> **不使用任何框架**：無 Tailwind、無 React/Vue、無 jQuery。  
> 全部使用原生 Web API，確保效能最佳、依賴最少。

---

## 📁 八、檔案結構

```
p:\tets\
├── index.html              # 主頁面（SPA 單頁）
├── css/
│   └── style.css           # 完整樣式（含 Design System + 所有元件）
├── js/
│   ├── main.js             # 主要邏輯（導覽、捲動偵測、漢堡選單）
│   ├── animations.js       # 捲動動畫引擎（IntersectionObserver）
│   ├── counter.js          # 數字計數器動畫
│   └── particles.js        # Canvas 粒子背景系統
├── images/
│   ├── hero-bg.webp        # Hero 背景圖
│   ├── factory.webp        # 工廠/公司圖片
│   ├── products/           # 產品圖片
│   │   ├── silicone-keypad.webp
│   │   ├── o-ring.webp
│   │   ├── special-silicone.webp
│   │   └── multi-material.webp
│   └── tech/               # 技術圖片
│       ├── solid-silicone.webp
│       └── lsr-injection.webp
├── favicon.ico
└── skill.md                # 本規劃文件
```

---

## 🚀 九、分階段實作步驟

### Phase 1：基礎建設 🔨
- [ ] 建立檔案目錄結構
- [ ] 建立 `style.css`，寫入完整 Design System（所有 CSS tokens）
- [ ] 建立 CSS Reset / Base Styles / 通用元件樣式
- [ ] 建立 `index.html` 骨架 + SEO meta tags + Google Fonts 引入
- [ ] 引入 Lucide Icons CDN

### Phase 2：導覽列 + Hero 🎯
- [ ] 導覽列 HTML + CSS（毛玻璃 + 響應式）
- [ ] 漢堡選單 + 全螢幕展開（JS）
- [ ] 捲動偵測：方向感知隱藏/顯示（JS）
- [ ] 當前區段高亮（IntersectionObserver）
- [ ] Hero HTML + CSS（全螢幕 + 動態背景）
- [ ] Canvas 粒子背景系統 (`particles.js`)
- [ ] Hero 文字進場動畫
- [ ] 數據亮點卡片
- [ ] 平滑捲動（smooth scroll to anchors）
- [ ] 頁面載入序列動畫

### Phase 3：關於鈞翔 📖
- [ ] 公司簡介（圖文並排 + 亮點卡片）
- [ ] 公司沿革（垂直時間軸 + 捲動動畫）
- [ ] 經營理念（四大理念卡片 + 毛玻璃效果）
- [ ] 生成所需圖片（generate_image）

### Phase 4：服務技術 + 產品 ⚙️
- [ ] 服務技術 Zigzag 佈局（固態/液態矽膠）
- [ ] 區段斜切 SVG 分割器
- [ ] 產品分類標籤篩選（JS 篩選邏輯）
- [ ] 產品卡片 Grid + Glassmorphism
- [ ] 產品卡片滑鼠跟隨光效
- [ ] 生成產品/技術圖片（generate_image）

### Phase 5：品質認證 + 聯絡 + Footer 📞
- [ ] 品質認證區段（ISO 徽章 + 數字統計）
- [ ] 數字計數器動畫 (`counter.js`)
- [ ] 三不原則動畫
- [ ] 聯絡表單（浮動標籤 + 驗證）
- [ ] 聯絡資訊卡 + Google Maps 嵌入
- [ ] 表單送出成功動畫
- [ ] Footer 三欄佈局
- [ ] 回到頂部按鈕

### Phase 6：全域動畫 + 打磨 ✨
- [ ] 捲動動畫引擎 (`animations.js`) — 統一管理所有動畫
- [ ] 磁吸按鈕效果
- [ ] 顆粒質感 (Grain Texture) 疊加
- [ ] RWD 全斷點微調測試
- [ ] 效能優化（lazy loading、will-change、壓縮）
- [ ] 瀏覽器最終驗收

---

## 🔍 十、SEO 策略

### Meta Tags
```html
<title>鈞翔實業有限公司 | LSR 液態矽膠射出 · 矽膠橡膠製品專業代工</title>
<meta name="description" content="鈞翔實業創立於1991年，ISO 9001認證矽膠橡膠專業代工廠。提供液態矽膠射出(LSR)、固態矽膠壓出、異材結合等技術，30年以上開模經驗。">
<meta name="keywords" content="矽膠, 液態矽膠, LSR, 橡膠, 矽膠射出, 異材結合, 矽膠按鍵, O型環, 防水圈, ISO 9001, 鈞翔實業">
<meta property="og:title" content="鈞翔實業有限公司 | 專業矽膠橡膠製造">
<meta property="og:description" content="30年矽膠橡膠專業代工經驗，ISO 9001認證，提供LSR液態矽膠射出、固態矽膠壓出等技術服務">
<meta property="og:type" content="website">
<meta property="og:locale" content="zh_TW">
```

### Schema.org 結構化資料
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "鈞翔實業有限公司",
  "alternateName": "Jun-Hsiang Enterprise Co., Ltd.",
  "url": "https://www.jun-hsiangs.com",
  "description": "專業矽膠橡膠製品成型代工廠，ISO 9001認證",
  "foundingDate": "1991-08-01",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "新樹路345巷3號",
    "addressLocality": "新莊區",
    "addressRegion": "新北市",
    "postalCode": "242",
    "addressCountry": "TW"
  },
  "telephone": "(02)2203-9918",
  "faxNumber": "(02)2206-6968",
  "email": "jojo.li888@msa.hinet.net"
}
</script>
```

---

## ⚡ 十一、精品互動技法增強

為提升網站的「WOW Factor」，我們實作了以下高級互動技術：

1. **磁吸式 3D 傾斜 (Magnetic Tilt Effect)**：
   - 應用於所有產品卡片。卡片會根據滑鼠位置產生輕微的 3D 偏轉，創造空間深度感。
   - 實作於 `js/main.js` 並搭配 `transform: preserve-3d`。

2. **滑鼠追蹤光源 (Mouse-Follow Lighting)**：
   - 卡片背景具備一個隨滑鼠移動的「金屬反射光」，增加動態質感。
   - 使用 CSS 變數 `--mouse-x` 與 `--mouse-y` 即時驅動。

3. **優化粒子引擎 (Premium Particle Engine)**：
   - 重構 `js/particles.js`，加入更高的互動靈敏度與工業金偏置色彩。
   - 具備滑鼠排斥與粒子連線效果，展現技術精密感。

4. **文字遮罩滑出動畫 (Mask-Slide Animation)**：
   - 標題採用 `overflow: hidden` 搭配 `translateY`，實現文字從隱形邊界滑出的高級感。

---

## 🔧 十二、技術棧
    transition: opacity 0.3s;
}
.product-card:hover::before { opacity: 1; }
```

### 4. Magnetic Button（磁吸按鈕）
```javascript
button.addEventListener('mousemove', (e) => {
    const rect = button.getBoundingClientRect();
    const dx = (e.clientX - rect.left - rect.width / 2) * 0.3;
    const dy = (e.clientY - rect.top - rect.height / 2) * 0.3;
    button.style.transform = `translate(${dx}px, ${dy}px)`;
});
button.addEventListener('mouseleave', () => {
    button.style.transform = 'translate(0, 0)';
});
```

### 5. Section Divider（區段分割）
```html
<div class="section-divider">
    <svg viewBox="0 0 1440 100" preserveAspectRatio="none">
        <path d="M0,0 L1440,60 L1440,100 L0,100 Z" fill="var(--color-bg-secondary)"/>
    </svg>
</div>
```

### 6. Smooth Scroll（平滑捲動）
```css
html {
    scroll-behavior: smooth;
    scroll-padding-top: 80px; /* 導覽列高度 */
}
```

---

## 📝 十二、開發注意事項

> [!IMPORTANT]
> 1. 所有文字內容必須為**繁體中文**
> 2. 圖片使用 `generate_image` 工具生成，確保每張圖片都是真實可用的
> 3. 所有互動元素必須有 **unique ID** 以利測試
> 4. 確保無障礙設計：`aria-label`、`alt` 屬性、`tabindex`、鍵盤導覽
> 5. 效能目標：首屏載入 < 3 秒、Lighthouse 分數 > 90

> [!WARNING]
> - 不使用任何 CSS 框架（如 Tailwind、Bootstrap）
> - 不使用任何 JS 框架（如 React、Vue、jQuery）
> - 純 HTML + CSS + JavaScript 原生實作
> - 所有樣式透過 CSS Custom Properties 統一管理
> - 不使用任何第三方動畫庫（如 AOS、GSAP）

> [!TIP]
> - 使用 CSS `clamp()` 實現流式字型，避免硬編碼字型大小
> - 使用 `IntersectionObserver` 替代 `scroll` event，效能更佳
> - 圖片使用 `loading="lazy"` 延遲載入
> - 動畫元素使用 `will-change` 提示瀏覽器預先優化
> - Canvas 粒子系統使用 `requestAnimationFrame` 確保流暢
> - 善用 CSS `prefers-reduced-motion` 尊重使用者動畫偏好設定
