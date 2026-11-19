import base64
import os
import subprocess
import tempfile

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUT_PDF = os.path.abspath(os.path.join("pdf", "en", "Jun-Hsiang-Enterprise-Company-Profile-EN.pdf"))

def img_data_uri(rel_path):
    abs_p = os.path.abspath(rel_path)
    if not os.path.exists(abs_p):
        return ""
    ext = os.path.splitext(abs_p)[1].lower().lstrip(".")
    mime = "image/png" if ext == "png" else ("image/webp" if ext == "webp" else "image/jpeg")
    b64 = base64.b64encode(open(abs_p, "rb").read()).decode("ascii")
    return f"data:{mime};base64,{b64}"

logo_uri = img_data_uri("images/logo.png")
hero_mold_uri = img_data_uri("images/hero-premium-mold-mobile.webp") or img_data_uri("images/hero-premium-mold.webp")
hero_factory_uri = img_data_uri("images/hero-premium-factory-mobile.webp") or img_data_uri("images/hero-premium-factory.webp")

HTML_CONTENT = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>Jun-Hsiang Enterprise Co., Ltd. — Company Profile &amp; Manufacturing Capabilities</title>
<style>
  @page {{ size: A4; margin: 0; }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #0F172A;
    background: #FFFFFF;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}
  .page {{
    width: 210mm;
    height: 297mm;
    padding: 14mm 15mm 12mm 15mm;
    position: relative;
    page-break-after: always;
    overflow: hidden;
  }}
  .page:last-child {{ page-break-after: auto; }}
  .header-bar {{
    background: #0A0F1C;
    color: #F8FAFC;
    padding: 16px 20px;
    border-radius: 10px;
    border-bottom: 4px solid #D4A843;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
  }}
  .brand-left {{ display: flex; align-items: center; gap: 12px; }}
  .brand-left img {{ width: 42px; height: 42px; border-radius: 8px; background: #fff; padding: 3px; }}
  .brand-name {{ font-size: 16pt; font-weight: 800; letter-spacing: 0.3px; color: #FFFFFF; margin: 0; }}
  .brand-sub {{ font-size: 8.8pt; color: #D4A843; font-weight: 600; margin: 2px 0 0; }}
  .header-badges {{ text-align: right; font-size: 8.2pt; line-height: 1.5; color: #CBD5E1; }}
  .header-badges strong {{ color: #FDE68A; }}
  .pill-row {{ display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 14px; }}
  .pill {{
    background: #F1F5F9;
    border: 1px solid #CBD5E1;
    color: #0F172A;
    font-size: 8.2pt;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 999px;
  }}
  .pill.gold {{ background: #FEF9C3; border-color: #D4A843; color: #713F12; }}
  .section-title {{
    font-size: 11.5pt;
    font-weight: 800;
    color: #0A0F1C;
    border-left: 4px solid #D4A843;
    padding-left: 9px;
    margin: 12px 0 8px;
    text-transform: uppercase;
    letter-spacing: 0.4px;
  }}
  p.lead {{ font-size: 9.4pt; line-height: 1.55; color: #334155; margin: 0 0 10px; }}
  .two-col {{ display: grid; grid-template-columns: 1.15fr 0.85fr; gap: 12px; margin-bottom: 12px; }}
  .photo-card {{
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    overflow: hidden;
    background: #F8FAFC;
  }}
  .photo-card img {{ width: 100%; height: 118px; object-fit: cover; display: block; }}
  .photo-cap {{ padding: 6px 10px; font-size: 7.8pt; color: #475569; font-weight: 600; }}
  .facts-table {{ width: 100%; border-collapse: collapse; font-size: 8.5pt; }}
  .facts-table td {{ padding: 6px 8px; border-bottom: 1px solid #E2E8F0; vertical-align: top; }}
  .facts-table td.k {{ width: 34%; font-weight: 700; color: #0F172A; background: #F8FAFC; }}
  .cap-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 9px; }}
  .cap-box {{
    border: 1px solid #CBD5E1;
    border-top: 3px solid #0D9488;
    border-radius: 7px;
    padding: 9px 11px;
    background: #FFFFFF;
  }}
  .cap-box h3 {{ font-size: 9.5pt; margin: 0 0 4px; color: #0F172A; }}
  .cap-box p {{ font-size: 8.3pt; line-height: 1.45; color: #475569; margin: 0; }}
  .ind-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 12px; }}
  .ind-box {{
    background: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-radius: 7px;
    padding: 9px 10px;
  }}
  .ind-box strong {{ display: block; font-size: 8.8pt; color: #0F172A; margin-bottom: 3px; }}
  .ind-box span {{ font-size: 7.9pt; color: #475569; line-height: 1.4; display: block; }}
  .steps {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 12px; }}
  .step {{
    border: 1px solid #E2E8F0;
    border-radius: 7px;
    padding: 8px 10px;
    background: #FFFFFF;
  }}
  .step-num {{
    display: inline-block;
    background: #0A0F1C;
    color: #D4A843;
    font-weight: 800;
    font-size: 7.5pt;
    padding: 2px 7px;
    border-radius: 999px;
    margin-bottom: 4px;
  }}
  .step strong {{ display: block; font-size: 8.6pt; color: #0F172A; margin-bottom: 2px; }}
  .step p {{ margin: 0; font-size: 7.8pt; color: #475569; line-height: 1.4; }}
  .rfq-card {{
    background: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-left: 4px solid #0D9488;
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 12px;
  }}
  .rfq-card h3 {{ margin: 0 0 6px; font-size: 9.8pt; color: #0F172A; }}
  .rfq-list {{ margin: 0; padding-left: 16px; font-size: 8.4pt; color: #334155; line-height: 1.55; columns: 2; column-gap: 18px; }}
  .contact-box {{
    background: #0A0F1C;
    color: #F8FAFC;
    border-radius: 10px;
    padding: 14px 18px;
    border-top: 4px solid #D4A843;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .contact-box h3 {{ margin: 0 0 4px; color: #FDE68A; font-size: 10.8pt; }}
  .contact-box p {{ margin: 2px 0; font-size: 8.6pt; color: #E2E8F0; }}
  .contact-right {{ text-align: right; font-size: 8.5pt; color: #CBD5E1; line-height: 1.6; }}
  .contact-right strong {{ color: #FFFFFF; }}
  .page-footer {{
    position: absolute;
    bottom: 8mm;
    left: 15mm;
    right: 15mm;
    display: flex;
    justify-content: space-between;
    font-size: 7.5pt;
    color: #64748B;
    border-top: 1px solid #E2E8F0;
    padding-top: 5px;
  }}
</style>
</head>
<body>

<!-- PAGE 1 -->
<div class="page">
  <div class="header-bar">
    <div class="brand-left">
      <img src="{logo_uri}" alt="Jun-Hsiang Logo"/>
      <div>
        <div class="brand-name">Jun-Hsiang Enterprise Co., Ltd.</div>
        <div class="brand-sub">Custom Silicone &amp; Rubber Parts Manufacturer in Taiwan</div>
      </div>
    </div>
    <div class="header-badges">
      <div><strong>ISO 9001 Certified</strong> • 30+ Years Experience</div>
      <div>100% Made in Taiwan (Non-China Supply Chain)</div>
      <div>www.jun-hsiang.com.tw/en/</div>
    </div>
  </div>

  <div class="pill-row">
    <span class="pill gold">100% Made in Taiwan (MIT)</span>
    <span class="pill">LSR Liquid Silicone Injection</span>
    <span class="pill">HCR Compression Molding</span>
    <span class="pill">Silicone-to-Metal / Plastic Overmolding</span>
    <span class="pill">Mutual NDA Ready</span>
  </div>

  <div class="section-title">Company Overview</div>
  <p class="lead">
    Founded in New Taipei City, Taiwan with over 30 years of manufacturing craftsmanship, <strong>Jun-Hsiang Enterprise Co., Ltd.</strong> is an ISO 9001-certified custom silicone and rubber molding manufacturer serving global industrial, automotive, medical, electronics, and food-contact buyers across the United States, Europe, and Japan. We combine in-house precision mold tooling with LSR injection, vacuum compression molding, and multi-material overmolding to deliver tariff-resilient, non-China production from pilot prototyping through mass production.
  </p>

  <div class="two-col">
    <div>
      <table class="facts-table">
        <tr><td class="k">Factory Location</td><td>New Taipei City (Xinzhuang Dist.), Taiwan</td></tr>
        <tr><td class="k">Quality System</td><td>ISO 9001 Certified Quality Management</td></tr>
        <tr><td class="k">Material Compliance</td><td>US FDA 21 CFR 177.2600, EU LFGB, REACH, RoHS, ISO 10993 LSR options</td></tr>
        <tr><td class="k">Tooling Capability</td><td>In-house precision mold design, fabrication &amp; maintenance</td></tr>
        <tr><td class="k">IP &amp; Export Docs</td><td>Mutual NDA before CAD review; Certificate of Origin (MIT)</td></tr>
        <tr><td class="k">Volume Flexibility</td><td>Low-volume pilot sampling to scalable mass production</td></tr>
      </table>
    </div>
    <div class="photo-card">
      <img src="{hero_mold_uri}" alt="Precision Silicone Mold Tooling"/>
      <div class="photo-cap">In-house precision mold development &amp; LSR / HCR silicone molding in New Taipei City, Taiwan.</div>
    </div>
  </div>

  <div class="section-title">Core Manufacturing Capabilities</div>
  <div class="cap-grid">
    <div class="cap-box">
      <h3>1. LSR Liquid Silicone Injection Molding</h3>
      <p>Two-part platinum-cured LSR injection molding with precision cold-runner and multi-cavity tooling. Ideal for complex geometries, thin walls, large-shot thick parts, and controlled-flash cleanliness.</p>
    </div>
    <div class="cap-box">
      <h3>2. HCR Solid Silicone &amp; Rubber Compression</h3>
      <p>Vacuum compression molding for High Consistency Rubber (HCR), EPDM, NBR, Viton (FKM), and Fluorosilicone (FVMQ). Cost-effective tooling for industrial gaskets, O-rings, keypads, and mounts.</p>
    </div>
    <div class="cap-box">
      <h3>3. Silicone-to-Metal &amp; Plastic Overmolding</h3>
      <p>Insert molding and chemical/mechanical bonding onto aluminum, steel, stainless steel, brass, and engineering plastics (PC, PA, PBT). Supports both primer-controlled and primerless self-bonding LSR.</p>
    </div>
    <div class="cap-box">
      <h3>4. Specialty Elastomers &amp; Custom Hardness</h3>
      <p>Full Shore A 10° to 80° hardness customization, including oil-bleeding self-lubricating silicone for low-insertion-force automotive wire harness seals and chemical-resistant specialty elastomers.</p>
    </div>
  </div>

  <div class="page-footer">
    <span>Jun-Hsiang Enterprise Co., Ltd. — Company Profile &amp; Capability Brochure</span>
    <span>Page 1 of 2</span>
  </div>
</div>

<!-- PAGE 2 -->
<div class="page">
  <div class="header-bar" style="padding: 11px 18px; margin-bottom: 12px;">
    <div class="brand-left">
      <img src="{logo_uri}" alt="Jun-Hsiang Logo" style="width: 30px; height: 30px;"/>
      <div>
        <div class="brand-name" style="font-size: 12.5pt;">Jun-Hsiang Enterprise Co., Ltd.</div>
        <div class="brand-sub" style="font-size: 7.8pt;">Industries, Quality Workflow &amp; Direct RFQ Guide</div>
      </div>
    </div>
    <div class="header-badges" style="font-size: 7.8pt;">
      <div><strong>andy_hsu@jun-hsiang.com.tw</strong> | +886-2-2203-9918</div>
    </div>
  </div>

  <div class="section-title">Target Industries &amp; Representative Components</div>
  <div class="ind-grid">
    <div class="ind-box">
      <strong>Automotive &amp; EV Harness</strong>
      <span>Self-lubricating single wire seals (SWS), waterproof connector seals, LSR overmolded PA66 sockets.</span>
    </div>
    <div class="ind-box">
      <strong>Medical &amp; Respiratory</strong>
      <span>FDA &amp; ISO 10993 platinum-cured LSR respiratory mask cushions, seals, and hygienic elastomer components.</span>
    </div>
    <div class="ind-box">
      <strong>Food Contact &amp; Infant Care</strong>
      <span>US FDA 21 CFR 177.2600 &amp; EU LFGB food-grade seals, gaskets, and platinum-cured silicone parts.</span>
    </div>
    <div class="ind-box">
      <strong>Semiconductor &amp; AI Server</strong>
      <span>Low-outgassing seals, FVMQ/FKM chemical-resistant O-rings, thermal &amp; vibration management pads.</span>
    </div>
    <div class="ind-box">
      <strong>Industrial Machinery</strong>
      <span>Rubber-to-metal bonded anti-vibration feet, heavy-duty shock mounts, custom gaskets &amp; diaphragms.</span>
    </div>
    <div class="ind-box">
      <strong>UAV Drones &amp; Electronics</strong>
      <span>Gimbal vibration damping balls, waterproof IP rings, conductive carbon-pill silicone keypads.</span>
    </div>
  </div>

  <div class="section-title">6-Step Build-to-Print Manufacturing Workflow</div>
  <div class="steps">
    <div class="step">
      <span class="step-num">STEP 01</span>
      <strong>Mutual NDA &amp; CAD Review</strong>
      <p>Sign mutual NDA before reviewing 2D/3D drawings (STEP, IGS, PDF, DWG) to protect your IP.</p>
    </div>
    <div class="step">
      <span class="step-num">STEP 02</span>
      <strong>Material &amp; Spec Alignment</strong>
      <p>Select LSR vs. HCR, Shore A hardness, operating temperature, and FDA / LFGB / REACH compliance.</p>
    </div>
    <div class="step">
      <span class="step-num">STEP 03</span>
      <strong>Mold &amp; Process Quotation</strong>
      <p>Provide transparent tooling structure recommendations, cavity layout, and itemized unit pricing.</p>
    </div>
    <div class="step">
      <span class="step-num">STEP 04</span>
      <strong>In-House Mold Fabrication</strong>
      <p>Precision cavity machining, venting, and parting-line control managed directly in our Taiwan facility.</p>
    </div>
    <div class="step">
      <span class="step-num">STEP 05</span>
      <strong>T1 Sampling &amp; Inspection</strong>
      <p>First-article trial molding with 2.5D optical dimensional inspection and customer sample approval.</p>
    </div>
    <div class="step">
      <span class="step-num">STEP 06</span>
      <strong>Mass Production &amp; Export</strong>
      <p>ISO 9001 batch quality verification, clean packaging, and global export with MIT Certificate of Origin.</p>
    </div>
  </div>

  <div class="photo-card" style="margin-bottom: 12px; display: flex; align-items: center;">
    <img src="{hero_factory_uri}" alt="Taiwan Silicone Molding Facility" style="width: 44%; height: 96px; object-fit: cover;"/>
    <div style="padding: 8px 14px; font-size: 8.3pt; color: #334155; line-height: 1.5;">
      <strong style="color: #0F172A; display: block; margin-bottom: 3px;">Why US &amp; EU Buyers Source from Jun-Hsiang Taiwan</strong>
      Direct factory engineering communication in English, tariff-resilient Made-in-Taiwan origin, strict IP confidentiality under mutual NDA, and flexible support from prototype tooling to recurring production runs.
    </div>
  </div>

  <div class="rfq-card">
    <h3>RFQ Checklist — What to Include for a Fast Quotation</h3>
    <ul class="rfq-list">
      <li>2D / 3D CAD files (STEP, IGS, PDF, or DWG)</li>
      <li>Target elastomer (LSR, HCR, EPDM, NBR, FKM, FVMQ)</li>
      <li>Required Shore A hardness &amp; color specification</li>
      <li>Regulatory standards (US FDA, EU LFGB, REACH, RoHS)</li>
      <li>Estimated pilot quantity &amp; annual volume (EAU)</li>
      <li>Bonding substrate details (if metal/plastic overmolding)</li>
    </ul>
  </div>

  <div class="contact-box">
    <div>
      <h3>Start Your Engineering Review &amp; Quotation</h3>
      <p><strong>Contact:</strong> Andy Hsu — Export &amp; Engineering Sales</p>
      <p><strong>Email:</strong> andy_hsu@jun-hsiang.com.tw</p>
      <p><strong>Direct RFQ Portal:</strong> https://www.jun-hsiang.com.tw/en/#contact</p>
    </div>
    <div class="contact-right">
      <div><strong>Jun-Hsiang Enterprise Co., Ltd.</strong></div>
      <div>No. 3, Ln. 345, Xinshu Rd., Xinzhuang Dist.</div>
      <div>New Taipei City 242, Taiwan</div>
      <div>Tel: +886-2-2203-9918 | Fax: +886-2-2206-6968</div>
    </div>
  </div>

  <div class="page-footer">
    <span>Jun-Hsiang Enterprise Co., Ltd. — ISO 9001 Custom Silicone &amp; Rubber Parts Manufacturer (Taiwan)</span>
    <span>Page 2 of 2</span>
  </div>
</div>

</body>
</html>
"""

def main():
    os.makedirs(os.path.dirname(OUT_PDF), exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tmp:
        tmp.write(HTML_CONTENT)
        tmp_path = tmp.name

    try:
        file_url = "file:///" + tmp_path.replace("\\", "/")
        cmd = [
            CHROME_PATH,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--print-to-pdf-no-header",
            f"--print-to-pdf={OUT_PDF}",
            file_url,
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        assert res.returncode == 0 and os.path.exists(OUT_PDF), f"Chrome PDF failed: {res.stderr}"
        size_kb = os.path.getsize(OUT_PDF) / 1024
        print(f"Generated {OUT_PDF} ({size_kb:.1f} KB)")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

if __name__ == "__main__":
    main()
