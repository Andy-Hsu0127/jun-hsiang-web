import base64
import os
import subprocess
import tempfile

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUT_PDF = os.path.abspath(os.path.join("pdf", "en", "Jun-Hsiang-Enterprise-Company-Profile-EN.pdf"))

def img_uri(rel_path):
    abs_p = os.path.abspath(rel_path)
    if not os.path.exists(abs_p):
        return ""
    ext = os.path.splitext(abs_p)[1].lower().lstrip(".")
    mime = "image/png" if ext == "png" else ("image/webp" if ext == "webp" else "image/jpeg")
    b64 = base64.b64encode(open(abs_p, "rb").read()).decode("ascii")
    return f"data:{mime};base64,{b64}"

logo = img_uri("images/logo.png")
p_keypads = img_uri("images/brochure/prod-keypads.jpg")
p_orings = img_uri("images/brochure/prod-orings.jpg")
p_gaskets = img_uri("images/brochure/prod-gaskets.jpg")
p_medkb = img_uri("images/brochure/prod-medical-kb.jpg")
e_lsr = img_uri("images/brochure/equip-lsr.jpg")
e_vac = img_uri("images/brochure/equip-vacuum-press.jpg")
q_25d = img_uri("images/brochure/qc-25d-optical.jpg")
q_load = img_uri("images/brochure/qc-load-curve.jpg")

HTML_CONTENT = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>Jun-Hsiang Enterprise Co., Ltd. — Company Profile &amp; Manufacturing Capabilities</title>
<style>
  @page {{ size: A4; margin: 0; }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #0F172A; background: #FFFFFF;
    -webkit-print-color-adjust: exact; print-color-adjust: exact;
  }}
  .page {{
    width: 210mm; height: 297mm;
    padding: 13mm 15mm 12mm 15mm;
    position: relative; page-break-after: always; overflow: hidden;
  }}
  .page:last-child {{ page-break-after: auto; }}
  .header-bar {{
    background: #0A0F1C; color: #F8FAFC;
    padding: 14px 18px; border-radius: 10px; border-bottom: 4px solid #D4A843;
    display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;
  }}
  .header-sm {{ padding: 10px 16px; margin-bottom: 10px; }}
  .brand-left {{ display: flex; align-items: center; gap: 11px; }}
  .brand-left img {{ width: 40px; height: 40px; border-radius: 8px; background: #fff; padding: 3px; }}
  .header-sm .brand-left img {{ width: 28px; height: 28px; }}
  .brand-name {{ font-size: 15.5pt; font-weight: 800; color: #FFFFFF; margin: 0; }}
  .header-sm .brand-name {{ font-size: 12pt; }}
  .brand-sub {{ font-size: 8.5pt; color: #D4A843; font-weight: 600; margin: 2px 0 0; }}
  .header-sm .brand-sub {{ font-size: 7.6pt; }}
  .header-badges {{ text-align: right; font-size: 8pt; line-height: 1.5; color: #CBD5E1; }}
  .header-badges strong {{ color: #FDE68A; }}
  .pill-row {{ display: flex; gap: 7px; flex-wrap: wrap; margin-bottom: 11px; }}
  .pill {{
    background: #F1F5F9; border: 1px solid #CBD5E1; color: #0F172A;
    font-size: 7.9pt; font-weight: 700; padding: 3.5px 9px; border-radius: 999px;
  }}
  .pill.gold {{ background: #FEF9C3; border-color: #D4A843; color: #713F12; }}
  .section-title {{
    font-size: 10.8pt; font-weight: 800; color: #0A0F1C;
    border-left: 4px solid #D4A843; padding-left: 9px;
    margin: 11px 0 7px; text-transform: uppercase; letter-spacing: 0.4px;
  }}
  p.lead {{ font-size: 9pt; line-height: 1.52; color: #334155; margin: 0 0 9px; }}
  .facts-table {{ width: 100%; border-collapse: collapse; font-size: 8.3pt; margin-bottom: 10px; }}
  .facts-table td {{ padding: 5.5px 8px; border-bottom: 1px solid #E2E8F0; vertical-align: top; }}
  .facts-table td.k {{ width: 22%; font-weight: 700; color: #0F172A; background: #F8FAFC; }}
  .facts-table td.v {{ width: 28%; color: #334155; }}
  .fhpq-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 10px; }}
  .fhpq-card {{
    background: #F8FAFC; border: 1px solid #CBD5E1; border-top: 3px solid #D4A843;
    border-radius: 7px; padding: 8px 9px;
  }}
  .fhpq-card .letter {{ font-size: 11pt; font-weight: 900; color: #0A0F1C; margin-bottom: 2px; }}
  .fhpq-card .letter span {{ color: #B45309; }}
  .fhpq-card p {{ margin: 0; font-size: 7.7pt; color: #475569; line-height: 1.42; }}
  .timeline {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 7px; }}
  .tl-item {{
    border: 1px solid #E2E8F0; border-radius: 6px; padding: 6.5px 9px; background: #FFFFFF;
  }}
  .tl-yr {{ display: inline-block; background: #0A0F1C; color: #FDE68A; font-size: 7.5pt; font-weight: 800; padding: 1.5px 7px; border-radius: 999px; margin-bottom: 3px; }}
  .tl-item p {{ margin: 0; font-size: 7.7pt; color: #334155; line-height: 1.38; }}
  .photo-grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 10px; }}
  .photo-card {{
    border: 1px solid #CBD5E1; border-radius: 8px; overflow: hidden; background: #F8FAFC;
  }}
  .photo-card img {{ width: 100%; height: 146px; object-fit: contain; background: #FFFFFF; display: block; border-bottom: 1px solid #E2E8F0; padding: 4px; }}
  .photo-card.equip img {{ height: 158px; object-fit: contain; background: #F8FAFC; }}
  .photo-cap {{ padding: 6px 10px; }}
  .photo-cap strong {{ display: block; font-size: 8.6pt; color: #0F172A; margin-bottom: 2px; }}
  .photo-cap span {{ display: block; font-size: 7.6pt; color: #475569; line-height: 1.35; }}
  .cap-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }}
  .cap-box {{
    border: 1px solid #CBD5E1; border-top: 3px solid #0D9488;
    border-radius: 7px; padding: 8px 10px; background: #FFFFFF;
  }}
  .cap-box h3 {{ font-size: 9pt; margin: 0 0 3px; color: #0F172A; }}
  .cap-box p {{ font-size: 7.9pt; line-height: 1.42; color: #475569; margin: 0; }}
  .equip-table {{ width: 100%; border-collapse: collapse; font-size: 8pt; }}
  .equip-table th {{ background: #0A0F1C; color: #FDE68A; text-align: left; padding: 6px 9px; font-size: 8.2pt; }}
  .equip-table td {{ padding: 5.5px 9px; border-bottom: 1px solid #E2E8F0; color: #334155; vertical-align: top; }}
  .equip-table tr:nth-child(even) td {{ background: #F8FAFC; }}
  .ind-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 11px; }}
  .ind-box {{ background: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 7px; padding: 8px 10px; }}
  .ind-box strong {{ display: block; font-size: 8.6pt; color: #0F172A; margin-bottom: 2px; }}
  .ind-box span {{ font-size: 7.7pt; color: #475569; line-height: 1.38; display: block; }}
  .steps {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 11px; }}
  .step {{ border: 1px solid #E2E8F0; border-radius: 7px; padding: 8px 10px; background: #FFFFFF; }}
  .step-num {{ display: inline-block; background: #0A0F1C; color: #D4A843; font-weight: 800; font-size: 7.3pt; padding: 2px 7px; border-radius: 999px; margin-bottom: 3px; }}
  .step strong {{ display: block; font-size: 8.5pt; color: #0F172A; margin-bottom: 2px; }}
  .step p {{ margin: 0; font-size: 7.7pt; color: #475569; line-height: 1.38; }}
  .rfq-card {{
    background: #F8FAFC; border: 1px solid #CBD5E1; border-left: 4px solid #0D9488;
    border-radius: 8px; padding: 10px 14px; margin-bottom: 12px;
  }}
  .rfq-card h3 {{ margin: 0 0 6px; font-size: 9.5pt; color: #0F172A; }}
  .rfq-list {{ margin: 0; padding-left: 16px; font-size: 8.2pt; color: #334155; line-height: 1.55; columns: 2; column-gap: 18px; }}
  .contact-box {{
    background: #0A0F1C; color: #F8FAFC; border-radius: 10px;
    padding: 14px 18px; border-top: 4px solid #D4A843;
    display: flex; justify-content: space-between; align-items: center;
  }}
  .contact-box h3 {{ margin: 0 0 4px; color: #FDE68A; font-size: 10.6pt; }}
  .contact-box p {{ margin: 2px 0; font-size: 8.4pt; color: #E2E8F0; }}
  .contact-right {{ text-align: right; font-size: 8.3pt; color: #CBD5E1; line-height: 1.58; }}
  .contact-right strong {{ color: #FFFFFF; }}
  .page-footer {{
    position: absolute; bottom: 7.5mm; left: 15mm; right: 15mm;
    display: flex; justify-content: space-between; font-size: 7.4pt; color: #64748B;
    border-top: 1px solid #E2E8F0; padding-top: 5px;
  }}
</style>
</head>
<body>

<!-- PAGE 1: COMPANY PROFILE, MILESTONES & F.H.P.Q. -->
<div class="page">
  <div class="header-bar">
    <div class="brand-left">
      <img src="{logo}" alt="Jun-Hsiang Logo"/>
      <div>
        <div class="brand-name">Jun-Hsiang Enterprise Co., Ltd.</div>
        <div class="brand-sub">Custom Silicone &amp; Rubber Parts Manufacturer in Taiwan • Est. 1991</div>
      </div>
    </div>
    <div class="header-badges">
      <div><strong>ISO 9001:2015 Certified</strong> • 35 Years Experience</div>
      <div>100% Made in Taiwan (Non-China Supply Chain)</div>
      <div>www.jun-hsiang.com.tw/en/</div>
    </div>
  </div>

  <div class="pill-row">
    <span class="pill gold">100% Made in Taiwan (MIT)</span>
    <span class="pill">LSR Liquid Silicone Injection</span>
    <span class="pill">HCR Vacuum Compression</span>
    <span class="pill">Silicone-to-Metal / Plastic Overmolding</span>
    <span class="pill">In-House 2.5D QC Lab</span>
    <span class="pill">Mutual NDA Ready</span>
  </div>

  <div class="section-title">Company Profile</div>
  <p class="lead">
    Founded in September 1991 in New Taipei City, Taiwan, <strong>Jun-Hsiang Enterprise Co., Ltd.</strong> is an ISO 9001:2015-certified custom silicone and rubber molding manufacturer serving industrial, automotive, medical, electronics, and food-contact customers across the US, Europe, and Japan. Combining over three decades of mold tooling craftsmanship with LSR injection molding, vacuum compression presses, and an in-house 2.5D optical &amp; mechanical inspection lab, we deliver reliable Made-in-Taiwan production from pilot sampling to scalable mass production.
  </p>

  <table class="facts-table">
    <tr>
      <td class="k">Founded</td><td class="v">September 1991 (35 Years)</td>
      <td class="k">Paid-in Capital</td><td class="v">NTD 12,000,000</td>
    </tr>
    <tr>
      <td class="k">Factory Address</td><td class="v">No. 1 &amp; 3, Ln. 345, Xinshu Rd., Xinzhuang Dist., New Taipei City 242, Taiwan</td>
      <td class="k">Quality System</td><td class="v">ISO 9001:2015 Certified (Since 2017; latest copy available upon RFQ)</td>
    </tr>
    <tr>
      <td class="k">Material Compliance</td><td class="v">US FDA 21 CFR 177.2600, EU LFGB, REACH, RoHS, ISO 10993 LSR options</td>
      <td class="k">IP &amp; Export Support</td><td class="v">Mutual NDA prior to CAD review; Certificate of Origin (MIT)</td>
    </tr>
  </table>

  <div class="section-title">F.H.P.Q. Operating Philosophy</div>
  <div class="fhpq-grid">
    <div class="fhpq-card">
      <div class="letter"><span>F</span>riend</div>
      <p>Every customer is a long-term partner—supported with early engineering discussion, transparent quoting, and responsive trial sampling.</p>
    </div>
    <div class="fhpq-card">
      <div class="letter"><span>H</span>onesty</div>
      <p>Integrity is our foundation. We never overpromise—once we commit to a specification or delivery schedule, we stand behind it fully.</p>
    </div>
    <div class="fhpq-card">
      <div class="letter"><span>P</span>rofession</div>
      <p>Focused exclusively on silicone &amp; rubber molding (LSR injection, vacuum compression, overmolding) with continuous tooling refinement.</p>
    </div>
    <div class="fhpq-card">
      <div class="letter"><span>Q</span>uality</div>
      <p>Guided by the Three-No Quality Principle: <strong>Do Not Accept Defects, Do Not Produce Defects, Do Not Ship Defects</strong>.</p>
    </div>
  </div>

  <div class="section-title">Company Milestones (1991 – Present)</div>
  <div class="timeline">
    <div class="tl-item"><span class="tl-yr">1991</span><p>Founded in Xinzhuang, New Taipei City by Mr. Chi-Lung Hsu, specializing in precision rubber parts.</p></div>
    <div class="tl-item"><span class="tl-yr">1993</span><p>Added vacuum compression molding presses to manufacture industrial silicone &amp; conductive keypads.</p></div>
    <div class="tl-item"><span class="tl-yr">1999</span><p>Relocated to expanded Xinshu Rd. facility in Xinzhuang to support growing OEM export demand.</p></div>
    <div class="tl-item"><span class="tl-yr">2001</span><p>Expanded into high-clarity swim goggles, straps, and durable outdoor/sports silicone accessories.</p></div>
    <div class="tl-item"><span class="tl-yr">2010</span><p>Launched hygienic medical-grade washable silicone keyboards for international export markets.</p></div>
    <div class="tl-item"><span class="tl-yr">2012</span><p>Entered smartphone &amp; 3C electronics precision rubber seals and protective elastomer components.</p></div>
    <div class="tl-item"><span class="tl-yr">2016</span><p>Expanded into electric scooter &amp; automotive waterproof sealing components and harness parts.</p></div>
    <div class="tl-item"><span class="tl-yr">2017</span><p>Achieved <strong>ISO 9001:2015</strong> international quality management certification for silicone &amp; rubber manufacturing.</p></div>
    <div class="tl-item"><span class="tl-yr">2018+</span><p>Facility expansion adding <strong>LSR Liquid Silicone Injection</strong>, 2.5D Optical Inspection, Life Cycle &amp; Load Curve Testers.</p></div>
  </div>

  <div class="page-footer">
    <span>Jun-Hsiang Enterprise Co., Ltd. — Company Profile &amp; Capability Brochure</span>
    <span>Page 1 of 4</span>
  </div>
</div>

<!-- PAGE 2: REAL PRODUCT SHOWCASE & CORE CAPABILITIES -->
<div class="page">
  <div class="header-bar header-sm">
    <div class="brand-left">
      <img src="{logo}" alt="Logo"/>
      <div>
        <div class="brand-name">Product Showcase &amp; Core Molding Capabilities</div>
        <div class="brand-sub">Actual Production Parts Molded at Our New Taipei City, Taiwan Facility</div>
      </div>
    </div>
    <div class="header-badges"><div><strong>ISO 9001:2015</strong> • 100% Made in Taiwan</div></div>
  </div>

  <div class="section-title">Representative Molded Parts (Actual Factory Production)</div>
  <div class="photo-grid-2">
    <div class="photo-card">
      <img src="{p_keypads}" alt="Industrial Silicone Keypads"/>
      <div class="photo-cap">
        <strong>Industrial &amp; Conductive Silicone Keypads</strong>
        <span>Wear-resistant, custom actuation force, multi-color screen printing, carbon pills &amp; backlit legends.</span>
      </div>
    </div>
    <div class="photo-card">
      <img src="{p_orings}" alt="Precision Silicone O-Rings"/>
      <div class="photo-cap">
        <strong>Custom Silicone &amp; Elastomer O-Rings</strong>
        <span>Chemical-, acid/alkali-, and temperature-resistant custom seals in LSR, HCR, FVMQ, Viton (FKM) &amp; EPDM.</span>
      </div>
    </div>
    <div class="photo-card">
      <img src="{p_gaskets}" alt="Waterproof Frame Gaskets"/>
      <div class="photo-cap">
        <strong>Precision Waterproof Frame Gaskets &amp; Seals</strong>
        <span>Complex perimeter gaskets for enclosures, industrial instruments, automotive &amp; outdoor housings.</span>
      </div>
    </div>
    <div class="photo-card">
      <img src="{p_medkb}" alt="Medical Washable Silicone Keyboards"/>
      <div class="photo-cap">
        <strong>Medical &amp; Hygienic Silicone Covers / Keyboards</strong>
        <span>Non-toxic, odorless, dustproof, and washable platinum-cured silicone covers for clinical equipment.</span>
      </div>
    </div>
  </div>

  <div class="section-title">Core Molding &amp; Secondary Processing Capabilities</div>
  <div class="cap-grid">
    <div class="cap-box">
      <h3>1. LSR Liquid Silicone Injection Molding</h3>
      <p>Two-part platinum-cured LSR injection molding with precision cold-runner and multi-cavity tooling. Suited for thin walls, micro-features, large-shot thick parts, and controlled-flash cleanliness.</p>
    </div>
    <div class="cap-box">
      <h3>2. HCR Solid Silicone &amp; Rubber Compression</h3>
      <p>Vacuum compression molding for High Consistency Rubber (HCR), EPDM, NBR, Viton (FKM), and Fluorosilicone (FVMQ). Cost-effective tooling for industrial gaskets, O-rings, keypads, and mounts.</p>
    </div>
    <div class="cap-box">
      <h3>3. Silicone-to-Metal &amp; Plastic Overmolding</h3>
      <p>Insert molding and bonding onto aluminum, steel, stainless steel, brass, and engineering thermoplastics (PC, PA, PBT). Supports both primer-controlled bonding and primerless self-bonding LSR.</p>
    </div>
    <div class="cap-box">
      <h3>4. Specialty Elastomers &amp; Surface Finishing</h3>
      <p>Custom Shore A 10°–80° formulations, oil-bleeding self-lubricating silicone for wire harness seals, plus in-house screen printing, IR tunnel curing, and post-cure baking ovens.</p>
    </div>
  </div>

  <div class="page-footer">
    <span>Jun-Hsiang Enterprise Co., Ltd. — Actual Production Parts &amp; Capabilities</span>
    <span>Page 2 of 4</span>
  </div>
</div>

<!-- PAGE 3: IN-HOUSE EQUIPMENT & QC LAB -->
<div class="page">
  <div class="header-bar header-sm">
    <div class="brand-left">
      <img src="{logo}" alt="Logo"/>
      <div>
        <div class="brand-name">Production Equipment &amp; QC Inspection Lab</div>
        <div class="brand-sub">Direct Factory Machinery &amp; Optical / Mechanical Verification in Taiwan</div>
      </div>
    </div>
    <div class="header-badges" style="white-space:nowrap;"><div><strong>andy_hsu@jun-hsiang.com.tw</strong> | +886-2-2203-9918</div></div>
  </div>

  <div class="section-title">Key Molding &amp; Quality Inspection Machinery (Actual Facility)</div>
  <div class="photo-grid-2">
    <div class="photo-card equip">
      <img src="{e_lsr}" alt="LSR Liquid Silicone Injection Machine"/>
      <div class="photo-cap">
        <strong>Vertical LSR Liquid Silicone Injection Press</strong>
        <span>Precision A/B metering system for platinum-cured LSR injection &amp; insert overmolding.</span>
      </div>
    </div>
    <div class="photo-card equip">
      <img src="{e_vac}" alt="Vacuum Compression Molding Press"/>
      <div class="photo-cap">
        <strong>Vacuum Compression Molding Press</strong>
        <span>Vacuum-assisted degassing for bubble-free HCR solid silicone &amp; specialty rubber parts.</span>
      </div>
    </div>
    <div class="photo-card equip">
      <img src="{q_25d}" alt="HO STAR 2.5D Optical Measuring System"/>
      <div class="photo-cap">
        <strong>2.5D Optical Dimensional Measuring System</strong>
        <span>Non-contact optical inspection for elastomer geometries that deform under physical calipers.</span>
      </div>
    </div>
    <div class="photo-card equip">
      <img src="{q_load}" alt="AIKOH Force-Displacement Load Curve Tester"/>
      <div class="photo-cap">
        <strong>Force-Displacement / Load Curve Tester</strong>
        <span>Measures keypad actuation force, tactile click ratio, and elastomer compression behavior.</span>
      </div>
    </div>
  </div>

  <div class="section-title">Complete In-House Equipment &amp; Inspection Inventory</div>
  <table class="equip-table">
    <thead>
      <tr>
        <th style="width: 24%;">Department</th>
        <th style="width: 76%;">In-House Machinery &amp; Verification Instruments</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Molding &amp; Compounding</strong></td>
        <td>LSR Liquid Silicone Injection Molding Machines • Vacuum Compression Molding Presses • Two-Roll Rubber Mixing Mills • Precision Material Cutting Machines • Post-Cure Baking Ovens</td>
      </tr>
      <tr>
        <td><strong>Printing &amp; Finishing</strong></td>
        <td>Flatbed &amp; Semi-Rigid Screen Printing Machines • Three-Roll Ink Mill • Infrared (IR) Conveyor Tunnel Dryers • Clean Inspection &amp; Trimming Workstations</td>
      </tr>
      <tr>
        <td><strong>Quality &amp; Reliability Lab</strong></td>
        <td>2.5D Optical Measuring Machine • Force-Displacement Curve Tester • Manual Push-Pull Force Gauge • Keypad Life Cycle Tester • Surface Abrasion Resistance Tester • Optical Magnifiers • Shore A Durometer • Digital Calipers &amp; Thickness Gauges</td>
      </tr>
    </tbody>
  </table>

  <div class="page-footer">
    <span>Jun-Hsiang Enterprise Co., Ltd. — In-House Equipment &amp; Quality Inspection Lab</span>
    <span>Page 3 of 4</span>
  </div>
</div>

<!-- PAGE 4: INDUSTRIES, WORKFLOW & DIRECT RFQ -->
<div class="page">
  <div class="header-bar header-sm">
    <div class="brand-left">
      <img src="{logo}" alt="Logo"/>
      <div>
        <div class="brand-name">Target Industries, Sourcing Workflow &amp; Direct RFQ</div>
        <div class="brand-sub">Build-to-Print Silicone &amp; Rubber Supply Chain Partner in Taiwan</div>
      </div>
    </div>
    <div class="header-badges"><div><strong>www.jun-hsiang.com.tw/en/</strong></div></div>
  </div>

  <div class="section-title">Target Industries &amp; Representative Applications</div>
  <div class="ind-grid">
    <div class="ind-box">
      <strong>Automotive &amp; EV Harness</strong>
      <span>Self-lubricating single wire seals (SWS), waterproof connector seals, LSR overmolded PA66 sockets.</span>
    </div>
    <div class="ind-box">
      <strong>Medical &amp; Respiratory</strong>
      <span>FDA &amp; ISO 10993 platinum-cured LSR respiratory mask cushions, washable keyboards, hygienic seals.</span>
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
      <p>Select LSR vs. HCR, Shore A hardness, operating environment, and FDA / LFGB / REACH compliance.</p>
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
      <strong>T1 Sampling &amp; 2.5D QC</strong>
      <p>First-article trial molding with 2.5D optical dimensional inspection and customer sample approval.</p>
    </div>
    <div class="step">
      <span class="step-num">STEP 06</span>
      <strong>Mass Production &amp; Export</strong>
      <p>ISO 9001:2015 batch quality verification, clean packaging, and global export with MIT Certificate of Origin.</p>
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
      <div>No. 1 &amp; 3, Ln. 345, Xinshu Rd., Xinzhuang Dist.</div>
      <div>New Taipei City 242, Taiwan</div>
      <div>Tel: +886-2-2203-9918 | Fax: +886-2-2206-6968</div>
    </div>
  </div>

  <div class="page-footer">
    <span>Jun-Hsiang Enterprise Co., Ltd. — ISO 9001:2015 Custom Silicone &amp; Rubber Parts Manufacturer (Taiwan)</span>
    <span>Page 4 of 4</span>
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
