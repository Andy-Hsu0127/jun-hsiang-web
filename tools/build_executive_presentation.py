"""
Build High-Impact 16:9 Executive Presentation & PDF for Jun-Hsiang Enterprise (Pass 2 Polish)
Refinements based on visual review:
1. Slide 1 (Cover): Add right-hand 2x2 showcase visual featuring genuine factory/product imagery, balancing the 16:9 widescreen canvas.
2. Slide 2 (Heritage): Full-width balanced 2-column layout (Left: 3 large metric cards; Right: 4 F.H.P.Q. operational pillars).
3. Slide 3 & 4 (Products & Machinery): Increased card height (520px) and refined image aspect ratio for maximum visual impact.
4. Slide 5 (Workflow & RFQ): Perfectly symmetric 1fr:1fr 2-column layout. Replaced potential unicode glyphs with clean, universal text/symbols.
"""

import base64
import os
import subprocess
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

WORKSPACE = Path("p:/tets")
IMAGES_DIR = WORKSPACE / "images" / "brochure"
LOGO_FILE = WORKSPACE / "images" / "logo.png"
OUTPUT_PDF = WORKSPACE / "pdf" / "en" / "Jun-Hsiang-Enterprise-Company-Profile-EN.pdf"
OUTPUT_PPTX = WORKSPACE / "pdf" / "en" / "Jun-Hsiang-Enterprise-Company-Profile-EN.pptx"
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

LOGO_URI = b64_img(LOGO_FILE)
PROD_KEYPADS_URI = b64_img(IMAGES_DIR / "prod-keypads.jpg")
PROD_ORINGS_URI = b64_img(IMAGES_DIR / "prod-orings.jpg")
PROD_GASKETS_URI = b64_img(IMAGES_DIR / "prod-gaskets.jpg")
PROD_MEDKB_URI = b64_img(IMAGES_DIR / "prod-medical-kb.jpg")
EQUIP_LSR_URI = b64_img(IMAGES_DIR / "equip-lsr.jpg")
EQUIP_VAC_URI = b64_img(IMAGES_DIR / "equip-vacuum-press.jpg")
QC_25D_URI = b64_img(IMAGES_DIR / "qc-25d-optical.jpg")
QC_LOAD_URI = b64_img(IMAGES_DIR / "qc-load-curve.jpg")

HTML_TEMPLATE = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Jun-Hsiang Enterprise - Company Profile</title>
<style>
  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}

  @page {{
    size: 16in 9in;
    margin: 0;
  }}

  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    background-color: #060b1a;
    color: #f8fafc;
    -webkit-font-smoothing: antialiased;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}

  .slide {{
    width: 16in;
    height: 9in;
    position: relative;
    overflow: hidden;
    page-break-after: always;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 0.7in 0.9in;
    background: radial-gradient(circle at 85% 15%, rgba(30, 58, 138, 0.32) 0%, rgba(6, 11, 26, 0.98) 70%);
  }}

  .slide:last-child {{
    page-break-after: auto;
  }}

  .slide::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image: 
      linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
    background-size: 64px 64px;
    pointer-events: none;
    z-index: 1;
  }}

  .slide-content {{
    position: relative;
    z-index: 2;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  /* Header */
  .slide-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }}

  .brand-group {{
    display: flex;
    align-items: center;
    gap: 16px;
  }}

  .brand-logo {{
    height: 44px;
    width: auto;
    object-fit: contain;
  }}

  .brand-name {{
    font-size: 19px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #f1f5f9;
    text-transform: uppercase;
  }}

  .slide-category {{
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2.5px;
    color: #38bdf8;
    text-transform: uppercase;
    background: rgba(56, 189, 248, 0.1);
    border: 1px solid rgba(56, 189, 248, 0.3);
    padding: 6px 16px;
    border-radius: 999px;
  }}

  .slide-title-block {{
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}

  .slide-title {{
    font-size: 40px;
    font-weight: 800;
    line-height: 1.15;
    color: #ffffff;
    letter-spacing: -0.5px;
  }}

  .slide-subtitle {{
    font-size: 16.5px;
    font-weight: 400;
    color: #94a3b8;
  }}

  /* Footer */
  .slide-footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    font-size: 13.5px;
    color: #64748b;
  }}

  .footer-left {{
    display: flex;
    align-items: center;
    gap: 24px;
  }}

  .footer-item {{
    display: flex;
    align-items: center;
    gap: 8px;
  }}

  .footer-dot {{
    width: 6px;
    height: 6px;
    background-color: #38bdf8;
    border-radius: 50%;
  }}

  /* Slide 1 Cover Hero Layout */
  .cover-grid {{
    display: grid;
    grid-template-columns: 1.15fr 0.85fr;
    gap: 56px;
    align-items: center;
    margin: auto 0;
  }}

  .cover-body {{
    display: flex;
    flex-direction: column;
  }}

  .cover-eyebrow {{
    font-size: 14.5px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #f59e0b;
    margin-bottom: 16px;
  }}

  .cover-title {{
    font-size: 58px;
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -1px;
    color: #ffffff;
    margin-bottom: 22px;
  }}

  .cover-title span {{
    color: #38bdf8;
  }}

  .cover-desc {{
    font-size: 18.5px;
    font-weight: 300;
    line-height: 1.6;
    color: #cbd5e1;
    margin-bottom: 36px;
  }}

  .cover-badges {{
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
  }}

  .cover-badge {{
    padding: 10px 18px;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 8px;
    font-size: 13.5px;
    font-weight: 600;
    color: #e2e8f0;
  }}

  .cover-badge strong {{
    color: #f59e0b;
  }}

  .cover-hero-mosaic {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 240px 240px;
    gap: 16px;
  }}

  .mosaic-card {{
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    overflow: hidden;
    position: relative;
  }}

  .mosaic-card img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
  }}

  .mosaic-label {{
    position: absolute;
    bottom: 12px;
    left: 12px;
    right: 12px;
    background: rgba(6, 11, 26, 0.85);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: 0.5px;
  }}

  /* Slide 2 Heritage */
  .heritage-grid {{
    display: grid;
    grid-template-columns: 420px 1fr;
    gap: 48px;
    align-items: center;
    margin: auto 0;
  }}

  .stat-stack {{
    display: flex;
    flex-direction: column;
    gap: 20px;
  }}

  .stat-card {{
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 22px 26px;
  }}

  .stat-num {{
    font-size: 50px;
    font-weight: 800;
    color: #38bdf8;
    line-height: 1;
    letter-spacing: -1px;
    margin-bottom: 6px;
  }}

  .stat-label {{
    font-size: 16px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 4px;
  }}

  .stat-sub {{
    font-size: 13px;
    color: #94a3b8;
    line-height: 1.45;
  }}

  .pillars-container {{
    display: flex;
    flex-direction: column;
    gap: 16px;
  }}

  .pillar-card {{
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 20px 28px;
    display: grid;
    grid-template-columns: 140px 1fr;
    gap: 24px;
    align-items: center;
  }}

  .pillar-head {{
    font-size: 19px;
    font-weight: 700;
    color: #f59e0b;
  }}

  .pillar-desc {{
    font-size: 14.5px;
    line-height: 1.55;
    color: #cbd5e1;
  }}

  /* Slide 3 & 4: 4-Card Photo Grids */
  .cards-grid-4 {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 26px;
    margin: auto 0;
  }}

  .showcase-card {{
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    height: 520px;
  }}

  .card-img-wrap {{
    height: 255px;
    width: 100%;
    overflow: hidden;
    position: relative;
    background-color: #0b1329;
  }}

  .card-img-wrap img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
  }}

  .card-badge {{
    position: absolute;
    top: 12px;
    left: 12px;
    background: rgba(6, 11, 26, 0.9);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.8px;
    color: #38bdf8;
    text-transform: uppercase;
  }}

  .card-content {{
    padding: 22px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    flex-grow: 1;
  }}

  .card-title {{
    font-size: 19px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 12px;
    line-height: 1.3;
  }}

  .card-bullets {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 7px;
    font-size: 13.5px;
    color: #cbd5e1;
    line-height: 1.45;
  }}

  .card-bullets li {{
    position: relative;
    padding-left: 16px;
  }}

  .card-bullets li::before {{
    content: '▪';
    position: absolute;
    left: 0;
    color: #f59e0b;
    font-size: 14px;
  }}

  .card-spec {{
    margin-top: 14px;
    padding-top: 12px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    font-size: 12px;
    color: #38bdf8;
    font-weight: 600;
  }}

  /* Slide 5 Workflow */
  .closing-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 48px;
    margin: auto 0;
    align-items: center;
  }}

  .workflow-list {{
    display: flex;
    flex-direction: column;
    gap: 14px;
  }}

  .workflow-step {{
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    padding: 16px 20px;
    display: flex;
    align-items: center;
    gap: 18px;
  }}

  .step-num {{
    width: 36px;
    height: 36px;
    background: rgba(56, 189, 248, 0.15);
    border: 1px solid rgba(56, 189, 248, 0.3);
    color: #38bdf8;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 15px;
    flex-shrink: 0;
  }}

  .step-info {{
    flex-grow: 1;
  }}

  .step-title {{
    font-size: 16px;
    font-weight: 700;
    color: #ffffff;
  }}

  .step-desc {{
    font-size: 13px;
    color: #94a3b8;
    margin-top: 2px;
  }}

  .contact-box {{
    background: linear-gradient(145deg, rgba(30, 58, 138, 0.35) 0%, rgba(15, 23, 42, 0.85) 100%);
    border: 1px solid rgba(56, 189, 248, 0.35);
    border-radius: 16px;
    padding: 34px 38px;
    display: flex;
    flex-direction: column;
    gap: 22px;
    box-shadow: 0 16px 40px rgba(0,0,0,0.4);
  }}

  .contact-box-title {{
    font-size: 22px;
    font-weight: 800;
    color: #ffffff;
  }}

  .rfq-checklist {{
    background: rgba(6, 11, 26, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    padding: 16px 20px;
  }}

  .rfq-checklist-title {{
    font-size: 12.5px;
    font-weight: 700;
    color: #f59e0b;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-bottom: 8px;
  }}

  .rfq-checklist ul {{
    list-style: none;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px;
    font-size: 12.5px;
    color: #cbd5e1;
  }}

  .rfq-checklist li::before {{
    content: '✓ ';
    color: #38bdf8;
    font-weight: bold;
  }}

  .contact-details {{
    display: flex;
    flex-direction: column;
    gap: 12px;
    font-size: 14.5px;
    color: #e2e8f0;
  }}

  .contact-row {{
    display: flex;
    align-items: center;
    gap: 12px;
  }}

  .contact-label {{
    color: #94a3b8;
    min-width: 75px;
    font-size: 13.5px;
  }}

  .contact-val strong {{
    color: #ffffff;
    font-weight: 600;
  }}
</style>
</head>
<body>

<!-- SLIDE 1: COVER -->
<div class="slide" id="slide-1">
  <div class="slide-content">
    <div class="slide-header">
      <div class="brand-group">
        <img class="brand-logo" src="{LOGO_URI}" alt="Logo">
        <div class="brand-name">Jun-Hsiang Enterprise Co., Ltd.</div>
      </div>
      <div class="slide-category">B2B OEM Capabilities</div>
    </div>

    <div class="cover-grid">
      <div class="cover-body">
        <div class="cover-eyebrow">Taiwan Precision Silicone & Rubber Engineering</div>
        <h1 class="cover-title">Custom Silicone & Rubber<br><span>Manufacturing Capabilities</span></h1>
        <p class="cover-desc">
          Specializing in Liquid Silicone Rubber (LSR) injection, high-vacuum compression molding, 
          and silicone-to-metal/plastic overmolding. Providing global OEM/ODM engineering co-development, 
          rapid DFM evaluation, and reliable non-China supply chain delivery.
        </p>
        <div class="cover-badges">
          <div class="cover-badge">📍 <strong>Origin:</strong> Made in Taiwan (MIT)</div>
          <div class="cover-badge">🛡️ <strong>Quality:</strong> ISO 9001:2015 Registered</div>
          <div class="cover-badge">⚡ <strong>Speed:</strong> 24–48h Engineering DFM Turnaround</div>
          <div class="cover-badge">🌐 <strong>Export:</strong> Direct to USA, EU & Japan</div>
        </div>
      </div>

      <div class="cover-hero-mosaic">
        <div class="mosaic-card">
          <img src="{PROD_KEYPADS_URI}" alt="Keypads">
          <div class="mosaic-label">Conductive Keypads</div>
        </div>
        <div class="mosaic-card">
          <img src="{EQUIP_LSR_URI}" alt="LSR Press">
          <div class="mosaic-label">Vertical LSR Injection</div>
        </div>
        <div class="mosaic-card">
          <img src="{PROD_ORINGS_URI}" alt="O-Rings">
          <div class="mosaic-label">Precision O-Rings & Seals</div>
        </div>
        <div class="mosaic-card">
          <img src="{QC_25D_URI}" alt="2.5D Optical">
          <div class="mosaic-label">2.5D Optical Inspection</div>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <div class="footer-left">
        <div class="footer-item"><div class="footer-dot"></div> Founded September 1991</div>
        <div class="footer-item"><div class="footer-dot"></div> Capitalization: NTD 12,000,000</div>
        <div class="footer-item"><div class="footer-dot"></div> New Taipei City, Taiwan</div>
      </div>
      <div class="footer-right">01 / 05</div>
    </div>
  </div>
</div>

<!-- SLIDE 2: HERITAGE -->
<div class="slide" id="slide-2">
  <div class="slide-content">
    <div class="slide-header">
      <div class="slide-title-block">
        <div class="slide-category">Company Heritage & Operational Standards</div>
        <h2 class="slide-title">Built on 35+ Years of Mold Engineering Discipline</h2>
        <div class="slide-subtitle">Operating under the F.H.P.Q. quality philosophy with transparent DFM and zero customer conflict</div>
      </div>
      <div class="brand-group">
        <img class="brand-logo" src="{LOGO_URI}" alt="Logo">
      </div>
    </div>

    <div class="heritage-grid">
      <div class="stat-stack">
        <div class="stat-card">
          <div class="stat-num">1991</div>
          <div class="stat-label">Founded in Taiwan</div>
          <div class="stat-sub">Over three decades of precision elastomeric tooling experience.</div>
        </div>
        <div class="stat-card">
          <div class="stat-num">NT$ 12M</div>
          <div class="stat-label">Paid-in Capital</div>
          <div class="stat-sub">Solid balance sheet with ongoing reinvestment in automated presses and optical metrology.</div>
        </div>
        <div class="stat-card">
          <div class="stat-num">100%</div>
          <div class="stat-label">Non-China Manufacturing</div>
          <div class="stat-sub">Zero Section 301 tariff exposure, resilient export routing, intellectual property protection.</div>
        </div>
      </div>

      <div class="pillars-container">
        <div class="pillar-card">
          <div class="pillar-head">🤝 Friend</div>
          <div class="pillar-desc">
            We partner with customer engineering teams as collaborative problem-solvers. From initial draft angle advice to parting line placement, we treat your product success as our own.
          </div>
        </div>
        <div class="pillar-card">
          <div class="pillar-head">🛡️ Honesty</div>
          <div class="pillar-desc">
            Customer tooling ownership is 100% safeguarded. We provide transparent raw material certifications (SGS, FDA, RoHS, REACH) and honest feasibility assessments prior to mold steel cutting.
          </div>
        </div>
        <div class="pillar-card">
          <div class="pillar-head">⚙️ Profession</div>
          <div class="pillar-desc">
            End-to-end in-house capabilities: 2D/3D mold flow optimization, custom rubber compounding, precision liquid injection, silk-screen printing, and secondary post-cure baking.
          </div>
        </div>
        <div class="pillar-card">
          <div class="pillar-head">🏆 Quality</div>
          <div class="pillar-desc">
            Strict adherence to the <em>"Do not accept, do not produce, and do not release defects"</em> discipline. Comprehensive in-line dimensional checks and full optical QA sign-off.
          </div>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <div class="footer-left">
        <div class="footer-item"><div class="footer-dot"></div> ISO 9001:2015 Quality Management System</div>
        <div class="footer-item"><div class="footer-dot"></div> Low MOQ Initial Support for Validated Projects</div>
      </div>
      <div class="footer-right">02 / 05</div>
    </div>
  </div>
</div>

<!-- SLIDE 3: PRODUCTS -->
<div class="slide" id="slide-3">
  <div class="slide-content">
    <div class="slide-header">
      <div class="slide-title-block">
        <div class="slide-category">Product Lines & Applications</div>
        <h2 class="slide-title">Precision Silicone & Rubber Components</h2>
        <div class="slide-subtitle">Engineered for mission-critical industrial, medical, automotive, and electronic applications</div>
      </div>
      <div class="brand-group">
        <img class="brand-logo" src="{LOGO_URI}" alt="Logo">
      </div>
    </div>

    <div class="cards-grid-4">
      <div class="showcase-card">
        <div class="card-img-wrap">
          <img src="{PROD_KEYPADS_URI}" alt="Silicone Keypads">
          <div class="card-badge">HMI Interfaces</div>
        </div>
        <div class="card-content">
          <div>
            <div class="card-title">Conductive Keypads & Actuators</div>
            <ul class="card-bullets">
              <li>Low-resistance conductive carbon pills</li>
              <li>Multi-color silk-screen & laser etching</li>
              <li>Wear-resistant PU & Epoxy top coatings</li>
              <li>Engineered actuation tactile ratio</li>
            </ul>
          </div>
          <div class="card-spec">App: Industrial remotes, POS, medical devices</div>
        </div>
      </div>

      <div class="showcase-card">
        <div class="card-img-wrap">
          <img src="{PROD_ORINGS_URI}" alt="O-Rings">
          <div class="card-badge">Precision Sealing</div>
        </div>
        <div class="card-content">
          <div>
            <div class="card-title">Custom O-Rings & Oil Seals</div>
            <ul class="card-bullets">
              <li>Silicone, FKM (Viton), EPDM, NBR & FVMQ</li>
              <li>Standard AS568, JIS B2401 & custom IDs</li>
              <li>Extreme temperature resilience (-50°C ~ 250°C)</li>
              <li>Low compression set for permanent sealing</li>
            </ul>
          </div>
          <div class="card-spec">App: Automotive harnesses, fluid valves, pumps</div>
        </div>
      </div>

      <div class="showcase-card">
        <div class="card-img-wrap">
          <img src="{PROD_GASKETS_URI}" alt="Gaskets">
          <div class="card-badge">Enclosure Protection</div>
        </div>
        <div class="card-content">
          <div>
            <div class="card-title">Precision Frame Gaskets</div>
            <ul class="card-bullets">
              <li>Complex 3D perimeter profiles with ribs</li>
              <li>IP67 / IP68 ingress protection standards</li>
              <li>Self-retaining press-in geometry designs</li>
              <li>Available in EMI conductive compounds</li>
            </ul>
          </div>
          <div class="card-spec">App: Outdoor enclosures, 5G drones, sensors</div>
        </div>
      </div>

      <div class="showcase-card">
        <div class="card-img-wrap">
          <img src="{PROD_MEDKB_URI}" alt="Medical Keyboards">
          <div class="card-badge">Biomedical & Clean</div>
        </div>
        <div class="card-content">
          <div>
            <div class="card-title">Medical Washable Keyboards</div>
            <ul class="card-bullets">
              <li>Seamless 100% watertight hygienic surface</li>
              <li>Withstands hospital-grade disinfectant wash</li>
              <li>FDA & LFGB compliant food/medical silicone</li>
              <li>Silent tactile feedback for clinical suites</li>
            </ul>
          </div>
          <div class="card-spec">App: Hospital workstations, cleanrooms, dental</div>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <div class="footer-left">
        <div class="footer-item"><div class="footer-dot"></div> Custom Shore A 10 to 90 durometer compounding</div>
        <div class="footer-item"><div class="footer-dot"></div> RoHS 2.0 & REACH compliant formulations</div>
      </div>
      <div class="footer-right">03 / 05</div>
    </div>
  </div>
</div>

<!-- SLIDE 4: MACHINERY & QC -->
<div class="slide" id="slide-4">
  <div class="slide-content">
    <div class="slide-header">
      <div class="slide-title-block">
        <div class="slide-category">Manufacturing Fleet & Metrology Lab</div>
        <h2 class="slide-title">In-House Machinery & Quality Verification</h2>
        <div class="slide-subtitle">Advanced liquid injection, vacuum compression, and certified optical measurement systems</div>
      </div>
      <div class="brand-group">
        <img class="brand-logo" src="{LOGO_URI}" alt="Logo">
      </div>
    </div>

    <div class="cards-grid-4">
      <div class="showcase-card">
        <div class="card-img-wrap">
          <img src="{EQUIP_LSR_URI}" alt="LSR Press">
          <div class="card-badge">Liquid Injection</div>
        </div>
        <div class="card-content">
          <div>
            <div class="card-title">Vertical LSR Injection Press</div>
            <ul class="card-bullets">
              <li>Chuan-Lien MIV 1500-LS precision system</li>
              <li>Computerized dynamic A/B component mixing</li>
              <li>Flash-free runner & micro-part capability</li>
              <li>Ideal for multi-cavity medical & optical seals</li>
            </ul>
          </div>
          <div class="card-spec">System: High-precision liquid silicone dosing</div>
        </div>
      </div>

      <div class="showcase-card">
        <div class="card-img-wrap">
          <img src="{EQUIP_VAC_URI}" alt="Vacuum Press">
          <div class="card-badge">Compression Fleet</div>
        </div>
        <div class="card-content">
          <div>
            <div class="card-title">Vacuum Compression Presses</div>
            <ul class="card-bullets">
              <li>High-tonnage hydraulic multi-tier platens</li>
              <li>Integrated vacuum chamber air evacuation</li>
              <li>Prevents trapped air, knit-lines, and bubbles</li>
              <li>Uniform platen thermal distribution</li>
            </ul>
          </div>
          <div class="card-spec">Capacity: High-density keypads & large pads</div>
        </div>
      </div>

      <div class="showcase-card">
        <div class="card-img-wrap">
          <img src="{QC_25D_URI}" alt="Optical Measuring">
          <div class="card-badge">Optical Metrology</div>
        </div>
        <div class="card-content">
          <div>
            <div class="card-title">HO STAR 2.5D Optical System</div>
            <ul class="card-bullets">
              <li>Non-contact sub-pixel optical edge detection</li>
              <li>Eliminates elastomeric contact deformation</li>
              <li>Full 2D drawing overlay & profile tolerance</li>
              <li>Automated multi-point inspection reporting</li>
            </ul>
          </div>
          <div class="card-spec">Accuracy: Critical dimension & parting line verification</div>
        </div>
      </div>

      <div class="showcase-card">
        <div class="card-img-wrap">
          <img src="{QC_LOAD_URI}" alt="Load Curve Tester">
          <div class="card-badge">Tactile Testing</div>
        </div>
        <div class="card-content">
          <div>
            <div class="card-title">AIKOH Dynamic Load Tester</div>
            <ul class="card-bullets">
              <li>Actuation force vs displacement curve capture</li>
              <li>Peak load, return force, and click ratio</li>
              <li>Automated cycle life & rebound fatigue testing</li>
              <li>Certified SPC reports per production lot</li>
            </ul>
          </div>
          <div class="card-spec">Function: HMI key switches & spring dampers</div>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <div class="footer-left">
        <div class="footer-item"><div class="footer-dot"></div> Post-cure convection ovens for volatile removal</div>
        <div class="footer-item"><div class="footer-dot"></div> Taber surface abrasion & alcohol rub testing</div>
      </div>
      <div class="footer-right">04 / 05</div>
    </div>
  </div>
</div>

<!-- SLIDE 5: WORKFLOW & RFQ -->
<div class="slide" id="slide-5">
  <div class="slide-content">
    <div class="slide-header">
      <div class="slide-title-block">
        <div class="slide-category">Engineering Engagement & RFQ Protocol</div>
        <h2 class="slide-title">Seamless Build-to-Print Execution</h2>
        <div class="slide-subtitle">From initial 3D CAD analysis to global freight forwarding with rapid communication</div>
      </div>
      <div class="brand-group">
        <img class="brand-logo" src="{LOGO_URI}" alt="Logo">
      </div>
    </div>

    <div class="closing-grid">
      <div class="workflow-list">
        <div class="workflow-step">
          <div class="step-num">01</div>
          <div class="step-info">
            <div class="step-title">CAD Review & DFM Feasibility</div>
            <div class="step-desc">Detailed check on draft angles, parting line placement, wall thicknesses, and undercut demolding strategy.</div>
          </div>
        </div>
        <div class="workflow-step">
          <div class="step-num">02</div>
          <div class="step-info">
            <div class="step-title">Material Formulation & Quotation</div>
            <div class="step-desc">Selecting exact durometer (Shore A), base polymer (Silicone, Viton, EPDM), color matching, and transparent tooling NRE.</div>
          </div>
        </div>
        <div class="workflow-step">
          <div class="step-num">03</div>
          <div class="step-info">
            <div class="step-title">Tooling Fabrication & T1 Sampling</div>
            <div class="step-desc">Precision CNC/EDM mold machining, first article inspection (FAI), and optical measurement report delivery.</div>
          </div>
        </div>
        <div class="workflow-step">
          <div class="step-num">04</div>
          <div class="step-info">
            <div class="step-title">Pilot Validation & Mass Production</div>
            <div class="step-desc">Customer fit check approval, high-vacuum vulcanization, secondary post-curing, and final 100% QA screening.</div>
          </div>
        </div>
        <div class="workflow-step">
          <div class="step-num">05</div>
          <div class="step-info">
            <div class="step-title">Global Export & Direct Delivery</div>
            <div class="step-desc">Air/Ocean shipping directly to North America, Europe, and Asia with complete customs and COC documentation.</div>
          </div>
        </div>
      </div>

      <div class="contact-box">
        <div class="contact-box-title">Start Your Project With Us</div>
        
        <div class="rfq-checklist">
          <div class="rfq-checklist-title">RFQ Drawing Submission Checklist</div>
          <ul>
            <li>2D drawing with key tolerances</li>
            <li>3D CAD model (STEP, IGES)</li>
            <li>Required Shore A durometer</li>
            <li>Operating temperature & fluids</li>
            <li>Color requirement (RAL / Pantone)</li>
            <li>Estimated annual order volume</li>
          </ul>
        </div>

        <div class="contact-details">
          <div class="contact-row">
            <span class="contact-label">Contact:</span>
            <div class="contact-val"><strong>Andy Hsu</strong> (Engineering & Sales)</div>
          </div>
          <div class="contact-row">
            <span class="contact-label">Email:</span>
            <div class="contact-val"><strong>andy_hsu@jun-hsiang.com.tw</strong></div>
          </div>
          <div class="contact-row">
            <span class="contact-label">Phone:</span>
            <div class="contact-val"><strong>+886-2-2203-9918</strong> (Mon–Fri 08:30–17:30 UTC+8)</div>
          </div>
          <div class="contact-row">
            <span class="contact-label">Address:</span>
            <div class="contact-val"><strong>No. 1 & 3, Ln. 345, Xinshu Rd., Xinzhuang Dist., New Taipei City 242, Taiwan</strong></div>
          </div>
          <div class="contact-row">
            <span class="contact-label">Website:</span>
            <div class="contact-val"><strong>https://www.jun-hsiang.com.tw/en/</strong></div>
          </div>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <div class="footer-left">
        <div class="footer-item"><div class="footer-dot"></div> Mutual NDA Protection Prior to Drawing Transfer</div>
        <div class="footer-item"><div class="footer-dot"></div> 24–48h Engineering Feasibility Feedback</div>
      </div>
      <div class="footer-right">05 / 05</div>
    </div>
  </div>
</div>

</body>
</html>
"""

def generate_pdf_via_chrome():
    print("[1/3] Generating 16:9 PDF via Google Chrome Headless...")
    html_temp = WORKSPACE / "scratch" / "presentation_deck.html"
    html_temp.write_text(HTML_TEMPLATE, encoding="utf-8")
    
    cmd = [
        CHROME_PATH,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={OUTPUT_PDF.resolve()}",
        str(html_temp.resolve().as_uri())
    ]
    subprocess.run(cmd, check=True)
    size_kb = OUTPUT_PDF.stat().st_size / 1024
    print(f"  - Successfully generated 16:9 PDF: {OUTPUT_PDF.name} ({size_kb:.1f} KB)")

def generate_slide_previews():
    print("[2/3] Generating slide PNG screenshots for visual inspection...")
    for i in range(1, 6):
        slide_pattern = f'<div class="slide" id="slide-{i}">'
        parts = HTML_TEMPLATE.split(slide_pattern)
        if len(parts) > 1:
            slide_content = slide_pattern + parts[1].split('<!-- SLIDE')[0].split('</body>')[0]
            single_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
{HTML_TEMPLATE.split('<style>')[1].split('</style>')[0]}
body {{ overflow: hidden; }}
.slide {{ page-break-after: auto; }}
</style>
</head>
<body>
{slide_content}
</body>
</html>"""
            slide_file = WORKSPACE / "scratch" / f"single_slide_{i}.html"
            slide_file.write_text(single_html, encoding="utf-8")
            
            preview_png = PREVIEWS_DIR / f"slide-{i}.png"
            cmd = [
                CHROME_PATH,
                "--headless",
                "--disable-gpu",
                "--window-size=1920,1080",
                "--hide-scrollbars",
                f"--screenshot={preview_png.resolve()}",
                str(slide_file.resolve().as_uri())
            ]
            subprocess.run(cmd, check=True)
            print(f"  - Generated preview: {preview_png.name}")

def generate_native_pptx():
    print("[3/3] Generating native editable 16:9 PowerPoint (.pptx)...")
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    BG_COLOR = RGBColor(6, 11, 26)
    CARD_BG = RGBColor(17, 28, 56)
    CARD_BORDER = RGBColor(40, 60, 100)
    TEXT_WHITE = RGBColor(255, 255, 255)
    TEXT_MUTED = RGBColor(148, 163, 184)
    TEXT_CYAN = RGBColor(56, 189, 248)
    TEXT_GOLD = RGBColor(245, 158, 11)
    
    def set_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()
        return bg

    def add_header(slide, cat_text, title_text, sub_text=""):
        cat_box = slide.shapes.add_textbox(Inches(0.9), Inches(0.45), Inches(5), Inches(0.35))
        tf = cat_box.text_frame
        p = tf.paragraphs[0]
        p.text = cat_text.upper()
        p.font.name = "Arial"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_CYAN
        
        t_box = slide.shapes.add_textbox(Inches(0.9), Inches(0.8), Inches(10), Inches(0.6))
        tf = t_box.text_frame
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Arial"
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        
        if sub_text:
            s_box = slide.shapes.add_textbox(Inches(0.9), Inches(1.4), Inches(11.5), Inches(0.4))
            tf = s_box.text_frame
            p = tf.paragraphs[0]
            p.text = sub_text
            p.font.name = "Arial"
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_MUTED

    def add_footer(slide, current, total="05"):
        box = slide.shapes.add_textbox(Inches(0.9), Inches(6.9), Inches(11.533), Inches(0.35))
        tf = box.text_frame
        p = tf.paragraphs[0]
        p.text = f"Jun-Hsiang Enterprise Co., Ltd. • ISO 9001:2015 Registered • Made in Taiwan                      {current} / {total}"
        p.font.name = "Arial"
        p.font.size = Pt(9.5)
        p.font.color.rgb = RGBColor(100, 116, 139)

    # SLIDE 1: COVER
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)
    if LOGO_FILE.exists():
        s1.shapes.add_picture(str(LOGO_FILE), Inches(0.9), Inches(0.65), width=Inches(0.6))
    t1 = s1.shapes.add_textbox(Inches(1.6), Inches(0.65), Inches(8), Inches(0.45))
    p = t1.text_frame.paragraphs[0]
    p.text = "JUN-HSIANG ENTERPRISE CO., LTD."
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE

    # Left text block
    t2 = s1.shapes.add_textbox(Inches(0.9), Inches(1.9), Inches(6.8), Inches(3.2))
    tf2 = t2.text_frame
    tf2.word_wrap = True
    p0 = tf2.paragraphs[0]
    p0.text = "TAIWAN PRECISION SILICONE & RUBBER ENGINEERING"
    p0.font.name = "Arial"
    p0.font.size = Pt(10.5)
    p0.font.bold = True
    p0.font.color.rgb = TEXT_GOLD
    p1 = tf2.add_paragraph()
    p1.text = "Custom Silicone & Rubber\nManufacturing Capabilities"
    p1.font.name = "Arial"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p2 = tf2.add_paragraph()
    p2.text = "\nLiquid Silicone (LSR) Injection • Vacuum Compression Molding • Overmolding\nProviding global OEM/ODM engineering co-development, rapid DFM analysis, and resilient non-China supply chain delivery."
    p2.font.name = "Arial"
    p2.font.size = Pt(12)
    p2.font.color.rgb = TEXT_MUTED

    # Left badges
    badges = [
        ("📍 Origin: Made in Taiwan", "⚡ Speed: 24-48h DFM"),
        ("🛡️ ISO 9001:2015 Registered", "🌐 Export: USA, EU, Japan")
    ]
    for r, row in enumerate(badges):
        for c, text in enumerate(row):
            bx = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9 + c*3.3), Inches(5.4 + r*0.65), Inches(3.2), Inches(0.55))
            bx.fill.solid()
            bx.fill.fore_color.rgb = CARD_BG
            bx.line.color.rgb = CARD_BORDER
            tf = bx.text_frame
            p = tf.paragraphs[0]
            p.text = text
            p.font.name = "Arial"
            p.font.size = Pt(10)
            p.font.color.rgb = TEXT_WHITE

    # Right mosaic images
    mosaic_imgs = [
        ("prod-keypads.jpg", Inches(8.1), Inches(1.9)),
        ("equip-lsr.jpg", Inches(10.65), Inches(1.9)),
        ("prod-orings.jpg", Inches(8.1), Inches(4.3)),
        ("qc-25d-optical.jpg", Inches(10.65), Inches(4.3))
    ]
    for img_name, mx, my in mosaic_imgs:
        img_p = IMAGES_DIR / img_name
        if img_p.exists():
            s1.shapes.add_picture(str(img_p), mx, my, width=Inches(2.4), height=Inches(2.2))

    add_footer(s1, "01")

    # SLIDE 2: HERITAGE
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_header(s2, "Company Heritage & Standards", "Built on 35+ Years of Mold Engineering Discipline", "Operating under the F.H.P.Q. quality philosophy with transparent DFM and zero customer conflict")
    stats = [
        ("1991", "Founded in Taiwan", "Over 3 decades of elastomeric tooling experience"),
        ("NT$ 12M", "Paid-in Capital", "Solid balance sheet with ongoing machine investments"),
        ("100%", "Non-China Supply", "Zero tariff exposure, resilient export routing")
    ]
    for i, (num, lbl, desc) in enumerate(stats):
        box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(1.95 + i*1.55), Inches(3.5), Inches(1.35))
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = CARD_BORDER
        tf = box.text_frame
        p = tf.paragraphs[0]
        p.text = num
        p.font.name = "Arial"
        p.font.size = Pt(26)
        p.font.bold = True
        p.font.color.rgb = TEXT_CYAN
        p2 = tf.add_paragraph()
        p2.text = lbl
        p2.font.name = "Arial"
        p2.font.size = Pt(11.5)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE
        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.name = "Arial"
        p3.font.size = Pt(9)
        p3.font.color.rgb = TEXT_MUTED

    pillars = [
        ("🤝 Friend", "Collaborative engineering problem-solvers. We partner from draft angle design to parting lines."),
        ("🛡️ Honesty", "100% customer tooling ownership protection. Transparent SGS, FDA, RoHS material certifications."),
        ("⚙️ Profession", "In-house mold design, custom rubber compounding, precision liquid injection, and secondary post-curing."),
        ("🏆 Quality", "\"Do not accept, do not produce, do not release defects.\" Full optical dimensional checks and QA sign-off.")
    ]
    for i, (title, desc) in enumerate(pillars):
        box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.7), Inches(1.95 + i*1.15), Inches(7.7), Inches(0.98))
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = CARD_BORDER
        tf = box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_GOLD
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = "Arial"
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_WHITE
    add_footer(s2, "02")

    # SLIDE 3: PRODUCTS
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_header(s3, "Product Lines & Applications", "Precision Silicone & Rubber Components", "Engineered for mission-critical industrial, medical, automotive, and electronic applications")
    products = [
        ("prod-keypads.jpg", "Conductive Keypads", "• Conductive carbon pills\n• Multi-color silk screen\n• Wear-resistant PU/Epoxy\n• Tactile actuation curve", "App: Remotes, POS, medical"),
        ("prod-orings.jpg", "Custom O-Rings & Seals", "• Silicone, Viton, EPDM, NBR\n• AS568 & JIS standards\n• -50°C to +250°C stability\n• Low compression set", "App: Automotive, valves, pumps"),
        ("prod-gaskets.jpg", "Precision Gaskets", "• Complex 3D rib profiles\n• IP67 / IP68 waterproof\n• Self-retaining press-in\n• EMI conductive options", "App: Outdoor cases, drones"),
        ("prod-medical-kb.jpg", "Medical Keyboards", "• 100% Watertight surface\n• Resists chemical washdown\n• FDA / LFGB compliant\n• Silent clinical feedback", "App: Hospitals, cleanrooms")
    ]
    for i, (img_name, title, bullets, spec) in enumerate(products):
        x = Inches(0.9 + i*2.92)
        box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.95), Inches(2.75), Inches(4.7))
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = CARD_BORDER
        img_file = IMAGES_DIR / img_name
        if img_file.exists():
            s3.shapes.add_picture(str(img_file), x + Inches(0.1), Inches(2.05), width=Inches(2.55), height=Inches(1.85))
        tb = s3.shapes.add_textbox(x + Inches(0.1), Inches(4.0), Inches(2.55), Inches(2.5))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p2 = tf.add_paragraph()
        p2.text = bullets
        p2.font.name = "Arial"
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MUTED
        p3 = tf.add_paragraph()
        p3.text = "\n" + spec
        p3.font.name = "Arial"
        p3.font.size = Pt(8.5)
        p3.font.color.rgb = TEXT_CYAN
    add_footer(s3, "03")

    # SLIDE 4: MACHINERY & QC
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_header(s4, "Manufacturing Fleet & Metrology Lab", "In-House Machinery & Quality Verification", "Advanced liquid injection, vacuum compression, and certified optical measurement systems")
    machines = [
        ("equip-lsr.jpg", "Vertical LSR Injection", "• Chuan-Lien MIV 1500-LS\n• Dynamic A/B component mixing\n• Flash-free runner technology\n• Multi-cavity micro molding", "System: Liquid silicone dosing"),
        ("equip-vacuum-press.jpg", "Vacuum Compression", "• High-tonnage hydraulic platens\n• Vacuum chamber air evacuation\n• Prevents knit-lines & voids\n• Uniform temperature control", "Fleet: High-density keypads"),
        ("qc-25d-optical.jpg", "HO STAR 2.5D Optical", "• Non-contact edge detection\n• Zero elastomeric deformation\n• Profile tolerance inspection\n• Automated FAI reporting", "Accuracy: Parting line QA"),
        ("qc-load-curve.jpg", "AIKOH Dynamic Load Tester", "• Force vs stroke displacement\n• Peak load & snap click ratio\n• Cycle life & rebound fatigue\n• Certified lot SPC reports", "Function: Keypad switch testing")
    ]
    for i, (img_name, title, bullets, spec) in enumerate(machines):
        x = Inches(0.9 + i*2.92)
        box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.95), Inches(2.75), Inches(4.7))
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = CARD_BORDER
        img_file = IMAGES_DIR / img_name
        if img_file.exists():
            s4.shapes.add_picture(str(img_file), x + Inches(0.1), Inches(2.05), width=Inches(2.55), height=Inches(1.85))
        tb = s4.shapes.add_textbox(x + Inches(0.1), Inches(4.0), Inches(2.55), Inches(2.5))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p2 = tf.add_paragraph()
        p2.text = bullets
        p2.font.name = "Arial"
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MUTED
        p3 = tf.add_paragraph()
        p3.text = "\n" + spec
        p3.font.name = "Arial"
        p3.font.size = Pt(8.5)
        p3.font.color.rgb = TEXT_CYAN
    add_footer(s4, "04")

    # SLIDE 5: WORKFLOW & CONTACT
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_header(s5, "Engineering Engagement & RFQ Protocol", "Seamless Build-to-Print Execution", "From initial 3D CAD analysis to global freight forwarding with rapid communication")
    steps = [
        ("01", "CAD Review & DFM Feasibility", "Draft angles, parting lines, wall thickness, undercut strategy"),
        ("02", "Material Formulation & Quote", "Shore A selection, polymer compound, transparent tooling NRE"),
        ("03", "Tooling & T1 Sampling", "Precision CNC mold machining, FAI inspection, optical report"),
        ("04", "Validation & Mass Production", "Customer sign-off, vacuum vulcanization, post-cure, 100% QA"),
        ("05", "Global Direct Export", "Air/Ocean shipping to USA, EU, Japan with complete COC docs")
    ]
    for i, (num, title, desc) in enumerate(steps):
        box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(1.95 + i*0.93), Inches(5.6), Inches(0.82))
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = CARD_BORDER
        tf = box.text_frame
        p = tf.paragraphs[0]
        p.text = f"{num}  {title}"
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_CYAN
        p2 = tf.add_paragraph()
        p2.text = f"     {desc}"
        p2.font.name = "Arial"
        p2.font.size = Pt(9)
        p2.font.color.rgb = TEXT_MUTED

    c_box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.95), Inches(5.6), Inches(4.65))
    c_box.fill.solid()
    c_box.fill.fore_color.rgb = RGBColor(15, 23, 42)
    c_box.line.color.rgb = TEXT_CYAN
    tf = c_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Start Your Project With Us"
    p.font.name = "Arial"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p_chk = tf.add_paragraph()
    p_chk.text = "\nRFQ DRAWING SUBMISSION CHECKLIST:\n• 2D drawing with tolerances & 3D CAD model (STEP/IGES)\n• Shore A hardness, operating temperature & environment\n• Color matching (Pantone/RAL) & target annual volume"
    p_chk.font.name = "Arial"
    p_chk.font.size = Pt(9.5)
    p_chk.font.color.rgb = TEXT_GOLD
    p_con = tf.add_paragraph()
    p_con.text = "\nDIRECT CONTACT:\nContact: Andy Hsu (Engineering & Sales)\nEmail: andy_hsu@jun-hsiang.com.tw\nPhone: +886-2-2203-9918 (Mon-Fri 08:30-17:30 UTC+8)\nAddress: No. 1 & 3, Ln. 345, Xinshu Rd., Xinzhuang Dist., New Taipei City 242, Taiwan\nWebsite: https://www.jun-hsiang.com.tw/en/"
    p_con.font.name = "Arial"
    p_con.font.size = Pt(9.5)
    p_con.font.color.rgb = TEXT_WHITE
    add_footer(s5, "05")

    prs.save(str(OUTPUT_PPTX))
    size_kb = OUTPUT_PPTX.stat().st_size / 1024
    print(f"  - Successfully saved native 16:9 PPTX: {OUTPUT_PPTX.name} ({size_kb:.1f} KB)")

def main():
    generate_pdf_via_chrome()
    generate_slide_previews()
    generate_native_pptx()
    print("ALL DONE!")

if __name__ == "__main__":
    main()
