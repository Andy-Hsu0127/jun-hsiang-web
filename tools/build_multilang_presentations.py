"""
Build Traditional Chinese (ZH) and Japanese (JA) 7-Slide 16:9 Executive Company Profiles
using the approved Swiss Industrial Precision design system.

Outputs:
  ZH:
    - pdf/Jun-Hsiang-Enterprise-Company-Profile-ZH.pdf
    - pdf/Jun-Hsiang-Enterprise-Company-Profile-ZH.pptx
    - scratch/presentation_previews/zh-slide-1.png .. zh-slide-7.png
  JA:
    - pdf/ja/Jun-Hsiang-Enterprise-Company-Profile-JA.pdf
    - pdf/ja/Jun-Hsiang-Enterprise-Company-Profile-JA.pptx
    - scratch/presentation_previews/ja-slide-1.png .. ja-slide-7.png
"""

import base64
import subprocess
from pathlib import Path
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

WORKSPACE = Path("p:/tets")
IMAGES_DIR = WORKSPACE / "images" / "brochure"
LOGO_FILE = WORKSPACE / "images" / "logo.png"
PREVIEWS_DIR = WORKSPACE / "scratch" / "presentation_previews"
PREVIEWS_DIR.mkdir(parents=True, exist_ok=True)
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def b64_img(file_path):
    p = Path(file_path)
    if not p.exists():
        return ""
    ext = p.suffix.lower().lstrip(".")
    mime = "image/png" if ext == "png" else ("image/webp" if ext == "webp" else "image/jpeg")
    data = base64.b64encode(p.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


ASSETS = {
    "logo": b64_img(LOGO_FILE),
    "keypads": b64_img(IMAGES_DIR / "prod-keypads.jpg"),
    "orings": b64_img(IMAGES_DIR / "prod-orings.jpg"),
    "gaskets": b64_img(IMAGES_DIR / "prod-gaskets.jpg"),
    "medkb": b64_img(IMAGES_DIR / "prod-medical-kb.jpg"),
    "lsr": b64_img(IMAGES_DIR / "equip-lsr.jpg"),
    "vac": b64_img(IMAGES_DIR / "equip-vacuum-press.jpg"),
    "opt25d": b64_img(IMAGES_DIR / "qc-25d-optical.jpg"),
    "load": b64_img(IMAGES_DIR / "qc-load-curve.jpg"),
}


# =====================================================================
# LANGUAGE CONTENT DEFINITIONS (Strict Rule 2, 5, 8, 11, 15 Compliance)
# =====================================================================
LANG_DATA = {
    "zh": {
        "lang_attr": "zh-Hant",
        "font_stack": '"Microsoft JhengHei", "PingFang TC", "Noto Sans CJK TC", -apple-system, BlinkMacSystemFont, sans-serif',
        "pptx_font": "Microsoft JhengHei",
        "pdf_out": WORKSPACE / "pdf" / "Jun-Hsiang-Enterprise-Company-Profile-ZH.pdf",
        "pptx_out": WORKSPACE / "pdf" / "Jun-Hsiang-Enterprise-Company-Profile-ZH.pptx",
        "doc_title": "鈞翔實業有限公司 — 矽膠與橡膠精密製造能力簡介",
        "brand_name": "鈞翔實業有限公司",
        "brand_short": "鈞翔實業",
        "brand_sub": "台灣精密矽膠・橡膠 OEM／ODM 製造廠",
        "footer_left": "鈞翔實業有限公司 ・ 客製化矽膠與橡膠精密成型製造廠",
        # Slide 1
        "s1_kicker": "企業製造能力簡介",
        "s1_h1_line1": "精密矽膠與橡膠",
        "s1_h1_em": "客製成型製造",
        "s1_desc": "專精液態矽膠（LSR）射出、抽真空固態熱壓成型，以及矽膠包鐵／包塑膠異材結合。自 1991 年深耕台灣新莊，提供從 2D／3D 圖面 DFM 評估、模具開發至穩定外銷量產之一條龍代工服務。",
        "s1_meta": [
            ("創立年份", "1991 年 9 月（35+ 年）"),
            ("品質系統", "ISO 9001:2015 認證"),
            ("製造基地", "100% 台灣在地製造"),
        ],
        "s1_gallery_title": "廠內核心設備與實績精選",
        "s1_fig1": "立式 LSR 液態矽膠射出機 — MIV 1500-LS",
        "s1_fig2": "客製化矽膠／橡膠 O-Ring 與密封件",
        # Slide 2
        "s2_kicker": "01 — 公司簡介與經營理念",
        "s2_title": "深耕台灣 35 年的精密橡矽膠模具與成型實力",
        "s2_year_sub": "創立於台灣新北市新莊區",
        "s2_facts": [
            ("公司名稱", "鈞翔實業有限公司"),
            ("實收資本額", "新台幣 12,000,000 元"),
            ("廠房地址", "新北市新莊區新樹路 345 巷 1、3 號"),
            ("品質認證", "ISO 9001:2015 品質管理系統"),
            ("服務市場", "台灣、北美、歐洲、日本 OEM／ODM"),
            ("供應鏈優勢", "非中國製造・支援打樣與彈性量產"),
        ],
        "s2_intro": "秉持 <strong>F.H.P.Q. 四大核心精神</strong>，協助研發與採購團隊從早期 DFM 可製造性評估、模具結構設計一路推進至量產穩定交付。",
        "s2_fhpq": [
            ("01", "Friend — 研發夥伴思維", "開模前主動回饋分模線、拔模角、倒勾脫模與材料選型建議，與客戶工程團隊共同排除量產風險。"),
            ("02", "Honesty — 誠信與模具權保障", "嚴格守護客戶專屬模具所有權與 NDA 機密規範，透明提供原料合規檢驗文件。"),
            ("03", "Profession — 廠內垂直整合", "涵蓋廠內煉膠、LSR 液態射出、抽真空熱壓、網版印刷、雷射雕刻與二次硫化烘烤製程。"),
            ("04", "Quality — 品質三不原則", "嚴格落實「不接受、不製造、不流出不良品」，搭配 2.5D 光學量測與荷重曲線檢驗把關。"),
        ],
        # Slide 3
        "s3_kicker": "02 — 核心製造工藝與材料矩陣",
        "s3_title": "三大精密成型製程與客製化彈性體材料",
        "s3_procs": [
            ("01", "LSR 液態矽膠射出成型", "採用密閉式 A/B 劑精密計量射出系統，適合複雜幾何結構、高潔淨度與醫療級應用。",
             ["廠內配置川連 MIV 1500-LS 立式 LSR 射出機", "支援冷流道與低毛邊精密模具結構", "適用醫療面罩、精密閥片與光學防水密封件", "批次硫化穩定度高，適合中大批量長期供貨"], True),
            ("02", "抽真空固態熱壓成型", "高噸位油壓熱壓機台搭配真空抽氣腔體，專攻固態矽膠（HCR）與各類特種工業橡膠。",
             ["合模前真空抽氣，大幅降低氣泡與包風缺陷", "模具開發成本具彈性，兼顧打樣與量產需求", "適用導電按鍵、O-Ring、大型防水框墊與減震腳墊", "支援 Shore A 10 至 90 客製硬度與配色調膠"], False),
            ("03", "異材包覆與埋入結合", "將矽膠或橡膠透過底塗處理與加熱硫化，直接緊密包覆於金屬件或耐溫工程塑膠上。",
             ["支援不鏽鋼、鋁合金、銅件等金屬埋入包膠", "支援 PC、PBT、PA 尼龍與 PEEK 塑膠異材結合", "嚴格控管表面前處理與接著劑塗佈工藝", "減少人工組裝工序並提升防水氣密結構強度"], False),
        ],
        "s3_mat_label": "可加工<br/>彈性體材料",
        "s3_mats": [
            ("LSR", "醫療與精密液態矽膠"),
            ("VMQ", "FDA／LFGB 食品級矽膠"),
            ("FKM", "氟橡膠（耐化學耐高溫）"),
            ("FVMQ", "氟矽膠（耐油耐溶劑）"),
            ("EPDM", "耐候耐蒸氣橡膠"),
            ("NBR / CR", "工業耐油密封橡膠"),
        ],
        "s3_footer": "可依產品需求搭配 RoHS 2.0、REACH、FDA 21 CFR 177.2600 與 LFGB 合規原料配方",
        # Slide 4
        "s4_kicker": "03 — 客製化產品實績",
        "s4_title": "依圖面開發之精密橡矽膠零件",
        "s4_cards": [
            ("keypads", "人機介面與按鍵", "導電矽膠按鍵與遙控按鍵",
             ["導電碳粒印刷與鍍金接點客製規格", "多色網版印刷與背光雷射雕刻工藝", "PU 霧面、耐磨塗層與環氧樹脂滴膠保護"],
             "應用領域：工業控制器、POS 終端機、醫療設備面板"),
            ("orings", "流體與高壓密封", "客製 O-Ring 與精密油封",
             ["支援 AS568、JIS B2401 與非標異形截面開模", "寬溫域耐受表現（-50°C 至 +250°C 視材質）", "低壓縮永久變形配方，確保長期氣密防水"],
             "應用領域：車用防水接頭、流體閥件、幫浦與管路密封"),
            ("medkb", "醫療與潔淨室", "醫療級可水洗矽膠鍵盤",
             ["一體成型無縫防水表面，阻隔液體與粉塵滲入", "耐受醫院級酒精與消毒劑反覆擦拭清潔", "採用生物相容性與食品級矽膠配方製造"],
             "應用領域：醫院護理車、牙科診療室、無塵室工作站"),
            ("gaskets", "戶外機殼防護", "精密防水框墊與異形密封圈",
             ["支援複雜 3D 外框輪廓與多道防水肋條結構", "對應 IP67／IP68 戶外防水防塵機殼需求", "可選配自潤滑矽膠或 EMI 導電屏蔽橡膠"],
             "應用領域：戶外通訊機殼、無人機、工業感測器外殼"),
        ],
        "s4_footer": "本頁所有產品照片均為鈞翔實業台灣廠區實際量產之真實成品拍攝",
        # Slide 5
        "s5_kicker": "04 — 廠內生產設備與後加工線",
        "s5_title": "台灣廠內成型機台與完整後段製程",
        "s5_equips": [
            ("lsr", "液態射出成型系統", "立式 LSR 液態矽膠射出機",
             "配置川連 MIV 1500-LS 立式鎖模系統，特別適合金屬／塑膠埋入件定位與高精密液態矽膠成型。",
             ["密閉式 A/B 雙劑精密計量與靜態混合送料", "立式台面設計便於異材嵌件穩定放置", "微細結構充模均勻，確保批次尺寸一致性"]),
            ("vac", "固態橡矽膠成型產線", "抽真空油壓熱壓成型機群",
             "高噸位熱壓機台整合真空抽氣罩結構，於硫化加壓前排除模腔殘留空氣，提升成品緻密度。",
             ["合模前強制抽真空，有效抑制包風與缺料", "多區溫控熱板維持大型模具均勻硫化品質", "涵蓋精密按鍵、大面積防水框墊與減震墊片"]),
        ],
        "s5_sec_title": "廠內一貫化前後段設備",
        "s5_sec_items": ["雙滾輪煉膠機", "三滾輪油墨研磨機", "平面網版印刷線", "紅外線隧道烘乾爐", "二次硫化恆溫烤箱"],
        "s5_footer": "從原料混煉、成型硫化到印刷烘烤全程廠內掌控，交期與品質穩定透明",
        # Slide 6
        "s6_kicker": "05 — 品質保證與精密量測實驗室",
        "s6_title": "非接觸光學量測與動態力學檢驗把關",
        "s6_qas": [
            ("opt25d", "精密尺寸量測", "HO STAR 2.5D 光學量測儀",
             "採用非接觸式光學影像邊緣偵測，避免傳統接觸式量具壓迫軟質彈性體造成誤差，精準核對內外徑與 2D 輪廓公差。"),
            ("load", "按鍵手感與壽命測試", "AIKOH 動態荷重曲線測試機",
             "完整量測按鍵按壓力與行程曲線（峰值力、回彈力、觸感比），並搭配廠內耐磨耗與按鍵壽命測試機進行可靠度驗證。"),
        ],
        "s6_proto_kicker": "ISO 9001:2015 品管流程",
        "s6_proto_title": "五段式品質檢驗關卡",
        "s6_gates": [
            ("01", "進料原料檢驗（IQC）", "核對硬度（Shore A）、批次追溯編號與供應商 RoHS／REACH／FDA 報告。"),
            ("02", "首件尺寸檢驗（FAI）", "T1 試模樣品均以 2.5D 光學儀量測並出具檢驗報告，供客戶工程承認。"),
            ("03", "製程巡迴檢驗（IPQC）", "定時抽檢硫化狀態、毛邊控制、分模線對位與外觀瑕疵。"),
            ("04", "功能與表面耐久測試", "執行荷重手感曲線、表面耐磨、酒精擦拭測試與二次烘烤去揮發物。"),
            ("05", "出貨抽驗與報告交付（OQC）", "完成批號抽檢與外觀全檢把關，隨貨提供檢驗紀錄與出廠證明。"),
        ],
        "s6_iso_note": "正式詢價時可提供最新有效之 ISO 9001:2015 證書與 SGS 原料檢驗報告。",
        "s6_footer": "廠內獨立品保實驗室嚴格把關，確保每一批出貨符合客戶圖面與裝配規範",
        # Slide 7
        "s7_kicker": "06 — 開發流程與快速詢價窗口",
        "s7_title": "從 2D／3D 圖面評估到穩定交貨",
        "s7_steps": [
            ("01", "圖面審查與 DFM", "簽署 NDA 後審查拔模角、分模線、肉厚與倒勾脫模可行性。"),
            ("02", "材料選型與報價", "確認材質、Shore A 硬度、開模費用與各階量產單價。"),
            ("03", "開模製造與 T1 打樣", "CNC／放電精密加工開模，完成 T1 試模並附 2.5D 量測報告。"),
            ("04", "承認與正式量產", "客戶裝配測試承認後進入真空硫化、二次烘烤與品保出貨。"),
            ("05", "彈性交貨與外銷", "支援台灣在地配送與空海運直送歐美日客戶端。"),
        ],
        "s7_rfq_kicker": "快速工程報價指南",
        "s7_rfq_title": "詢價圖面準備清單",
        "s7_rfq_items": [
            "2D 工程圖（含關鍵公差標註）",
            "3D 圖檔（STEP / IGES / STP）",
            "指定材質與 Shore A 硬度",
            "使用溫度與接觸介質環境",
            "顏色要求（Pantone / RAL）",
            "預計打樣數量與年需求量",
        ],
        "s7_headline": "歡迎直接寄送 2D／3D 圖面，由工程團隊為您進行製程評估與報價。",
        "s7_contacts": [
            ("聯絡窗口", "許先生（工程開發與業務）", False),
            ("電子信箱", "andy_hsu@jun-hsiang.com.tw", True),
            ("連絡電話", "(02) 2203-9918 （傳真：(02) 2206-6968）", False),
            ("官方 LINE", "@682wvagy （台灣專案快速傳圖聯繫）", False),
            ("廠房地址", "242 新北市新莊區新樹路 345 巷 1、3 號", False),
            ("官方網站", "https://www.jun-hsiang.com.tw/", False),
        ],
        "s7_footer": "鈞翔實業有限公司 ・ 傳圖前可配合簽署雙方保密協議（NDA）",
    },

    "ja": {
        "lang_attr": "ja",
        "font_stack": '"Yu Gothic UI", "Meiryo", "Hiragino Kaku Gothic ProN", -apple-system, sans-serif',
        "pptx_font": "Yu Gothic UI",
        "pdf_out": WORKSPACE / "pdf" / "ja" / "Jun-Hsiang-Enterprise-Company-Profile-JA.pdf",
        "pptx_out": WORKSPACE / "pdf" / "ja" / "Jun-Hsiang-Enterprise-Company-Profile-JA.pptx",
        "doc_title": "鈞翔実業有限公司 — 精密シリコーン・ゴム成形 会社案内",
        "brand_name": "鈞翔実業有限公司",
        "brand_short": "鈞翔実業",
        "brand_sub": "台湾 精密シリコーン・ゴム OEM／ODM メーカー",
        "footer_left": "鈞翔実業有限公司 ・ 精密シリコーン・ゴム成形メーカー（台湾）",
        # Slide 1
        "s1_kicker": "会社案内・製造能力プロファイル",
        "s1_h1_line1": "精密シリコーン・ゴム",
        "s1_h1_em": "カスタム成形技術",
        "s1_desc": "液状シリコーン（LSR）射出成形、真空圧縮成形、および金属・樹脂インサート一体成形を専門とする台湾メーカー。1991年の創業以来、2D／3D図面のDFM検討から金型製作、試作・量産輸出まで一貫対応いたします。",
        "s1_meta": [
            ("設立", "1991年9月（創業35年以上）"),
            ("品質規格", "ISO 9001:2015 認証取得"),
            ("生産拠点", "100% 台湾自社工場生産"),
        ],
        "s1_gallery_title": "主要設備・製造実績ハイライト",
        "s1_fig1": "竪型 LSR 液状シリコーン射出成形機 — MIV 1500-LS",
        "s1_fig2": "カスタム Oリング・精密シール部品",
        # Slide 2
        "s2_kicker": "01 — 会社概要・経営理念",
        "s2_title": "台湾で35年以上培った精密エラストマー成形技術",
        "s2_year_sub": "台湾・新北市新荘区にて創業",
        "s2_facts": [
            ("社名", "鈞翔実業有限公司"),
            ("資本金", "12,000,000 台湾ドル"),
            ("工場所在地", "242 台湾新北市新荘区新樹路345巷1・3号"),
            ("品質マネジメント", "ISO 9001:2015 認証取得"),
            ("主要輸出先", "日本・北米・欧州およびグローバルOEM"),
            ("サプライチェーン", "脱中国リスク・台湾一貫生産体制"),
        ],
        "s2_intro": "<strong>F.H.P.Q. の品質理念</strong>に基づき、設計段階のDFM提案から金型製作、T1試作検証、量産納入までお客様の技術パートナーとして伴走します。",
        "s2_fhpq": [
            ("01", "Friend — 技術パートナーシップ", "金型着工前にパーティングライン、抜き勾配、アンダーカット離型性、材料選定について具体的なDFM提案を実施します。"),
            ("02", "Honesty — 誠実な金型管理と透明性", "お客様の金型所有権と機密保持（NDA）を厳守し、材料の各種環境規制証明書類を透明性高く提供します。"),
            ("03", "Profession — 社内一貫製造体制", "材料練りからLSR射出、真空圧縮、シルク印刷、レーザー刻印、二次加硫（ポストキュア）まで社内で完結します。"),
            ("04", "Quality — 不良品三原則の徹底", "「受け取らない・作らない・流さない」を徹底し、2.5D光学測定機や荷重曲線試験機により品質を保証します。"),
        ],
        # Slide 3
        "s3_kicker": "02 — コア成形技術と対応材料",
        "s3_title": "3つの精密成形プロセスと対応エラストマー",
        "s3_procs": [
            ("01", "LSR 液状シリコーン射出成形", "密閉式A/B液計量射出システムにより、複雑形状・医療機器・光学部品向けの高精度成形を実現します。",
             ["竪型LSR射出成形機（MIV 1500-LS）を保有", "バリを抑えたコールドランナー金型設計に対応", "医療用マスク、精密バルブ、光学防水シールに最適", "ロット間の加硫ばらつきが少なく安定量産が可能"], True),
            ("02", "真空圧縮成形（コンプレッション）", "高圧油圧プレスと真空チャンバーを組み合わせ、ミラブルシリコーン（HCR）や特殊合成ゴムを精密成形します。",
             ["型締め前の真空引きにより気泡・ボイドを抑制", "試作から中量産まで金型コストを最適化", "導電キーパッド、Oリング、大型ガスケットに対応", "Shore A 10〜90 のカスタム硬度・調色に対応"], False),
            ("03", "インサート一体成形（異材接合）", "金属部品や耐熱エンジニアリングプラスチックへ、プライマー処理と加熱加硫でシリコーンを強固に接合します。",
             ["ステンレス、アルミ、真鍮など金属インサート対応", "PC、PBT、PA、PEEK などの耐熱樹脂基材に対応", "前処理・接着剤塗布工程を厳格に管理", "組立て工数の削減と高い防水・気密性を両立"], False),
        ],
        "s3_mat_label": "対応可能<br/>ゴム・シリコーン",
        "s3_mats": [
            ("LSR", "医療・光学用液状シリコーン"),
            ("VMQ", "FDA／LFGB 適合シリコーン"),
            ("FKM", "フッ素ゴム（耐薬品・耐熱）"),
            ("FVMQ", "フロロシリコーン（耐油）"),
            ("EPDM", "耐候・耐スチームゴム"),
            ("NBR / CR", "工業用耐油シールゴム"),
        ],
        "s3_footer": "RoHS 2.0、REACH、FDA 21 CFR 177.2600、LFGB 適合材料での製造に対応可能です",
        # Slide 4
        "s4_kicker": "03 — カスタム製品ポートフォリオ",
        "s4_title": "図面仕様に基づく精密シリコーン・ゴム部品",
        "s4_cards": [
            ("keypads", "HMI・操作インターフェース", "導電性シリコーンキーパッド",
             ["カーボン接点・金接点など各種導電仕様に対応", "多色シルク印刷およびバックライト用レーザー刻印", "PUマット・耐摩耗コート・エポキシ樹脂コーティング"],
             "用途：産業用コントローラ、POS端末、医療機器操作盤"),
            ("orings", "流体・高圧シール", "カスタム Oリング・精密オイルシール",
             ["AS568・JIS B2401 規格および特注断面形状に対応", "幅広い温度範囲（-50°C〜+250°C ※材質による）", "低圧縮永久ひずみ配合により長期シール性を確保"],
             "用途：車載防水コネクタ、流体バルブ、ポンプ部品"),
            ("medkb", "医療・クリーンルーム", "医療用ウォッシャブルキーボード",
             ["継ぎ目のない完全防水カバー構造で液体侵入を防止", "医療用アルコール・消毒剤による清拭に高い耐性", "生体適合性・食品衛生適合シリコーン材料を採用"],
             "用途：病院内カート、歯科診療室、クリーンルーム端末"),
            ("gaskets", "筐体防水・保護", "精密フレームガスケット・防水パッキン",
             ["複雑な3D外周形状および多段防水リブ構造に対応", "IP67／IP68 屋外筐体の防水・防塵設計をサポート", "自己潤滑シリコーンやEMI導電シールド配合も対応"],
             "用途：屋外通信筐体、ドローン、産業用センサハウジング"),
        ],
        "s4_footer": "掲載写真はすべて台湾・鈞翔実業の自社工場にて製造した実物製品です",
        # Slide 5
        "s5_kicker": "04 — 生産設備および二次加工ライン",
        "s5_title": "台湾自社工場の成形設備と一貫後加工体制",
        "s5_equips": [
            ("lsr", "液状射出成形システム", "竪型 LSR 液状シリコーン射出機",
             "川連製 MIV 1500-LS 竪型型締機構を採用。金属・樹脂インサート品のセット性と微細液状成形に優れます。",
             ["密閉式A/B二液計量・スタティックミキシング供給", "竪型構造によりインサート部品を安定配置", "微細形状への高い充填性とロット均一性を実現"]),
            ("vac", "固形ゴム成形ライン", "真空圧縮成形プレス群",
             "真空チャンバー一体型の油圧プレス機群により、加硫時のエア噛みを防ぎ緻密な成形品を実現します。",
             ["型締め前の真空排気によりエア溜まり・欠肉を防止", "精密温度制御熱板による均一な加硫品質", "大型フレームガスケットからキーパッドまで幅広く対応"]),
        ],
        "s5_sec_title": "社内保有の前後工程設備",
        "s5_sec_items": ["2本ロール練り機", "3本ロールインキ練肉機", "平面シルク印刷ライン", "IRコンベア乾燥炉", "二次加硫恒温オーブン"],
        "s5_footer": "材料混練から成形、印刷、二次加硫まで社内一貫管理により短納期と安定品質を実現",
        # Slide 6
        "s6_kicker": "05 — 品質保証・精密測定ラボ",
        "s6_title": "非接触光学測定と動的荷重試験による品質検証",
        "s6_qas": [
            ("opt25d", "精密寸法測定", "HO STAR 2.5D 光学画像測定機",
             "非接触光学エッジ検出により軟質ゴムの測定変形を防ぎ、2D図面に基づく内径・外径・輪郭公差を精確に検証します。"),
            ("load", "荷重・耐久試験", "AIKOH 動的荷重曲線試験機",
             "押下荷重とストローク曲線（ピーク荷重・戻り荷重・クリック率）を測定。耐摩耗試験機・打鍵寿命試験機も社内完備。"),
        ],
        "s6_proto_kicker": "ISO 9001:2015 品質管理プロセス",
        "s6_proto_title": "5段階 品質検査ゲート",
        "s6_gates": [
            ("01", "受入材料検査（IQC）", "硬度（Shore A）、ロットトレーサビリティ、RoHS／REACH／FDA書類を確認。"),
            ("02", "初品検査（FAI）", "T1試作品を2.5D光学測定機で全項目測定し、検査成績書を提出します。"),
            ("03", "工程内巡回検査（IPQC）", "加硫状態、バリ管理、パーティングラインずれ、外観品質を定期検査。"),
            ("04", "機能・表面耐久評価", "荷重曲線試験、耐摩耗・アルコール拭取り試験、二次加硫揮発分除去を実施。"),
            ("05", "出荷検査・証明書発行（OQC）", "最終抜取検査および外観検査を経て、検査成績書・適合証明書を添付出荷。"),
        ],
        "s6_iso_note": "最新のISO 9001:2015認証書およびSGS材料試験報告書はお見積り時に提示可能です。",
        "s6_footer": "社内品質保証ラボでの厳格な検証を経て台湾より出荷いたします",
        # Slide 7
        "s7_kicker": "06 — 開発フロー・お問い合わせ窓口",
        "s7_title": "図面受領からグローバル納品までの流れ",
        "s7_steps": [
            ("01", "図面確認・DFM検討", "NDA締結後、抜き勾配・分割線・肉厚・離型性を技術検証。"),
            ("02", "材料選定・お見積り", "材質・Shore A硬度を選定し、金型費と数量別単価を提示。"),
            ("03", "金型製作・T1試作", "CNC・放電加工で金型製作後、T1試作と2.5D測定報告書を提出。"),
            ("04", "評価承認・量産移行", "組付け評価承認後、真空加硫・二次加硫・品質検査を経て量産。"),
            ("05", "日本・海外へ直接出荷", "台湾より航空便・海上便にて必要書類一式と共にお届け。"),
        ],
        "s7_rfq_kicker": "迅速なお見積りのために",
        "s7_rfq_title": "お見積り依頼時チェックリスト",
        "s7_rfq_items": [
            "2D図面（重要公差の記載）",
            "3D CADデータ（STEP / IGES）",
            "希望材質および Shore A 硬度",
            "使用温度範囲・接触薬品／環境",
            "色指定（Pantone / RAL 等）",
            "試作数量および年間予定数量",
        ],
        "s7_headline": "2D／3D図面をお送りいただければ、技術担当より成形可否とお見積りをご回答いたします。",
        "s7_contacts": [
            ("担当窓口", "許（Andy Hsu）— 技術営業・海外担当", False),
            ("メール", "andy_hsu@jun-hsiang.com.tw", True),
            ("電話番号", "+886-2-2203-9918 （FAX: +886-2-2206-6968）", False),
            ("工場所在地", "242 台湾新北市新荘区新樹路345巷1・3号", False),
            ("Webサイト", "https://www.jun-hsiang.com.tw/ja/", False),
        ],
        "s7_footer": "鈞翔実業有限公司 ・ 図面送付前の秘密保持契約（NDA）締結に対応しております",
    },
}


def build_css(font_stack):
    return f"""
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  @page {{ size: 1920px 1080px; margin: 0; }}
  html, body {{
    width: 1920px; background: #FFFFFF;
    font-family: {font_stack};
    color: #111827;
    -webkit-font-smoothing: antialiased;
    -webkit-print-color-adjust: exact; print-color-adjust: exact;
  }}
  .slide {{
    width: 1920px; height: 1080px; position: relative;
    overflow: hidden; page-break-after: always; background: #FFFFFF;
  }}
  .slide:last-child {{ page-break-after: auto; }}
  .kicker {{ font-size: 14px; font-weight: 700; letter-spacing: 2.5px; color: #A67C2E; }}
  .section-h2 {{ font-size: 42px; font-weight: 700; letter-spacing: -0.3px; line-height: 1.2; color: #0E131B; }}
  .light-slide {{ background: #FFFFFF; padding: 62px 96px 54px 96px; display: flex; flex-direction: column; justify-content: space-between; }}
  .warm-slide {{ background: #F6F6F3; padding: 62px 96px 54px 96px; display: flex; flex-direction: column; justify-content: space-between; }}
  .top-bar {{ display: flex; justify-content: space-between; align-items: flex-end; padding-bottom: 22px; border-bottom: 1px solid #E2E5EA; }}
  .top-bar-left {{ display: flex; flex-direction: column; gap: 10px; }}
  .top-bar-brand {{ display: flex; align-items: center; gap: 14px; font-size: 14px; font-weight: 700; letter-spacing: 2px; color: #64748B; }}
  .top-bar-brand img {{ height: 30px; width: auto; }}
  .bottom-bar {{ display: flex; justify-content: space-between; align-items: center; padding-top: 20px; border-top: 1px solid #E2E5EA; font-size: 14px; color: #6B7280; }}
  .page-num {{ font-variant-numeric: tabular-nums; font-weight: 700; color: #0E131B; letter-spacing: 2px; }}

  /* SLIDE 1 */
  .cover-slide {{ display: grid; grid-template-columns: 1120px 800px; width: 1920px; height: 1080px; }}
  .cover-left {{ background: #0E131B; color: #FFFFFF; padding: 72px 96px 64px 96px; display: flex; flex-direction: column; justify-content: space-between; }}
  .cover-brand {{ display: flex; align-items: center; gap: 18px; }}
  .cover-brand img {{ height: 46px; width: auto; }}
  .cover-brand-text {{ display: flex; flex-direction: column; gap: 3px; }}
  .cover-brand-name {{ font-size: 20px; font-weight: 700; letter-spacing: 2px; color: #FFFFFF; }}
  .cover-brand-sub {{ font-size: 13px; letter-spacing: 1.5px; color: #9CA3AF; }}
  .cover-main {{ display: flex; flex-direction: column; gap: 28px; margin: auto 0; }}
  .cover-kicker {{ font-size: 15px; font-weight: 700; letter-spacing: 3px; color: #D4AA55; }}
  .cover-h1 {{ font-size: 66px; font-weight: 700; line-height: 1.18; letter-spacing: 0.5px; color: #FFFFFF; }}
  .cover-h1 em {{ font-style: normal; color: #E5C178; }}
  .cover-desc {{ font-size: 20px; font-weight: 400; line-height: 1.7; color: #CBD5E1; max-width: 860px; }}
  .cover-meta-strip {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px; padding-top: 32px; border-top: 1px solid rgba(255,255,255,0.14); }}
  .cover-meta-label {{ font-size: 12px; font-weight: 700; letter-spacing: 2px; color: #9CA3AF; margin-bottom: 6px; }}
  .cover-meta-val {{ font-size: 18px; font-weight: 600; color: #FFFFFF; }}
  .cover-right {{ background: #F6F6F3; padding: 56px 64px; display: flex; flex-direction: column; justify-content: space-between; }}
  .cover-gallery-top {{ display: flex; justify-content: space-between; align-items: center; font-size: 13px; font-weight: 700; letter-spacing: 2px; color: #6B7280; padding-bottom: 18px; border-bottom: 1px solid #DCDFE4; }}
  .cover-figure {{ background: #FFFFFF; border: 1px solid #E5E7EB; padding: 24px; display: flex; flex-direction: column; justify-content: space-between; }}
  .cover-figure-lg {{ height: 440px; }}
  .cover-figure-sm {{ height: 360px; }}
  .cover-figure img {{ width: 100%; height: calc(100% - 36px); object-fit: contain; mix-blend-mode: multiply; }}
  .fig-caption {{ display: flex; justify-content: space-between; align-items: center; padding-top: 12px; border-top: 1px solid #F0F1F4; font-size: 13px; font-weight: 600; color: #4B5563; }}
  .fig-caption span {{ color: #A67C2E; letter-spacing: 1px; }}

  /* SLIDE 2 */
  .s2-body {{ display: grid; grid-template-columns: 560px 1fr; gap: 68px; flex: 1; padding: 40px 0 26px 0; }}
  .facts-panel {{ background: #F6F6F3; padding: 38px 42px; display: flex; flex-direction: column; justify-content: space-between; }}
  .big-stat-row {{ display: flex; align-items: baseline; gap: 18px; padding-bottom: 24px; border-bottom: 1px solid #DCDFE4; }}
  .big-stat-num {{ font-family: Georgia, serif; font-size: 82px; line-height: 0.95; color: #0E131B; }}
  .big-stat-text {{ font-size: 18px; font-weight: 600; line-height: 1.4; color: #374151; }}
  .fact-table {{ display: flex; flex-direction: column; }}
  .fact-row {{ display: flex; justify-content: space-between; align-items: baseline; padding: 15px 0; border-bottom: 1px solid #E2E5EA; gap: 16px; }}
  .fact-row:last-child {{ border-bottom: none; }}
  .fact-key {{ font-size: 13.5px; font-weight: 700; color: #6B7280; white-space: nowrap; }}
  .fact-val {{ font-size: 15.5px; font-weight: 600; color: #111827; text-align: right; }}
  .fhpq-panel {{ display: flex; flex-direction: column; justify-content: space-between; }}
  .fhpq-intro {{ font-size: 22px; font-weight: 400; line-height: 1.6; color: #1F2937; padding-bottom: 26px; border-bottom: 1px solid #E2E5EA; }}
  .fhpq-intro strong {{ color: #0E131B; font-weight: 700; }}
  .fhpq-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 34px 44px; padding-top: 30px; flex: 1; }}
  .fhpq-item {{ display: flex; flex-direction: column; gap: 10px; }}
  .fhpq-num {{ font-family: Georgia, serif; font-size: 28px; color: #A67C2E; line-height: 1; }}
  .fhpq-title {{ font-size: 21px; font-weight: 700; color: #0E131B; }}
  .fhpq-desc {{ font-size: 16px; line-height: 1.65; color: #4B5563; }}

  /* SLIDE 3 */
  .s3-body {{ display: flex; flex-direction: column; justify-content: space-between; flex: 1; padding: 34px 0 22px 0; gap: 28px; }}
  .process-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px; flex: 1; }}
  .process-col {{ background: #FFFFFF; border: 1px solid #E2E5EA; padding: 36px 34px; display: flex; flex-direction: column; justify-content: space-between; }}
  .process-col-featured {{ background: #0E131B; border-color: #0E131B; color: #FFFFFF; }}
  .proc-index {{ font-family: Georgia, serif; font-size: 38px; color: #A67C2E; line-height: 1; margin-bottom: 16px; }}
  .process-col-featured .proc-index {{ color: #D4AA55; }}
  .proc-title {{ font-size: 24px; font-weight: 700; line-height: 1.3; margin-bottom: 14px; color: #0E131B; }}
  .process-col-featured .proc-title {{ color: #FFFFFF; }}
  .proc-summary {{ font-size: 15.5px; line-height: 1.65; color: #4B5563; margin-bottom: 20px; }}
  .process-col-featured .proc-summary {{ color: #CBD5E1; }}
  .proc-list {{ list-style: none; display: flex; flex-direction: column; gap: 11px; padding-top: 20px; border-top: 1px solid #E5E7EB; font-size: 15px; line-height: 1.45; color: #374151; }}
  .process-col-featured .proc-list {{ border-top-color: rgba(255,255,255,0.14); color: #E2E8F0; }}
  .proc-list li {{ padding-left: 18px; position: relative; }}
  .proc-list li::before {{ content: ""; position: absolute; left: 0; top: 10px; width: 6px; height: 1.5px; background: #A67C2E; }}
  .process-col-featured .proc-list li::before {{ background: #D4AA55; }}
  .material-strip {{ background: #FFFFFF; border: 1px solid #E2E5EA; padding: 22px 34px; display: grid; grid-template-columns: 200px repeat(6, 1fr); align-items: center; gap: 18px; }}
  .mat-label {{ font-size: 14px; font-weight: 700; color: #0E131B; border-right: 1px solid #E2E5EA; padding-right: 18px; line-height: 1.4; }}
  .mat-item {{ display: flex; flex-direction: column; gap: 4px; }}
  .mat-code {{ font-size: 17px; font-weight: 700; color: #0E131B; }}
  .mat-desc {{ font-size: 13px; color: #6B7280; }}

  /* SLIDE 4 */
  .s4-body {{ display: grid; grid-template-columns: 1fr 1fr; gap: 34px; flex: 1; padding: 32px 0 22px 0; }}
  .prod-col {{ display: flex; flex-direction: column; gap: 26px; }}
  .prod-card-horiz {{ background: #F6F6F3; border: 1px solid #E5E7EB; display: grid; grid-template-columns: 330px 1fr; flex: 1; overflow: hidden; }}
  .prod-photo-stage {{ background: #FFFFFF; padding: 20px; display: flex; align-items: center; justify-content: center; border-right: 1px solid #E5E7EB; }}
  .prod-photo-stage img {{ max-width: 100%; max-height: 295px; object-fit: contain; mix-blend-mode: multiply; }}
  .prod-info {{ padding: 26px 30px; display: flex; flex-direction: column; justify-content: space-between; }}
  .prod-tag {{ font-size: 12px; font-weight: 700; letter-spacing: 1.5px; color: #A67C2E; margin-bottom: 6px; }}
  .prod-title {{ font-size: 22px; font-weight: 700; color: #0E131B; line-height: 1.3; margin-bottom: 12px; }}
  .prod-bullets {{ list-style: none; display: flex; flex-direction: column; gap: 8px; font-size: 14.5px; line-height: 1.5; color: #4B5563; }}
  .prod-bullets li {{ padding-left: 16px; position: relative; }}
  .prod-bullets li::before {{ content: ""; position: absolute; left: 0; top: 10px; width: 6px; height: 1.5px; background: #A67C2E; }}
  .prod-app {{ font-size: 13px; font-weight: 600; color: #374151; padding-top: 12px; border-top: 1px solid #E2E5EA; }}

  /* SLIDE 5 */
  .s5-body {{ display: flex; flex-direction: column; justify-content: space-between; flex: 1; padding: 32px 0 22px 0; gap: 26px; }}
  .equip-grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 38px; flex: 1; }}
  .equip-feature {{ background: #FFFFFF; border: 1px solid #E2E5EA; display: grid; grid-template-columns: 370px 1fr; overflow: hidden; }}
  .equip-img-stage {{ background: #FFFFFF; padding: 24px; display: flex; align-items: center; justify-content: center; border-right: 1px solid #ECEEF2; }}
  .equip-img-stage img {{ max-width: 100%; max-height: 465px; object-fit: contain; }}
  .equip-detail {{ padding: 34px 34px; display: flex; flex-direction: column; justify-content: space-between; }}
  .equip-title {{ font-size: 26px; font-weight: 700; color: #0E131B; line-height: 1.3; margin: 10px 0 14px 0; }}
  .equip-desc {{ font-size: 15.5px; line-height: 1.65; color: #4B5563; margin-bottom: 18px; }}
  .secondary-strip {{ background: #0E131B; color: #FFFFFF; padding: 22px 36px; display: flex; justify-content: space-between; align-items: center; }}
  .sec-strip-title {{ font-size: 14px; font-weight: 700; letter-spacing: 2px; color: #D4AA55; }}
  .sec-strip-items {{ display: flex; gap: 34px; font-size: 15.5px; font-weight: 500; color: #E5E7EB; }}

  /* SLIDE 6 */
  .s6-body {{ display: grid; grid-template-columns: 1.12fr 0.88fr; gap: 44px; flex: 1; padding: 32px 0 22px 0; }}
  .qa-photos-stack {{ display: grid; grid-template-columns: 1fr 1fr; gap: 26px; }}
  .qa-card {{ background: #F6F6F3; border: 1px solid #E2E5EA; display: flex; flex-direction: column; overflow: hidden; }}
  .qa-img-box {{ background: #FFFFFF; height: 350px; padding: 20px; display: flex; align-items: center; justify-content: center; border-bottom: 1px solid #E2E5EA; }}
  .qa-img-box img {{ max-width: 100%; max-height: 310px; object-fit: contain; }}
  .qa-card-body {{ padding: 26px 28px; display: flex; flex-direction: column; gap: 10px; flex: 1; }}
  .qa-card-title {{ font-size: 21px; font-weight: 700; color: #0E131B; }}
  .qa-card-text {{ font-size: 15px; line-height: 1.65; color: #4B5563; }}
  .qa-protocol {{ background: #F6F6F3; padding: 34px 38px; display: flex; flex-direction: column; justify-content: space-between; }}
  .qa-proto-head {{ font-size: 23px; font-weight: 700; color: #0E131B; margin-top: 8px; padding-bottom: 18px; border-bottom: 1px solid #DCDFE4; }}
  .qa-step-list {{ display: flex; flex-direction: column; gap: 16px; margin: auto 0; }}
  .qa-step {{ display: grid; grid-template-columns: 42px 1fr; gap: 14px; align-items: start; }}
  .qa-step-num {{ font-family: Georgia, serif; font-size: 22px; color: #A67C2E; line-height: 1.2; }}
  .qa-step-title {{ font-size: 16px; font-weight: 700; color: #0E131B; margin-bottom: 3px; }}
  .qa-step-desc {{ font-size: 14px; line-height: 1.55; color: #4B5563; }}
  .qa-iso-note {{ padding-top: 16px; border-top: 1px solid #DCDFE4; font-size: 13.5px; font-weight: 600; color: #374151; }}

  /* SLIDE 7 */
  .dark-closing {{ background: #0E131B; color: #FFFFFF; padding: 64px 96px 54px 96px; display: flex; flex-direction: column; justify-content: space-between; }}
  .dark-top-bar {{ display: flex; justify-content: space-between; align-items: flex-end; padding-bottom: 22px; border-bottom: 1px solid rgba(255,255,255,0.14); }}
  .dark-h2 {{ font-size: 42px; font-weight: 700; color: #FFFFFF; margin-top: 8px; }}
  .timeline-5 {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 22px; padding: 36px 0; border-bottom: 1px solid rgba(255,255,255,0.14); }}
  .tl-item {{ display: flex; flex-direction: column; gap: 10px; padding-right: 14px; border-right: 1px solid rgba(255,255,255,0.1); }}
  .tl-item:last-child {{ border-right: none; padding-right: 0; }}
  .tl-num {{ font-family: Georgia, serif; font-size: 30px; color: #D4AA55; line-height: 1; }}
  .tl-title {{ font-size: 18px; font-weight: 700; color: #FFFFFF; line-height: 1.3; }}
  .tl-desc {{ font-size: 14px; line-height: 1.6; color: #9CA3AF; }}
  .closing-lower {{ display: grid; grid-template-columns: 0.95fr 1.15fr; gap: 56px; padding: 32px 0 10px 0; align-items: start; }}
  .rfq-panel {{ background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.12); padding: 32px 36px; }}
  .rfq-panel-title {{ font-size: 21px; font-weight: 700; color: #FFFFFF; margin: 8px 0 20px 0; }}
  .rfq-list {{ list-style: none; display: grid; grid-template-columns: 1fr 1fr; gap: 14px 22px; font-size: 14.5px; color: #D1D5DB; }}
  .rfq-list li {{ padding-left: 16px; position: relative; }}
  .rfq-list li::before {{ content: ""; position: absolute; left: 0; top: 10px; width: 7px; height: 1.5px; background: #D4AA55; }}
  .contact-panel {{ display: flex; flex-direction: column; gap: 16px; }}
  .contact-headline {{ font-size: 25px; font-weight: 600; color: #FFFFFF; line-height: 1.45; }}
  .contact-grid {{ display: grid; grid-template-columns: 120px 1fr; gap: 11px 20px; padding-top: 8px; font-size: 15.5px; }}
  .c-key {{ font-size: 13px; font-weight: 700; color: #9CA3AF; padding-top: 2px; }}
  .c-val {{ color: #FFFFFF; font-weight: 500; }}
  .c-val-accent {{ color: #E5C178; font-weight: 700; }}
  .dark-bottom-bar {{ display: flex; justify-content: space-between; align-items: center; padding-top: 18px; border-top: 1px solid rgba(255,255,255,0.14); font-size: 14px; color: #9CA3AF; }}
"""


def build_slides_html(d):
    s1_meta_html = "".join(
        f'<div><div class="cover-meta-label">{k}</div><div class="cover-meta-val">{v}</div></div>'
        for k, v in d["s1_meta"]
    )
    s2_facts_html = "".join(
        f'<div class="fact-row"><span class="fact-key">{k}</span><span class="fact-val">{v}</span></div>'
        for k, v in d["s2_facts"]
    )
    s2_fhpq_html = "".join(
        f'<div class="fhpq-item"><div class="fhpq-num">{n}</div><div class="fhpq-title">{t}</div><div class="fhpq-desc">{desc}</div></div>'
        for n, t, desc in d["s2_fhpq"]
    )
    s3_procs_html = ""
    for n, t, summ, pts, featured in d["s3_procs"]:
        cls = "process-col process-col-featured" if featured else "process-col"
        li_html = "".join(f"<li>{p}</li>" for p in pts)
        s3_procs_html += f'<div class="{cls}"><div><div class="proc-index">{n}</div><div class="proc-title">{t}</div><div class="proc-summary">{summ}</div></div><ul class="proc-list">{li_html}</ul></div>'

    s3_mats_html = "".join(
        f'<div class="mat-item"><div class="mat-code">{c}</div><div class="mat-desc">{desc}</div></div>'
        for c, desc in d["s3_mats"]
    )

    def prod_card(img_key, tag, title, pts, app):
        li_html = "".join(f"<li>{p}</li>" for p in pts)
        return f"""
        <div class="prod-card-horiz">
          <div class="prod-photo-stage"><img src="{ASSETS[img_key]}" alt="{title}"/></div>
          <div class="prod-info">
            <div><div class="prod-tag">{tag}</div><div class="prod-title">{title}</div><ul class="prod-bullets">{li_html}</ul></div>
            <div class="prod-app">{app}</div>
          </div>
        </div>"""

    c = d["s4_cards"]
    s4_col1 = prod_card(*c[0]) + prod_card(*c[2])
    s4_col2 = prod_card(*c[1]) + prod_card(*c[3])

    s5_equips_html = ""
    for img_key, k, t, desc, pts in d["s5_equips"]:
        li_html = "".join(f"<li>{p}</li>" for p in pts)
        s5_equips_html += f"""
        <div class="equip-feature">
          <div class="equip-img-stage"><img src="{ASSETS[img_key]}" alt="{t}"/></div>
          <div class="equip-detail">
            <div><div class="kicker">{k}</div><div class="equip-title">{t}</div><p class="equip-desc">{desc}</p></div>
            <ul class="proc-list">{li_html}</ul>
          </div>
        </div>"""
    s5_sec_html = "".join(f"<span>{it}</span>" for it in d["s5_sec_items"])

    s6_qas_html = "".join(
        f'<div class="qa-card"><div class="qa-img-box"><img src="{ASSETS[ik]}" alt="{t}"/></div><div class="qa-card-body"><div class="prod-tag">{tag}</div><div class="qa-card-title">{t}</div><div class="qa-card-text">{desc}</div></div></div>'
        for ik, tag, t, desc in d["s6_qas"]
    )
    s6_gates_html = "".join(
        f'<div class="qa-step"><div class="qa-step-num">{n}</div><div><div class="qa-step-title">{t}</div><div class="qa-step-desc">{desc}</div></div></div>'
        for n, t, desc in d["s6_gates"]
    )

    s7_tl_html = "".join(
        f'<div class="tl-item"><div class="tl-num">{n}</div><div class="tl-title">{t}</div><div class="tl-desc">{desc}</div></div>'
        for n, t, desc in d["s7_steps"]
    )
    s7_rfq_html = "".join(f"<li>{it}</li>" for it in d["s7_rfq_items"])
    s7_contacts_html = "".join(
        f'<div class="c-key">{k}</div><div class="{"c-val c-val-accent" if acc else "c-val"}">{v}</div>'
        for k, v, acc in d["s7_contacts"]
    )

    return [
        # SLIDE 1
        f"""
        <div class="slide cover-slide" id="slide-1">
          <div class="cover-left">
            <div class="cover-brand">
              <img src="{ASSETS['logo']}" alt="Logo"/>
              <div class="cover-brand-text">
                <div class="cover-brand-name">{d['brand_name']}</div>
                <div class="cover-brand-sub">{d['brand_sub']}</div>
              </div>
            </div>
            <div class="cover-main">
              <div class="cover-kicker">{d['s1_kicker']}</div>
              <h1 class="cover-h1">{d['s1_h1_line1']}<br/><em>{d['s1_h1_em']}</em></h1>
              <p class="cover-desc">{d['s1_desc']}</p>
            </div>
            <div class="cover-meta-strip">{s1_meta_html}</div>
          </div>
          <div class="cover-right">
            <div class="cover-gallery-top"><span>{d['s1_gallery_title']}</span><span>01 / 07</span></div>
            <div class="cover-figure cover-figure-lg">
              <img src="{ASSETS['lsr']}" alt="LSR"/>
              <div class="fig-caption"><span>FIG. 01</span><div>{d['s1_fig1']}</div></div>
            </div>
            <div class="cover-figure cover-figure-sm">
              <img src="{ASSETS['orings']}" alt="O-Rings"/>
              <div class="fig-caption"><span>FIG. 02</span><div>{d['s1_fig2']}</div></div>
            </div>
          </div>
        </div>""",
        # SLIDE 2
        f"""
        <div class="slide light-slide" id="slide-2">
          <div class="top-bar">
            <div class="top-bar-left"><div class="kicker">{d['s2_kicker']}</div><h2 class="section-h2">{d['s2_title']}</h2></div>
            <div class="top-bar-brand"><img src="{ASSETS['logo']}" alt="Logo"/><span>{d['brand_short']}</span></div>
          </div>
          <div class="s2-body">
            <div class="facts-panel">
              <div class="big-stat-row"><div class="big-stat-num">1991</div><div class="big-stat-text">{d['s2_year_sub']}</div></div>
              <div class="fact-table">{s2_facts_html}</div>
            </div>
            <div class="fhpq-panel">
              <div class="fhpq-intro">{d['s2_intro']}</div>
              <div class="fhpq-grid">{s2_fhpq_html}</div>
            </div>
          </div>
          <div class="bottom-bar"><span>{d['footer_left']}</span><span class="page-num">02 / 07</span></div>
        </div>""",
        # SLIDE 3
        f"""
        <div class="slide warm-slide" id="slide-3">
          <div class="top-bar">
            <div class="top-bar-left"><div class="kicker">{d['s3_kicker']}</div><h2 class="section-h2">{d['s3_title']}</h2></div>
            <div class="top-bar-brand"><img src="{ASSETS['logo']}" alt="Logo"/><span>{d['brand_short']}</span></div>
          </div>
          <div class="s3-body">
            <div class="process-grid">{s3_procs_html}</div>
            <div class="material-strip"><div class="mat-label">{d['s3_mat_label']}</div>{s3_mats_html}</div>
          </div>
          <div class="bottom-bar"><span>{d['s3_footer']}</span><span class="page-num">03 / 07</span></div>
        </div>""",
        # SLIDE 4
        f"""
        <div class="slide light-slide" id="slide-4">
          <div class="top-bar">
            <div class="top-bar-left"><div class="kicker">{d['s4_kicker']}</div><h2 class="section-h2">{d['s4_title']}</h2></div>
            <div class="top-bar-brand"><img src="{ASSETS['logo']}" alt="Logo"/><span>{d['brand_short']}</span></div>
          </div>
          <div class="s4-body">
            <div class="prod-col">{s4_col1}</div>
            <div class="prod-col">{s4_col2}</div>
          </div>
          <div class="bottom-bar"><span>{d['s4_footer']}</span><span class="page-num">04 / 07</span></div>
        </div>""",
        # SLIDE 5
        f"""
        <div class="slide warm-slide" id="slide-5">
          <div class="top-bar">
            <div class="top-bar-left"><div class="kicker">{d['s5_kicker']}</div><h2 class="section-h2">{d['s5_title']}</h2></div>
            <div class="top-bar-brand"><img src="{ASSETS['logo']}" alt="Logo"/><span>{d['brand_short']}</span></div>
          </div>
          <div class="s5-body">
            <div class="equip-grid-2">{s5_equips_html}</div>
            <div class="secondary-strip"><div class="sec-strip-title">{d['s5_sec_title']}</div><div class="sec-strip-items">{s5_sec_html}</div></div>
          </div>
          <div class="bottom-bar"><span>{d['s5_footer']}</span><span class="page-num">05 / 07</span></div>
        </div>""",
        # SLIDE 6
        f"""
        <div class="slide light-slide" id="slide-6">
          <div class="top-bar">
            <div class="top-bar-left"><div class="kicker">{d['s6_kicker']}</div><h2 class="section-h2">{d['s6_title']}</h2></div>
            <div class="top-bar-brand"><img src="{ASSETS['logo']}" alt="Logo"/><span>{d['brand_short']}</span></div>
          </div>
          <div class="s6-body">
            <div class="qa-photos-stack">{s6_qas_html}</div>
            <div class="qa-protocol">
              <div><div class="kicker">{d['s6_proto_kicker']}</div><div class="qa-proto-head">{d['s6_proto_title']}</div></div>
              <div class="qa-step-list">{s6_gates_html}</div>
              <div class="qa-iso-note">{d['s6_iso_note']}</div>
            </div>
          </div>
          <div class="bottom-bar"><span>{d['s6_footer']}</span><span class="page-num">06 / 07</span></div>
        </div>""",
        # SLIDE 7
        f"""
        <div class="slide dark-closing" id="slide-7">
          <div class="dark-top-bar">
            <div class="top-bar-left"><div class="cover-kicker">{d['s7_kicker']}</div><h2 class="dark-h2">{d['s7_title']}</h2></div>
            <div class="cover-brand"><img src="{ASSETS['logo']}" alt="Logo"/></div>
          </div>
          <div class="timeline-5">{s7_tl_html}</div>
          <div class="closing-lower">
            <div class="rfq-panel">
              <div class="cover-kicker">{d['s7_rfq_kicker']}</div>
              <div class="rfq-panel-title">{d['s7_rfq_title']}</div>
              <ul class="rfq-list">{s7_rfq_html}</ul>
            </div>
            <div class="contact-panel">
              <div class="contact-headline">{d['s7_headline']}</div>
              <div class="contact-grid">{s7_contacts_html}</div>
            </div>
          </div>
          <div class="dark-bottom-bar"><span>{d['s7_footer']}</span><span style="color:#FFFFFF;font-weight:700;letter-spacing:2px;">07 / 07</span></div>
        </div>""",
    ]


def add_picture_fit(slide, img_path, box_x, box_y, box_w, box_h):
    p = Path(img_path)
    if not p.exists():
        return
    with Image.open(p) as im:
        iw, ih = im.size
    ratio = iw / ih
    box_ratio = box_w / box_h
    if ratio > box_ratio:
        w, h = box_w, box_w / ratio
    else:
        h, w = box_h, box_h * ratio
    x = box_x + (box_w - w) / 2
    y = box_y + (box_h - h) / 2
    slide.shapes.add_picture(str(p), Inches(x), Inches(y), width=Inches(w), height=Inches(h))


def build_pptx_for_lang(d):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]
    F = d["pptx_font"]

    DARK = RGBColor(14, 19, 27)
    WHITE = RGBColor(255, 255, 255)
    WARM = RGBColor(246, 246, 243)
    INK = RGBColor(17, 24, 39)
    MUTED = RGBColor(82, 91, 107)
    LIGHT_MUTED = RGBColor(156, 163, 175)
    GOLD = RGBColor(166, 124, 46)
    GOLD_LIGHT = RGBColor(212, 170, 85)
    LINE = RGBColor(226, 229, 234)
    LINE_DARK = RGBColor(45, 55, 72)

    img_map = {
        "keypads": IMAGES_DIR / "prod-keypads.jpg",
        "orings": IMAGES_DIR / "prod-orings.jpg",
        "gaskets": IMAGES_DIR / "prod-gaskets.jpg",
        "medkb": IMAGES_DIR / "prod-medical-kb.jpg",
        "lsr": IMAGES_DIR / "equip-lsr.jpg",
        "vac": IMAGES_DIR / "equip-vacuum-press.jpg",
        "opt25d": IMAGES_DIR / "qc-25d-optical.jpg",
        "load": IMAGES_DIR / "qc-load-curve.jpg",
    }

    def rect(slide, x, y, w, h, fill_rgb, border_rgb=None):
        s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        s.fill.solid()
        s.fill.fore_color.rgb = fill_rgb
        if border_rgb:
            s.line.color.rgb = border_rgb
            s.line.width = Pt(0.75)
        else:
            s.line.fill.background()
        return s

    def txt(slide, x, y, w, h, text, size=11, color=INK, bold=False, font=None, align=PP_ALIGN.LEFT):
        tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.alignment = align
        p.text = text
        p.font.name = font or F
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.color.rgb = color
        return tb

    def light_chrome(slide, bg_rgb, kicker, title, footer, page_str):
        rect(slide, 0, 0, 13.333, 7.5, bg_rgb)
        txt(slide, 0.65, 0.4, 9.0, 0.25, kicker, size=9.5, color=GOLD, bold=True)
        txt(slide, 0.65, 0.68, 9.8, 0.52, title, size=22, color=DARK, bold=True)
        if LOGO_FILE.exists():
            add_picture_fit(slide, LOGO_FILE, 10.9, 0.52, 0.4, 0.4)
        txt(slide, 11.38, 0.62, 1.35, 0.28, d["brand_short"], size=10, color=MUTED, bold=True)
        rect(slide, 0.65, 1.28, 12.033, 0.015, LINE)
        rect(slide, 0.65, 6.92, 12.033, 0.015, LINE)
        txt(slide, 0.65, 7.02, 10.2, 0.28, footer, size=9, color=MUTED)
        txt(slide, 11.4, 7.02, 1.28, 0.28, page_str, size=9.5, color=DARK, bold=True, font="Arial", align=PP_ALIGN.RIGHT)

    # SLIDE 1
    s1 = prs.slides.add_slide(blank)
    rect(s1, 0, 0, 7.8, 7.5, DARK)
    rect(s1, 7.8, 0, 5.533, 7.5, WARM)
    if LOGO_FILE.exists():
        add_picture_fit(s1, LOGO_FILE, 0.65, 0.5, 0.5, 0.5)
    txt(s1, 1.25, 0.5, 5.5, 0.28, d["brand_name"], size=13, color=WHITE, bold=True)
    txt(s1, 1.25, 0.8, 5.5, 0.22, d["brand_sub"], size=9, color=LIGHT_MUTED)
    txt(s1, 0.65, 2.0, 6.5, 0.28, d["s1_kicker"], size=10.5, color=GOLD_LIGHT, bold=True)
    txt(s1, 0.65, 2.38, 6.6, 1.5, f"{d['s1_h1_line1']}\n{d['s1_h1_em']}", size=36, color=WHITE, bold=True)
    txt(s1, 0.65, 4.1, 6.4, 1.3, d["s1_desc"], size=12, color=RGBColor(203, 213, 225))
    rect(s1, 0.65, 5.85, 6.5, 0.015, LINE_DARK)
    for i, (k, v) in enumerate(d["s1_meta"]):
        txt(s1, 0.65 + i * 2.2, 6.03, 2.1, 0.22, k, size=8.5, color=LIGHT_MUTED, bold=True)
        txt(s1, 0.65 + i * 2.2, 6.28, 2.1, 0.32, v, size=10.5, color=WHITE, bold=True)
    txt(s1, 8.25, 0.52, 3.8, 0.25, d["s1_gallery_title"], size=9, color=MUTED, bold=True)
    txt(s1, 12.1, 0.52, 0.8, 0.25, "01 / 07", size=9, color=MUTED, bold=True, font="Arial", align=PP_ALIGN.RIGHT)
    rect(s1, 8.25, 0.82, 4.65, 0.015, LINE)
    rect(s1, 8.25, 1.05, 4.65, 3.05, WHITE, LINE)
    add_picture_fit(s1, img_map["lsr"], 8.45, 1.18, 4.25, 2.45)
    txt(s1, 8.45, 3.74, 4.25, 0.25, f"FIG. 01   |   {d['s1_fig1']}", size=8.5, color=MUTED, bold=True)
    rect(s1, 8.25, 4.35, 4.65, 2.65, WHITE, LINE)
    add_picture_fit(s1, img_map["orings"], 8.45, 4.48, 4.25, 2.05)
    txt(s1, 8.45, 6.64, 4.25, 0.25, f"FIG. 02   |   {d['s1_fig2']}", size=8.5, color=MUTED, bold=True)

    # SLIDE 2
    s2 = prs.slides.add_slide(blank)
    light_chrome(s2, WHITE, d["s2_kicker"], d["s2_title"], d["footer_left"], "02 / 07")
    rect(s2, 0.65, 1.58, 3.95, 5.08, WARM)
    txt(s2, 0.92, 1.82, 1.75, 0.72, "1991", size=42, color=DARK, font="Georgia")
    txt(s2, 2.62, 2.02, 1.8, 0.55, d["s2_year_sub"], size=10.5, color=INK, bold=True)
    rect(s2, 0.92, 2.72, 3.4, 0.015, LINE)
    for i, (k, v) in enumerate(d["s2_facts"]):
        y = 2.92 + i * 0.58
        txt(s2, 0.92, y, 1.15, 0.28, k, size=8.8, color=MUTED, bold=True)
        txt(s2, 2.0, y, 2.32, 0.28, v, size=9.2, color=INK, bold=True, align=PP_ALIGN.RIGHT)
        if i < len(d["s2_facts"]) - 1:
            rect(s2, 0.92, y + 0.38, 3.4, 0.01, LINE)
    intro_plain = d["s2_intro"].replace("<strong>", "").replace("</strong>", "")
    txt(s2, 4.95, 1.62, 7.7, 0.78, intro_plain, size=13.5, color=INK)
    rect(s2, 4.95, 2.55, 7.7, 0.015, LINE)
    for idx, (num, title, desc) in enumerate(d["s2_fhpq"]):
        x = 4.95 + (idx % 2) * 3.95
        y = 2.82 + (idx // 2) * 1.95
        txt(s2, x, y, 0.6, 0.35, num, size=18, color=GOLD, font="Georgia")
        txt(s2, x, y + 0.36, 3.65, 0.32, title, size=13, color=DARK, bold=True)
        txt(s2, x, y + 0.74, 3.65, 1.05, desc, size=10, color=MUTED)

    # SLIDE 3
    s3 = prs.slides.add_slide(blank)
    light_chrome(s3, WARM, d["s3_kicker"], d["s3_title"], d["s3_footer"], "03 / 07")
    for i, (num, title, summ, pts, is_dark) in enumerate(d["s3_procs"]):
        x = 0.65 + i * 4.1
        rect(s3, x, 1.55, 3.85, 4.15, DARK if is_dark else WHITE, DARK if is_dark else LINE)
        txt(s3, x + 0.28, 1.76, 0.8, 0.4, num, size=24, color=GOLD_LIGHT if is_dark else GOLD, font="Georgia")
        txt(s3, x + 0.28, 2.24, 3.3, 0.55, title, size=15, color=WHITE if is_dark else DARK, bold=True)
        txt(s3, x + 0.28, 2.88, 3.3, 0.85, summ, size=9.8, color=RGBColor(203, 213, 225) if is_dark else MUTED)
        rect(s3, x + 0.28, 3.84, 3.3, 0.012, LINE_DARK if is_dark else LINE)
        tb = s3.shapes.add_textbox(Inches(x + 0.28), Inches(3.98), Inches(3.3), Inches(1.55))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        for j, pt in enumerate(pts):
            p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
            p.text = f"—  {pt}"
            p.font.name = F
            p.font.size = Pt(9.2)
            p.font.color.rgb = RGBColor(226, 232, 240) if is_dark else INK
            p.space_after = Pt(5)
    rect(s3, 0.65, 5.95, 12.033, 0.78, WHITE, LINE)
    txt(s3, 0.9, 6.12, 1.35, 0.45, d["s3_mat_label"].replace("<br/>", "\n"), size=9.5, color=DARK, bold=True)
    rect(s3, 2.3, 6.08, 0.015, 0.52, LINE)
    for i, (m, desc) in enumerate(d["s3_mats"]):
        mx = 2.52 + i * 1.68
        txt(s3, mx, 6.1, 1.6, 0.24, m, size=11, color=DARK, bold=True, font="Arial")
        txt(s3, mx, 6.38, 1.6, 0.24, desc, size=8.5, color=MUTED)

    # SLIDE 4
    s4 = prs.slides.add_slide(blank)
    light_chrome(s4, WHITE, d["s4_kicker"], d["s4_title"], d["s4_footer"], "04 / 07")
    for idx, (ik, tag, title, pts, app) in enumerate(d["s4_cards"]):
        x = 0.65 + (idx % 2) * 6.15
        y = 1.55 + (idx // 2) * 2.65
        rect(s4, x, y, 5.88, 2.42, WARM, LINE)
        rect(s4, x, y, 2.3, 2.42, WHITE, LINE)
        add_picture_fit(s4, img_map[ik], x + 0.14, y + 0.14, 2.02, 2.14)
        tx = x + 2.52
        txt(s4, tx, y + 0.18, 3.15, 0.22, tag, size=8.5, color=GOLD, bold=True)
        txt(s4, tx, y + 0.44, 3.15, 0.34, title, size=13.5, color=DARK, bold=True)
        tb = s4.shapes.add_textbox(Inches(tx), Inches(y + 0.86), Inches(3.15), Inches(1.02))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        for j, pt in enumerate(pts):
            p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
            p.text = f"—  {pt}"
            p.font.name = F
            p.font.size = Pt(9)
            p.font.color.rgb = MUTED
            p.space_after = Pt(3)
        rect(s4, tx, y + 1.96, 3.1, 0.012, LINE)
        txt(s4, tx, y + 2.05, 3.15, 0.26, app, size=8.2, color=INK, bold=True)

    # SLIDE 5
    s5 = prs.slides.add_slide(blank)
    light_chrome(s5, WARM, d["s5_kicker"], d["s5_title"], d["s5_footer"], "05 / 07")
    for i, (ik, tag, title, desc, pts) in enumerate(d["s5_equips"]):
        x = 0.65 + i * 6.18
        rect(s5, x, 1.55, 5.85, 4.2, WHITE, LINE)
        rect(s5, x, 1.55, 2.5, 4.2, WHITE, LINE)
        add_picture_fit(s5, img_map[ik], x + 0.16, 1.72, 2.18, 3.86)
        tx = x + 2.75
        txt(s5, tx, 1.8, 2.9, 0.22, tag, size=8.8, color=GOLD, bold=True)
        txt(s5, tx, 2.1, 2.9, 0.55, title, size=15.5, color=DARK, bold=True)
        txt(s5, tx, 2.78, 2.9, 0.95, desc, size=9.8, color=MUTED)
        rect(s5, tx, 3.88, 2.85, 0.012, LINE)
        tb = s5.shapes.add_textbox(Inches(tx), Inches(4.04), Inches(2.9), Inches(1.5))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        for j, pt in enumerate(pts):
            p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
            p.text = f"—  {pt}"
            p.font.name = F
            p.font.size = Pt(9.2)
            p.font.color.rgb = INK
            p.space_after = Pt(5)
    rect(s5, 0.65, 6.02, 12.033, 0.68, DARK)
    txt(s5, 0.92, 6.24, 2.4, 0.25, d["s5_sec_title"], size=9.5, color=GOLD_LIGHT, bold=True)
    txt(s5, 3.45, 6.23, 9.0, 0.28, "   |   ".join(d["s5_sec_items"]), size=10, color=WHITE)

    # SLIDE 6
    s6 = prs.slides.add_slide(blank)
    light_chrome(s6, WHITE, d["s6_kicker"], d["s6_title"], d["s6_footer"], "06 / 07")
    for i, (ik, tag, title, desc) in enumerate(d["s6_qas"]):
        x = 0.65 + i * 3.55
        rect(s6, x, 1.55, 3.32, 5.1, WARM, LINE)
        rect(s6, x, 1.55, 3.32, 2.6, WHITE, LINE)
        add_picture_fit(s6, img_map[ik], x + 0.14, 1.68, 3.04, 2.34)
        txt(s6, x + 0.22, 4.34, 2.88, 0.22, tag, size=8.5, color=GOLD, bold=True)
        txt(s6, x + 0.22, 4.62, 2.88, 0.34, title, size=13, color=DARK, bold=True)
        txt(s6, x + 0.22, 5.02, 2.88, 1.45, desc, size=9.5, color=MUTED)
    rect(s6, 7.85, 1.55, 4.83, 5.1, WARM)
    txt(s6, 8.15, 1.8, 4.2, 0.22, d["s6_proto_kicker"], size=8.8, color=GOLD, bold=True)
    txt(s6, 8.15, 2.08, 4.2, 0.36, d["s6_proto_title"], size=15, color=DARK, bold=True)
    rect(s6, 8.15, 2.52, 4.22, 0.015, LINE)
    for i, (num, title, desc) in enumerate(d["s6_gates"]):
        y = 2.7 + i * 0.68
        txt(s6, 8.15, y, 0.4, 0.3, num, size=14, color=GOLD, font="Georgia")
        txt(s6, 8.58, y, 3.8, 0.24, title, size=10.2, color=DARK, bold=True)
        txt(s6, 8.58, y + 0.25, 3.8, 0.36, desc, size=8.6, color=MUTED)
    rect(s6, 8.15, 6.18, 4.22, 0.015, LINE)
    txt(s6, 8.15, 6.28, 4.25, 0.28, d["s6_iso_note"], size=8.4, color=INK, bold=True)

    # SLIDE 7
    s7 = prs.slides.add_slide(blank)
    rect(s7, 0, 0, 13.333, 7.5, DARK)
    txt(s7, 0.65, 0.44, 8.5, 0.25, d["s7_kicker"], size=9.5, color=GOLD_LIGHT, bold=True)
    txt(s7, 0.65, 0.72, 9.5, 0.52, d["s7_title"], size=24, color=WHITE, bold=True)
    if LOGO_FILE.exists():
        add_picture_fit(s7, LOGO_FILE, 12.2, 0.55, 0.48, 0.48)
    rect(s7, 0.65, 1.35, 12.033, 0.015, LINE_DARK)
    for i, (num, title, desc) in enumerate(d["s7_steps"]):
        x = 0.65 + i * 2.43
        txt(s7, x, 1.62, 0.6, 0.38, num, size=20, color=GOLD_LIGHT, font="Georgia")
        txt(s7, x, 2.06, 2.22, 0.3, title, size=11.5, color=WHITE, bold=True)
        txt(s7, x, 2.42, 2.22, 0.88, desc, size=9, color=LIGHT_MUTED)
        if i < 4:
            rect(s7, x + 2.3, 1.7, 0.012, 1.45, LINE_DARK)
    rect(s7, 0.65, 3.45, 12.033, 0.015, LINE_DARK)
    rect(s7, 0.65, 3.78, 5.45, 2.78, RGBColor(21, 28, 40), LINE_DARK)
    txt(s7, 0.95, 4.02, 4.85, 0.22, d["s7_rfq_kicker"], size=8.8, color=GOLD_LIGHT, bold=True)
    txt(s7, 0.95, 4.3, 4.85, 0.35, d["s7_rfq_title"], size=14.5, color=WHITE, bold=True)
    for i, item in enumerate(d["s7_rfq_items"]):
        txt(s7, 0.95 + (i % 2) * 2.48, 4.84 + (i // 2) * 0.46, 2.38, 0.36, f"—  {item}", size=9.2, color=RGBColor(209, 213, 219))
    txt(s7, 6.5, 3.78, 6.15, 0.7, d["s7_headline"], size=15.5, color=WHITE, bold=True)
    for i, (k, v, is_acc) in enumerate(d["s7_contacts"]):
        y = 4.62 + i * 0.34
        txt(s7, 6.5, y, 1.15, 0.25, k, size=8.8, color=LIGHT_MUTED, bold=True)
        txt(s7, 7.65, y, 5.0, 0.3, v, size=10, color=GOLD_LIGHT if is_acc else WHITE, bold=is_acc)
    rect(s7, 0.65, 6.92, 12.033, 0.015, LINE_DARK)
    txt(s7, 0.65, 7.02, 10.2, 0.28, d["s7_footer"], size=9, color=LIGHT_MUTED)
    txt(s7, 11.4, 7.02, 1.28, 0.28, "07 / 07", size=9.5, color=WHITE, bold=True, font="Arial", align=PP_ALIGN.RIGHT)

    d["pptx_out"].parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(d["pptx_out"]))
    print(f"  - Saved PPTX: {d['pptx_out'].name} ({d['pptx_out'].stat().st_size / 1024:.1f} KB)")


def build_language(code):
    d = LANG_DATA[code]
    print(f"\n=== Building {code.upper()} 7-Slide Swiss Industrial Profile ===")
    css = build_css(d["font_stack"])
    slides = build_slides_html(d)

    def wrap(subset):
        return f'<!DOCTYPE html><html lang="{d["lang_attr"]}"><head><meta charset="UTF-8"><title>{d["doc_title"]}</title><style>{css}</style></head><body>{"".join(subset)}</body></html>'

    deck_html = WORKSPACE / "scratch" / f"presentation_deck_{code}.html"
    deck_html.write_text(wrap(slides), encoding="utf-8")

    d["pdf_out"].parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        CHROME_PATH, "--headless=new", "--disable-gpu",
        "--run-all-compositor-stages-before-draw", "--print-to-pdf-no-header",
        f"--print-to-pdf={d['pdf_out'].resolve()}", str(deck_html.resolve().as_uri()),
    ], check=True)
    print(f"  - Saved PDF:  {d['pdf_out'].name} ({d['pdf_out'].stat().st_size / 1024:.1f} KB)")

    for idx, s_html in enumerate(slides, start=1):
        sf = WORKSPACE / "scratch" / f"single_{code}_{idx}.html"
        sf.write_text(wrap([s_html]), encoding="utf-8")
        out_png = PREVIEWS_DIR / f"{code}-slide-{idx}.png"
        subprocess.run([
            CHROME_PATH, "--headless=new", "--disable-gpu",
            "--window-size=1920,1080", "--force-device-scale-factor=1", "--hide-scrollbars",
            f"--screenshot={out_png.resolve()}", str(sf.resolve().as_uri()),
        ], check=True)
    print(f"  - Captured 7 full-bleed PNG previews ({code}-slide-1..7.png)")

    build_pptx_for_lang(d)


def main():
    build_language("zh")
    build_language("ja")
    print("\nALL ZH & JA PRESENTATIONS BUILT SUCCESSFULLY!")


if __name__ == "__main__":
    main()
