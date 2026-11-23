"""
Build Swiss Industrial Precision 16:9 Executive Presentation & PDF for Jun-Hsiang Enterprise
Design Philosophy:
- "Swiss Industrial Precision" (inspired by Trelleborg, Shin-Etsu, Keyence, Misumi corporate catalogs)
- Sandwich architecture: Deep Graphite (#0E131B) Cover & Closing; Pure Gallery White (#FFFFFF) & Warm Paper (#F6F6F3) Content Slides
- White-background authentic factory & product photos blend seamlessly on white studio canvases (object-fit: contain, zero awkward black-box sticker look, zero cropping/distortion)
- ZERO emojis, ZERO glowing neon AI slop, ZERO repetitive templates (every slide has a distinct editorial layout)
- Exact 1920x1080 pixel-to-pixel rendering (no black border scaling bug)
- Strict compliance with AGENTS.md Rules 5, 8, 15 (no unverified tolerances, no "automated/automatic" wording)
Outputs:
  1. pdf/en/Jun-Hsiang-Enterprise-Company-Profile-EN.pdf (7-slide 16:9 widescreen vector PDF)
  2. pdf/en/Jun-Hsiang-Enterprise-Company-Profile-EN.pptx (7-slide native editable 16:9 PowerPoint)
  3. scratch/presentation_previews/slide-1.png .. slide-7.png (1920x1080 full-bleed previews)
"""

import base64
import subprocess
from pathlib import Path
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

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


COMMON_CSS = """
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  @page {
    size: 1920px 1080px;
    margin: 0;
  }

  html, body {
    width: 1920px;
    background: #FFFFFF;
    font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif;
    color: #111827;
    -webkit-font-smoothing: antialiased;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  .slide {
    width: 1920px;
    height: 1080px;
    position: relative;
    overflow: hidden;
    page-break-after: always;
    background: #FFFFFF;
  }

  .slide:last-child {
    page-break-after: auto;
  }

  /* Editorial Typography */
  .kicker {
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 3.2px;
    text-transform: uppercase;
    color: #A67C2E;
  }

  .display-title {
    font-family: Georgia, "Times New Roman", serif;
    font-weight: 400;
    letter-spacing: -0.5px;
    line-height: 1.12;
  }

  .section-h2 {
    font-size: 46px;
    font-weight: 700;
    letter-spacing: -0.8px;
    line-height: 1.14;
    color: #0E131B;
  }

  .section-lead {
    font-size: 20px;
    font-weight: 400;
    line-height: 1.5;
    color: #525B6B;
  }

  /* Shared Light Slide Chrome */
  .light-slide {
    background: #FFFFFF;
    padding: 64px 96px 56px 96px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .warm-slide {
    background: #F6F6F3;
    padding: 64px 96px 56px 96px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .top-bar {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    padding-bottom: 24px;
    border-bottom: 1px solid #E2E5EA;
  }

  .top-bar-left {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .top-bar-brand {
    display: flex;
    align-items: center;
    gap: 14px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2.2px;
    text-transform: uppercase;
    color: #64748B;
  }

  .top-bar-brand img {
    height: 30px;
    width: auto;
  }

  .bottom-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 20px;
    border-top: 1px solid #E2E5EA;
    font-size: 14px;
    color: #6B7280;
    letter-spacing: 0.3px;
  }

  .page-num {
    font-variant-numeric: tabular-nums;
    font-weight: 700;
    color: #0E131B;
    letter-spacing: 2px;
  }

  /* ================= SLIDE 1: ARCHITECTURAL SPLIT COVER ================= */
  .cover-slide {
    display: grid;
    grid-template-columns: 1120px 800px;
    width: 1920px;
    height: 1080px;
  }

  .cover-left {
    background: #0E131B;
    color: #FFFFFF;
    padding: 72px 96px 64px 96px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
  }

  .cover-brand {
    display: flex;
    align-items: center;
    gap: 18px;
  }

  .cover-brand img {
    height: 46px;
    width: auto;
  }

  .cover-brand-text {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .cover-brand-name {
    font-size: 18px;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #FFFFFF;
  }

  .cover-brand-sub {
    font-size: 12px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #9CA3AF;
  }

  .cover-main {
    display: flex;
    flex-direction: column;
    gap: 28px;
    margin: auto 0;
  }

  .cover-kicker {
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 3.5px;
    text-transform: uppercase;
    color: #D4AA55;
  }

  .cover-h1 {
    font-size: 72px;
    font-weight: 700;
    line-height: 1.06;
    letter-spacing: -1.8px;
    color: #FFFFFF;
  }

  .cover-h1 em {
    font-family: Georgia, "Times New Roman", serif;
    font-style: italic;
    font-weight: 400;
    color: #E5C178;
  }

  .cover-desc {
    font-size: 21px;
    font-weight: 300;
    line-height: 1.6;
    color: #CBD5E1;
    max-width: 820px;
  }

  .cover-meta-strip {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 32px;
    padding-top: 32px;
    border-top: 1px solid rgba(255, 255, 255, 0.14);
  }

  .cover-meta-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2.2px;
    text-transform: uppercase;
    color: #9CA3AF;
    margin-bottom: 6px;
  }

  .cover-meta-val {
    font-size: 17px;
    font-weight: 600;
    color: #FFFFFF;
  }

  .cover-right {
    background: #F6F6F3;
    padding: 56px 64px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .cover-gallery-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2.4px;
    text-transform: uppercase;
    color: #6B7280;
    padding-bottom: 18px;
    border-bottom: 1px solid #DCDFE4;
  }

  .cover-figure {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    padding: 24px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .cover-figure-lg {
    height: 440px;
  }

  .cover-figure-sm {
    height: 360px;
  }

  .cover-figure img {
    width: 100%;
    height: calc(100% - 34px);
    object-fit: contain;
    mix-blend-mode: multiply;
  }

  .fig-caption {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 12px;
    border-top: 1px solid #F0F1F4;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    color: #4B5563;
  }

  .fig-caption span {
    color: #A67C2E;
  }

  /* ================= SLIDE 2: HERITAGE & F.H.P.Q. ================= */
  .s2-body {
    display: grid;
    grid-template-columns: 540px 1fr;
    gap: 72px;
    flex: 1;
    padding: 44px 0 28px 0;
    align-items: stretch;
  }

  .facts-panel {
    background: #F6F6F3;
    padding: 40px 44px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .big-stat-row {
    display: flex;
    align-items: baseline;
    gap: 16px;
    padding-bottom: 28px;
    border-bottom: 1px solid #DCDFE4;
  }

  .big-stat-num {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 84px;
    font-weight: 400;
    line-height: 0.95;
    color: #0E131B;
  }

  .big-stat-text {
    font-size: 18px;
    font-weight: 600;
    line-height: 1.35;
    color: #374151;
  }

  .fact-table {
    display: flex;
    flex-direction: column;
  }

  .fact-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    padding: 16px 0;
    border-bottom: 1px solid #E2E5EA;
    gap: 20px;
  }

  .fact-row:last-child {
    border-bottom: none;
  }

  .fact-key {
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #6B7280;
    white-space: nowrap;
  }

  .fact-val {
    font-size: 16px;
    font-weight: 600;
    color: #111827;
    text-align: right;
  }

  .fhpq-panel {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .fhpq-intro {
    font-size: 24px;
    font-weight: 400;
    line-height: 1.5;
    color: #1F2937;
    padding-bottom: 28px;
    border-bottom: 1px solid #E2E5EA;
  }

  .fhpq-intro strong {
    color: #0E131B;
    font-weight: 700;
  }

  .fhpq-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 36px 48px;
    padding-top: 32px;
    flex: 1;
  }

  .fhpq-item {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .fhpq-num {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 28px;
    color: #A67C2E;
    line-height: 1;
  }

  .fhpq-title {
    font-size: 22px;
    font-weight: 700;
    color: #0E131B;
    letter-spacing: -0.2px;
  }

  .fhpq-desc {
    font-size: 16px;
    line-height: 1.6;
    color: #4B5563;
  }

  /* ================= SLIDE 3: PROCESSES & MATERIALS ================= */
  .s3-body {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    flex: 1;
    padding: 36px 0 24px 0;
    gap: 32px;
  }

  .process-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 32px;
    flex: 1;
  }

  .process-col {
    background: #FFFFFF;
    border: 1px solid #E2E5EA;
    padding: 38px 36px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .process-col-featured {
    background: #0E131B;
    border: 1px solid #0E131B;
    color: #FFFFFF;
  }

  .proc-index {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 40px;
    color: #A67C2E;
    line-height: 1;
    margin-bottom: 18px;
  }

  .process-col-featured .proc-index {
    color: #D4AA55;
  }

  .proc-title {
    font-size: 26px;
    font-weight: 700;
    line-height: 1.25;
    margin-bottom: 14px;
    color: #0E131B;
  }

  .process-col-featured .proc-title {
    color: #FFFFFF;
  }

  .proc-summary {
    font-size: 16px;
    line-height: 1.6;
    color: #4B5563;
    margin-bottom: 24px;
  }

  .process-col-featured .proc-summary {
    color: #CBD5E1;
  }

  .proc-list {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 11px;
    padding-top: 20px;
    border-top: 1px solid #E5E7EB;
    font-size: 15px;
    color: #374151;
  }

  .process-col-featured .proc-list {
    border-top-color: rgba(255, 255, 255, 0.14);
    color: #E2E8F0;
  }

  .proc-list li {
    padding-left: 18px;
    position: relative;
  }

  .proc-list li::before {
    content: "";
    position: absolute;
    left: 0;
    top: 9px;
    width: 6px;
    height: 1.5px;
    background: #A67C2E;
  }

  .process-col-featured .proc-list li::before {
    background: #D4AA55;
  }

  .material-strip {
    background: #FFFFFF;
    border: 1px solid #E2E5EA;
    padding: 24px 36px;
    display: grid;
    grid-template-columns: 240px repeat(6, 1fr);
    align-items: center;
    gap: 20px;
  }

  .mat-label {
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #0E131B;
    border-right: 1px solid #E2E5EA;
    padding-right: 20px;
  }

  .mat-item {
    display: flex;
    flex-direction: column;
    gap: 3px;
  }

  .mat-code {
    font-size: 17px;
    font-weight: 700;
    color: #0E131B;
  }

  .mat-desc {
    font-size: 13px;
    color: #6B7280;
  }

  /* ================= SLIDE 4: PRODUCT PORTFOLIO (ASYMMETRIC EDITORIAL) ================= */
  .s4-body {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 36px;
    flex: 1;
    padding: 34px 0 24px 0;
  }

  .prod-col {
    display: flex;
    flex-direction: column;
    gap: 28px;
  }

  .prod-card-horiz {
    background: #F6F6F3;
    border: 1px solid #E5E7EB;
    display: grid;
    grid-template-columns: 340px 1fr;
    flex: 1;
    overflow: hidden;
  }

  .prod-photo-stage {
    background: #FFFFFF;
    padding: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-right: 1px solid #E5E7EB;
  }

  .prod-photo-stage img {
    max-width: 100%;
    max-height: 300px;
    object-fit: contain;
    mix-blend-mode: multiply;
  }

  .prod-info {
    padding: 28px 32px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .prod-tag {
    font-size: 11.5px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #A67C2E;
    margin-bottom: 8px;
  }

  .prod-title {
    font-size: 24px;
    font-weight: 700;
    color: #0E131B;
    line-height: 1.25;
    margin-bottom: 14px;
  }

  .prod-bullets {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 8px;
    font-size: 15px;
    line-height: 1.45;
    color: #4B5563;
  }

  .prod-bullets li {
    padding-left: 16px;
    position: relative;
  }

  .prod-bullets li::before {
    content: "";
    position: absolute;
    left: 0;
    top: 9px;
    width: 6px;
    height: 1.5px;
    background: #A67C2E;
  }

  .prod-app {
    font-size: 13px;
    font-weight: 600;
    color: #374151;
    padding-top: 14px;
    border-top: 1px solid #E2E5EA;
  }

  /* ================= SLIDE 5: IN-HOUSE EQUIPMENT (2-UP STUDIO FEATURE) ================= */
  .s5-body {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    flex: 1;
    padding: 34px 0 22px 0;
    gap: 28px;
  }

  .equip-grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 40px;
    flex: 1;
  }

  .equip-feature {
    background: #FFFFFF;
    border: 1px solid #E2E5EA;
    display: grid;
    grid-template-columns: 380px 1fr;
    overflow: hidden;
  }

  .equip-img-stage {
    background: #FFFFFF;
    padding: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-right: 1px solid #ECEEF2;
  }

  .equip-img-stage img {
    max-width: 100%;
    max-height: 470px;
    object-fit: contain;
  }

  .equip-detail {
    padding: 36px 36px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .equip-title {
    font-size: 28px;
    font-weight: 700;
    color: #0E131B;
    line-height: 1.2;
    margin: 10px 0 16px 0;
  }

  .equip-desc {
    font-size: 16px;
    line-height: 1.6;
    color: #4B5563;
    margin-bottom: 20px;
  }

  .secondary-strip {
    background: #0E131B;
    color: #FFFFFF;
    padding: 22px 36px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .sec-strip-title {
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2.2px;
    text-transform: uppercase;
    color: #D4AA55;
  }

  .sec-strip-items {
    display: flex;
    gap: 36px;
    font-size: 15px;
    font-weight: 500;
    color: #E5E7EB;
  }

  /* ================= SLIDE 6: METROLOGY & QA LAB ================= */
  .s6-body {
    display: grid;
    grid-template-columns: 1.15fr 0.85fr;
    gap: 48px;
    flex: 1;
    padding: 34px 0 24px 0;
  }

  .qa-photos-stack {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 28px;
  }

  .qa-card {
    background: #F6F6F3;
    border: 1px solid #E2E5EA;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .qa-img-box {
    background: #FFFFFF;
    height: 360px;
    padding: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-bottom: 1px solid #E2E5EA;
  }

  .qa-img-box img {
    max-width: 100%;
    max-height: 320px;
    object-fit: contain;
  }

  .qa-card-body {
    padding: 28px 30px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    flex: 1;
  }

  .qa-card-title {
    font-size: 22px;
    font-weight: 700;
    color: #0E131B;
  }

  .qa-card-text {
    font-size: 15px;
    line-height: 1.6;
    color: #4B5563;
  }

  .qa-protocol {
    background: #F6F6F3;
    padding: 38px 42px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .qa-proto-head {
    font-size: 24px;
    font-weight: 700;
    color: #0E131B;
    margin-top: 8px;
    padding-bottom: 20px;
    border-bottom: 1px solid #DCDFE4;
  }

  .qa-step-list {
    display: flex;
    flex-direction: column;
    gap: 18px;
    margin: auto 0;
  }

  .qa-step {
    display: grid;
    grid-template-columns: 44px 1fr;
    gap: 14px;
    align-items: start;
  }

  .qa-step-num {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 22px;
    color: #A67C2E;
    line-height: 1.2;
  }

  .qa-step-title {
    font-size: 16.5px;
    font-weight: 700;
    color: #0E131B;
    margin-bottom: 3px;
  }

  .qa-step-desc {
    font-size: 14.5px;
    line-height: 1.5;
    color: #4B5563;
  }

  .qa-iso-note {
    padding-top: 18px;
    border-top: 1px solid #DCDFE4;
    font-size: 13.5px;
    font-weight: 600;
    color: #374151;
  }

  /* ================= SLIDE 7: DARK ARCHITECTURAL CLOSING ================= */
  .dark-closing {
    background: #0E131B;
    color: #FFFFFF;
    padding: 68px 96px 56px 96px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .dark-top-bar {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    padding-bottom: 24px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.14);
  }

  .dark-h2 {
    font-size: 46px;
    font-weight: 700;
    letter-spacing: -0.8px;
    color: #FFFFFF;
    margin-top: 8px;
  }

  .timeline-5 {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 24px;
    padding: 40px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.14);
  }

  .tl-item {
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding-right: 16px;
    border-right: 1px solid rgba(255, 255, 255, 0.1);
  }

  .tl-item:last-child {
    border-right: none;
    padding-right: 0;
  }

  .tl-num {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 32px;
    color: #D4AA55;
    line-height: 1;
  }

  .tl-title {
    font-size: 19px;
    font-weight: 700;
    color: #FFFFFF;
    line-height: 1.3;
  }

  .tl-desc {
    font-size: 14.5px;
    line-height: 1.55;
    color: #9CA3AF;
  }

  .closing-lower {
    display: grid;
    grid-template-columns: 1fr 1.15fr;
    gap: 64px;
    padding: 36px 0 12px 0;
    align-items: start;
  }

  .rfq-panel {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.12);
    padding: 36px 40px;
  }

  .rfq-panel-title {
    font-size: 22px;
    font-weight: 700;
    color: #FFFFFF;
    margin: 8px 0 22px 0;
  }

  .rfq-list {
    list-style: none;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px 28px;
    font-size: 15.5px;
    color: #D1D5DB;
  }

  .rfq-list li {
    padding-left: 18px;
    position: relative;
  }

  .rfq-list li::before {
    content: "";
    position: absolute;
    left: 0;
    top: 10px;
    width: 7px;
    height: 1.5px;
    background: #D4AA55;
  }

  .contact-panel {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .contact-headline {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 34px;
    font-weight: 400;
    color: #FFFFFF;
    line-height: 1.25;
  }

  .contact-grid {
    display: grid;
    grid-template-columns: 140px 1fr;
    gap: 14px 24px;
    padding-top: 12px;
    font-size: 16.5px;
  }

  .c-key {
    font-size: 12.5px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #9CA3AF;
    padding-top: 3px;
  }

  .c-val {
    color: #FFFFFF;
    font-weight: 500;
  }

  .c-val-accent {
    color: #E5C178;
    font-weight: 700;
  }

  .dark-bottom-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.14);
    font-size: 14px;
    color: #9CA3AF;
  }
"""


SLIDES_HTML = [
    # SLIDE 1: COVER
    f"""
    <div class="slide cover-slide" id="slide-1">
      <div class="cover-left">
        <div class="cover-brand">
          <img src="{LOGO_URI}" alt="Jun-Hsiang Logo"/>
          <div class="cover-brand-text">
            <div class="cover-brand-name">Jun-Hsiang Enterprise Co., Ltd.</div>
            <div class="cover-brand-sub">Precision Elastomer Manufacturing &bull; Taiwan</div>
          </div>
        </div>

        <div class="cover-main">
          <div class="cover-kicker">Corporate Capability Profile</div>
          <h1 class="cover-h1">Custom Silicone &amp;<br/>Rubber <em>Engineering</em></h1>
          <p class="cover-desc">
            In-house Liquid Silicone Rubber (LSR) injection, high-vacuum compression molding,
            and silicone-to-metal/plastic overmolding. Built in Taiwan for OEM and ODM engineering teams across North America, Europe, and Japan.
          </p>
        </div>

        <div class="cover-meta-strip">
          <div>
            <div class="cover-meta-label">Established</div>
            <div class="cover-meta-val">September 1991 (35+ Yrs)</div>
          </div>
          <div>
            <div class="cover-meta-label">Quality System</div>
            <div class="cover-meta-val">ISO 9001:2015 Registered</div>
          </div>
          <div>
            <div class="cover-meta-label">Supply Chain</div>
            <div class="cover-meta-val">100% Made in Taiwan</div>
          </div>
        </div>
      </div>

      <div class="cover-right">
        <div class="cover-gallery-top">
          <span>Selected Manufacturing Highlights</span>
          <span>01 / 07</span>
        </div>

        <div class="cover-figure cover-figure-lg">
          <img src="{EQUIP_LSR_URI}" alt="Vertical LSR Injection Press"/>
          <div class="fig-caption">
            <span>FIG. 01</span>
            <div>Vertical LSR Injection &mdash; MIV 1500-LS</div>
          </div>
        </div>

        <div class="cover-figure cover-figure-sm">
          <img src="{PROD_ORINGS_URI}" alt="Custom Silicone O-Rings"/>
          <div class="fig-caption">
            <span>FIG. 02</span>
            <div>Custom O-Rings &amp; Precision Seals</div>
          </div>
        </div>
      </div>
    </div>
    """,

    # SLIDE 2: COMPANY OVERVIEW & F.H.P.Q.
    f"""
    <div class="slide light-slide" id="slide-2">
      <div class="top-bar">
        <div class="top-bar-left">
          <div class="kicker">01 &mdash; Company Overview &amp; Heritage</div>
          <h2 class="section-h2">35 Years of Precision Elastomer Tooling in Taiwan</h2>
        </div>
        <div class="top-bar-brand">
          <img src="{LOGO_URI}" alt="Logo"/>
          <span>Jun-Hsiang Enterprise</span>
        </div>
      </div>

      <div class="s2-body">
        <div class="facts-panel">
          <div class="big-stat-row">
            <div class="big-stat-num">1991</div>
            <div class="big-stat-text">Founded in New Taipei City,<br/>Taiwan</div>
          </div>

          <div class="fact-table">
            <div class="fact-row">
              <span class="fact-key">Company</span>
              <span class="fact-val">Jun-Hsiang Enterprise Co., Ltd.</span>
            </div>
            <div class="fact-row">
              <span class="fact-key">Paid-in Capital</span>
              <span class="fact-val">NTD 12,000,000</span>
            </div>
            <div class="fact-row">
              <span class="fact-key">Manufacturing Base</span>
              <span class="fact-val">Xinzhuang Dist., New Taipei City</span>
            </div>
            <div class="fact-row">
              <span class="fact-key">Quality Standard</span>
              <span class="fact-val">ISO 9001:2015 Registered</span>
            </div>
            <div class="fact-row">
              <span class="fact-key">Export Regions</span>
              <span class="fact-val">USA, Europe, Japan &amp; Global OEMs</span>
            </div>
            <div class="fact-row">
              <span class="fact-key">Supply Advantage</span>
              <span class="fact-val">Non-China Resilient Manufacturing</span>
            </div>
          </div>
        </div>

        <div class="fhpq-panel">
          <div class="fhpq-intro">
            Guided by our <strong>F.H.P.Q. operational discipline</strong>, we support global hardware teams from initial DFM review and mold steel fabrication through validated mass production.
          </div>

          <div class="fhpq-grid">
            <div class="fhpq-item">
              <div class="fhpq-num">01</div>
              <div class="fhpq-title">Friend &mdash; Engineering Partnership</div>
              <div class="fhpq-desc">Collaborative DFM feedback on parting lines, draft angles, undercut demolding, and material selection before tooling begins.</div>
            </div>
            <div class="fhpq-item">
              <div class="fhpq-num">02</div>
              <div class="fhpq-title">Honesty &mdash; Protected Tooling &amp; Specs</div>
              <div class="fhpq-desc">Strict customer tooling ownership protection, NDA confidentiality, and transparent raw material compliance documentation.</div>
            </div>
            <div class="fhpq-item">
              <div class="fhpq-num">03</div>
              <div class="fhpq-title">Profession &mdash; Vertical Integration</div>
              <div class="fhpq-desc">In-house compounding, LSR injection, vacuum compression, screen printing, and secondary post-cure baking (with vetted partners for laser etching &amp; spray coating).</div>
            </div>
            <div class="fhpq-item">
              <div class="fhpq-num">04</div>
              <div class="fhpq-title">Quality &mdash; Zero-Defect Standard</div>
              <div class="fhpq-desc">Built on the rule: do not accept, do not produce, and do not release defective parts. Backed by 2.5D optical and load testing.</div>
            </div>
          </div>
        </div>
      </div>

      <div class="bottom-bar">
        <span>Jun-Hsiang Enterprise Co., Ltd. &bull; Custom Silicone &amp; Rubber OEM Manufacturer</span>
        <span class="page-num">02 / 07</span>
      </div>
    </div>
    """,

    # SLIDE 3: CORE PROCESSES & MATERIALS
    f"""
    <div class="slide warm-slide" id="slide-3">
      <div class="top-bar">
        <div class="top-bar-left">
          <div class="kicker">02 &mdash; Manufacturing Capabilities</div>
          <h2 class="section-h2">Three Core Molding Processes &amp; Material Matrix</h2>
        </div>
        <div class="top-bar-brand">
          <img src="{LOGO_URI}" alt="Logo"/>
          <span>Jun-Hsiang Enterprise</span>
        </div>
      </div>

      <div class="s3-body">
        <div class="process-grid">
          <div class="process-col process-col-featured">
            <div>
              <div class="proc-index">01</div>
              <div class="proc-title">LSR Liquid Silicone Injection</div>
              <div class="proc-summary">Closed-loop metered A/B liquid silicone injection for complex geometries, tight parting lines, and cleanroom-grade consistency.</div>
            </div>
            <ul class="proc-list">
              <li>Vertical LSR press architecture (MIV 1500-LS)</li>
              <li>Flash-minimized cold-runner tooling options</li>
              <li>Ideal for medical masks, valves, and optical seals</li>
              <li>Consistent batch-to-batch curing repeatability</li>
            </ul>
          </div>

          <div class="process-col">
            <div>
              <div class="proc-index">02</div>
              <div class="proc-title">Vacuum Compression Molding</div>
              <div class="proc-summary">High-tonnage hydraulic molding with integrated vacuum evacuation for HCR solid silicone and specialty synthetic rubbers.</div>
            </div>
            <ul class="proc-list">
              <li>Vacuum chamber prevents trapped air and voids</li>
              <li>Cost-effective tooling for prototypes &amp; mid-volumes</li>
              <li>Supports conductive keypads, O-rings &amp; large gaskets</li>
              <li>Flexible Shore A 10 to 90 custom compounding</li>
            </ul>
          </div>

          <div class="process-col">
            <div>
              <div class="proc-index">03</div>
              <div class="proc-title">Overmolding &amp; Insert Bonding</div>
              <div class="proc-summary">Chemical and mechanical bonding of silicone or elastomer directly onto metal hardware and high-temperature engineering plastics.</div>
            </div>
            <ul class="proc-list">
              <li>Silicone-to-stainless steel, aluminum &amp; brass inserts</li>
              <li>Silicone-to-PC, PBT, PA &amp; PEEK substrates</li>
              <li>Controlled surface pretreatment &amp; primer application</li>
              <li>Eliminates manual assembly and leak paths</li>
            </ul>
          </div>
        </div>

        <div class="material-strip">
          <div class="mat-label">Elastomer<br/>Materials</div>
          <div class="mat-item">
            <div class="mat-code">LSR</div>
            <div class="mat-desc">Medical &amp; Optical</div>
          </div>
          <div class="mat-item">
            <div class="mat-code">VMQ</div>
            <div class="mat-desc">FDA / LFGB Silicone</div>
          </div>
          <div class="mat-item">
            <div class="mat-code">FKM</div>
            <div class="mat-desc">Viton Chemical Seal</div>
          </div>
          <div class="mat-item">
            <div class="mat-code">FVMQ</div>
            <div class="mat-desc">Fuel &amp; Oil Resistant</div>
          </div>
          <div class="mat-item">
            <div class="mat-code">EPDM</div>
            <div class="mat-desc">Weather &amp; Steam</div>
          </div>
          <div class="mat-item">
            <div class="mat-code">NBR / CR</div>
            <div class="mat-desc">Industrial Oil Seals</div>
          </div>
        </div>
      </div>

      <div class="bottom-bar">
        <span>RoHS 2.0, REACH, FDA 21 CFR 177.2600 &amp; LFGB compliant formulations available upon request</span>
        <span class="page-num">03 / 07</span>
      </div>
    </div>
    """,

    # SLIDE 4: PRODUCT PORTFOLIO
    f"""
    <div class="slide light-slide" id="slide-4">
      <div class="top-bar">
        <div class="top-bar-left">
          <div class="kicker">03 &mdash; Product Portfolio</div>
          <h2 class="section-h2">Custom Components Built to Print</h2>
        </div>
        <div class="top-bar-brand">
          <img src="{LOGO_URI}" alt="Logo"/>
          <span>Jun-Hsiang Enterprise</span>
        </div>
      </div>

      <div class="s4-body">
        <div class="prod-col">
          <div class="prod-card-horiz">
            <div class="prod-photo-stage">
              <img src="{PROD_KEYPADS_URI}" alt="Conductive Silicone Keypads"/>
            </div>
            <div class="prod-info">
              <div>
                <div class="prod-tag">HMI &amp; Tactile Interfaces</div>
                <div class="prod-title">Conductive Silicone Keypads</div>
                <ul class="prod-bullets">
                  <li>Conductive carbon pills &amp; gold-contact options</li>
                  <li>In-house multi-color silk-screen printing</li>
                  <li>Coordinated laser etching &amp; PU/matte spray coating via vetted partners</li>
                </ul>
              </div>
              <div class="prod-app">Applications: Industrial controllers, POS terminals, remotes</div>
            </div>
          </div>

          <div class="prod-card-horiz">
            <div class="prod-photo-stage">
              <img src="{PROD_MEDKB_URI}" alt="Medical Washable Keyboards"/>
            </div>
            <div class="prod-info">
              <div>
                <div class="prod-tag">Healthcare &amp; Cleanroom</div>
                <div class="prod-title">Medical Washable Keyboards</div>
                <ul class="prod-bullets">
                  <li>Seamless watertight skin blocks fluid &amp; dust ingress</li>
                  <li>Resistant to hospital-grade alcohol &amp; disinfectants</li>
                  <li>Biocompatible &amp; food-grade silicone compounds</li>
                </ul>
              </div>
              <div class="prod-app">Applications: Clinical carts, dental suites, cleanrooms</div>
            </div>
          </div>
        </div>

        <div class="prod-col">
          <div class="prod-card-horiz">
            <div class="prod-photo-stage">
              <img src="{PROD_ORINGS_URI}" alt="Custom O-Rings and Oil Seals"/>
            </div>
            <div class="prod-info">
              <div>
                <div class="prod-tag">Fluid &amp; Pressure Sealing</div>
                <div class="prod-title">Custom O-Rings &amp; Oil Seals</div>
                <ul class="prod-bullets">
                  <li>AS568, JIS B2401 &amp; custom non-standard cross-sections</li>
                  <li>Wide thermal stability from -50&deg;C to +250&deg;C (material-dependent)</li>
                  <li>Low compression set for long-term static &amp; dynamic seals</li>
                </ul>
              </div>
              <div class="prod-app">Applications: Automotive connectors, valves, fluid pumps</div>
            </div>
          </div>

          <div class="prod-card-horiz">
            <div class="prod-photo-stage">
              <img src="{PROD_GASKETS_URI}" alt="Precision Frame Gaskets"/>
            </div>
            <div class="prod-info">
              <div>
                <div class="prod-tag">Enclosure Protection</div>
                <div class="prod-title">Precision Frame Gaskets</div>
                <ul class="prod-bullets">
                  <li>Complex 3D perimeter profiles &amp; multi-rib waterproof lips</li>
                  <li>Engineered for waterproof &amp; dust-resistant enclosure sealing</li>
                  <li>Available in self-lubricating &amp; EMI-shielded grades</li>
                </ul>
              </div>
              <div class="prod-app">Applications: Outdoor telecom, UAV drones, sensor housings</div>
            </div>
          </div>
        </div>
      </div>

      <div class="bottom-bar">
        <span>All photographs represent authentic parts manufactured by Jun-Hsiang Enterprise in Taiwan</span>
        <span class="page-num">04 / 07</span>
      </div>
    </div>
    """,

    # SLIDE 5: IN-HOUSE PRODUCTION EQUIPMENT
    f"""
    <div class="slide warm-slide" id="slide-5">
      <div class="top-bar">
        <div class="top-bar-left">
          <div class="kicker">04 &mdash; Production Infrastructure</div>
          <h2 class="section-h2">In-House Molding Fleet &amp; Secondary Processing</h2>
        </div>
        <div class="top-bar-brand">
          <img src="{LOGO_URI}" alt="Logo"/>
          <span>Jun-Hsiang Enterprise</span>
        </div>
      </div>

      <div class="s5-body">
        <div class="equip-grid-2">
          <div class="equip-feature">
            <div class="equip-img-stage">
              <img src="{EQUIP_LSR_URI}" alt="Chuan-Lien MIV 1500-LS Vertical LSR Press"/>
            </div>
            <div class="equip-detail">
              <div>
                <div class="kicker">Liquid Injection System</div>
                <div class="equip-title">Vertical LSR Injection Press</div>
                <p class="equip-desc">Chuan-Lien MIV 1500-LS vertical clamping system engineered for insert loading and high-precision liquid silicone molding.</p>
              </div>
              <ul class="proc-list">
                <li>Closed A/B metered dosing &amp; static mixing</li>
                <li>Vertical platen ergonomics for metal/plastic inserts</li>
                <li>High-consistency cavity filling for micro-features</li>
              </ul>
            </div>
          </div>

          <div class="equip-feature">
            <div class="equip-img-stage">
              <img src="{EQUIP_VAC_URI}" alt="Vacuum Compression Molding Press"/>
            </div>
            <div class="equip-detail">
              <div>
                <div class="kicker">Solid Elastomer Fleet</div>
                <div class="equip-title">Vacuum Compression Presses</div>
                <p class="equip-desc">Heavy-duty hydraulic compression fleet equipped with vacuum chambers to eliminate air entrapment during vulcanization.</p>
              </div>
              <ul class="proc-list">
                <li>Full vacuum evacuation before mold closure</li>
                <li>Uniform platen thermal control across multi-cavities</li>
                <li>Handles large frame gaskets, dampers &amp; keypads</li>
              </ul>
            </div>
          </div>
        </div>

        <div class="secondary-strip">
          <div class="sec-strip-title">In-House Secondary Line</div>
          <div class="sec-strip-items">
            <span>2-Roll Mixing Mills</span>
            <span>3-Roll Ink Mills</span>
            <span>Flatbed Screen Printing</span>
            <span>IR Conveyor Dryers</span>
            <span>Post-Cure Baking Ovens</span>
          </div>
        </div>
      </div>

      <div class="bottom-bar">
        <span>Complete vertical control from raw compound milling to final post-cured packaging</span>
        <span class="page-num">05 / 07</span>
      </div>
    </div>
    """,

    # SLIDE 6: METROLOGY & QA LAB
    f"""
    <div class="slide light-slide" id="slide-6">
      <div class="top-bar">
        <div class="top-bar-left">
          <div class="kicker">05 &mdash; Quality Assurance &amp; Metrology</div>
          <h2 class="section-h2">Non-Contact Optical &amp; Mechanical Verification</h2>
        </div>
        <div class="top-bar-brand">
          <img src="{LOGO_URI}" alt="Logo"/>
          <span>Jun-Hsiang Enterprise</span>
        </div>
      </div>

      <div class="s6-body">
        <div class="qa-photos-stack">
          <div class="qa-card">
            <div class="qa-img-box">
              <img src="{QC_25D_URI}" alt="HO STAR 2.5D Optical Measuring System"/>
            </div>
            <div class="qa-card-body">
              <div class="prod-tag">Dimensional Metrology</div>
              <div class="qa-card-title">HO STAR 2.5D Optical System</div>
              <div class="qa-card-text">Non-contact optical edge inspection prevents mechanical deformation on soft elastomers, verifying critical IDs, ODs, and profiles against 2D drawings.</div>
            </div>
          </div>

          <div class="qa-card">
            <div class="qa-img-box">
              <img src="{QC_LOAD_URI}" alt="AIKOH Dynamic Load Curve Tester"/>
            </div>
            <div class="qa-card-body">
              <div class="prod-tag">Tactile &amp; Force Testing</div>
              <div class="qa-card-title">AIKOH Load Curve Tester</div>
              <div class="qa-card-text">Captures complete force-displacement curves (peak actuation force, return force, and tactile snap ratio) for keypad switch consistency.</div>
            </div>
          </div>
        </div>

        <div class="qa-protocol">
          <div>
            <div class="kicker">ISO 9001 Quality Workflow</div>
            <div class="qa-proto-head">4-Stage Inspection Gate</div>
          </div>

          <div class="qa-step-list">
            <div class="qa-step">
              <div class="qa-step-num">01</div>
              <div>
                <div class="qa-step-title">Incoming Compound Verification</div>
                <div class="qa-step-desc">Durometer (Shore A), batch traceability, and supplier RoHS / REACH / FDA lot documentation.</div>
              </div>
            </div>
            <div class="qa-step">
              <div class="qa-step-num">02</div>
              <div>
                <div class="qa-step-title">First Article Inspection (FAI)</div>
                <div class="qa-step-desc">Full dimensional report on T1 samples using 2.5D optical metrology prior to customer sign-off.</div>
              </div>
            </div>
            <div class="qa-step">
              <div class="qa-step-num">03</div>
              <div>
                <div class="qa-step-title">In-Process Molding Checks</div>
                <div class="qa-step-desc">Scheduled patrol checks on cure state, flash control, parting-line alignment, and visual defects.</div>
              </div>
            </div>
            <div class="qa-step">
              <div class="qa-step-num">04</div>
              <div>
                <div class="qa-step-title">Outgoing Visual &amp; Dimensional QA</div>
                <div class="qa-step-desc">Final lot sampling and visual screening before packing and export dispatch from Taiwan.</div>
              </div>
            </div>
          </div>

          <div class="qa-iso-note">ISO 9001 quality management system; raw material test reports available upon request.</div>
        </div>
      </div>

      <div class="bottom-bar">
        <span>In-house inspection lab ensures dimensional repeatability before parts leave Taiwan</span>
        <span class="page-num">06 / 07</span>
      </div>
    </div>
    """,

    # SLIDE 7: WORKFLOW & DIRECT CONTACT (DARK ARCHITECTURAL BACK COVER)
    f"""
    <div class="slide dark-closing" id="slide-7">
      <div class="dark-top-bar">
        <div class="top-bar-left">
          <div class="cover-kicker">06 &mdash; Engagement &amp; Direct Contact</div>
          <h2 class="dark-h2">From CAD Drawing to Global Delivery</h2>
        </div>
        <div class="cover-brand">
          <img src="{LOGO_URI}" alt="Logo"/>
        </div>
      </div>

      <div class="timeline-5">
        <div class="tl-item">
          <div class="tl-num">01</div>
          <div class="tl-title">CAD &amp; DFM Review</div>
          <div class="tl-desc">Draft angles, parting lines, wall thickness, and undercut evaluation under mutual NDA.</div>
        </div>
        <div class="tl-item">
          <div class="tl-num">02</div>
          <div class="tl-title">Compound &amp; Quote</div>
          <div class="tl-desc">Polymer &amp; Shore A selection, tooling NRE breakdown, and unit pricing by volume tier.</div>
        </div>
        <div class="tl-item">
          <div class="tl-num">03</div>
          <div class="tl-title">Tooling &amp; T1 Samples</div>
          <div class="tl-desc">Precision CNC/EDM mold fabrication, T1 molding trial, and 2.5D optical FAI report.</div>
        </div>
        <div class="tl-item">
          <div class="tl-num">04</div>
          <div class="tl-title">Validation &amp; Production</div>
          <div class="tl-desc">Customer fit sign-off, controlled vulcanization, post-cure baking, and outgoing QA.</div>
        </div>
        <div class="tl-item">
          <div class="tl-num">05</div>
          <div class="tl-title">Direct Global Export</div>
          <div class="tl-desc">Air or ocean logistics direct from Taiwan to USA, Europe, and Japan with standard export documentation.</div>
        </div>
      </div>

      <div class="closing-lower">
        <div class="rfq-panel">
          <div class="cover-kicker">Fast-Track Engineering Quotation</div>
          <div class="rfq-panel-title">RFQ Drawing Submission Checklist</div>
          <ul class="rfq-list">
            <li>2D drawing with critical tolerances</li>
            <li>3D CAD file (STEP / IGES / STP)</li>
            <li>Material &amp; Shore A durometer</li>
            <li>Operating temperature &amp; media</li>
            <li>Color spec (Pantone / RAL)</li>
            <li>Target prototype &amp; annual volume</li>
          </ul>
        </div>

        <div class="contact-panel">
          <div class="contact-headline">Send your 2D/3D drawings for a direct engineering feasibility review.</div>
          <div class="contact-grid">
            <div class="c-key">Contact</div>
            <div class="c-val">Andy Hsu &mdash; Engineering &amp; Global Sales</div>

            <div class="c-key">Email</div>
            <div class="c-val c-val-accent">andy_hsu@jun-hsiang.com.tw</div>

            <div class="c-key">Telephone</div>
            <div class="c-val">+886-2-2203-9918 &nbsp;(Fax: +886-2-2206-6968)</div>

            <div class="c-key">Factory</div>
            <div class="c-val">No. 1 &amp; 3, Ln. 345, Xinshu Rd., Xinzhuang Dist., New Taipei City 242, Taiwan</div>

            <div class="c-key">Website</div>
            <div class="c-val">https://www.jun-hsiang.com.tw/en/</div>
          </div>
        </div>
      </div>

      <div class="dark-bottom-bar">
        <span>Jun-Hsiang Enterprise Co., Ltd. &bull; Mutual NDA available prior to file transfer</span>
        <span style="color:#FFFFFF; font-weight:700; letter-spacing:2px;">07 / 07</span>
      </div>
    </div>
    """
]


def build_full_html(slides_subset):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Jun-Hsiang Enterprise Co., Ltd. — Company Capability Profile</title>
<style>{COMMON_CSS}</style>
</head>
<body>
{''.join(slides_subset)}
</body>
</html>"""


def generate_pdf_and_previews():
    print("[1/3] Generating 7-slide 16:9 Swiss Editorial PDF via Chrome Headless...")
    deck_html = WORKSPACE / "scratch" / "presentation_deck_v3.html"
    deck_html.write_text(build_full_html(SLIDES_HTML), encoding="utf-8")

    cmd_pdf = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={OUTPUT_PDF.resolve()}",
        str(deck_html.resolve().as_uri()),
    ]
    subprocess.run(cmd_pdf, check=True)
    print(f"  - PDF generated: {OUTPUT_PDF.name} ({OUTPUT_PDF.stat().st_size / 1024:.1f} KB)")

    print("[2/3] Capturing exact 1920x1080 full-bleed PNG previews...")
    for idx, slide_html in enumerate(SLIDES_HTML, start=1):
        single_file = WORKSPACE / "scratch" / f"single_v3_{idx}.html"
        single_file.write_text(build_full_html([slide_html]), encoding="utf-8")
        out_png = PREVIEWS_DIR / f"slide-{idx}.png"
        cmd_png = [
            CHROME_PATH,
            "--headless=new",
            "--disable-gpu",
            "--window-size=1920,1080",
            "--force-device-scale-factor=1",
            "--hide-scrollbars",
            f"--screenshot={out_png.resolve()}",
            str(single_file.resolve().as_uri()),
        ]
        subprocess.run(cmd_png, check=True)
        print(f"  - Captured {out_png.name}")


def add_picture_fit(slide, img_path, box_x, box_y, box_w, box_h):
    """Insert image centered inside (box_x, box_y, box_w, box_h) preserving exact aspect ratio."""
    p = Path(img_path)
    if not p.exists():
        return
    with Image.open(p) as im:
        iw, ih = im.size
    ratio = iw / ih
    box_ratio = box_w / box_h
    if ratio > box_ratio:
        w = box_w
        h = box_w / ratio
    else:
        h = box_h
        w = box_h * ratio
    x = box_x + (box_w - w) / 2
    y = box_y + (box_h - h) / 2
    slide.shapes.add_picture(str(p), Inches(x), Inches(y), width=Inches(w), height=Inches(h))


def generate_native_pptx():
    print("[3/3] Generating native editable 7-slide 16:9 PowerPoint (.pptx)...")
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

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

    def txt(slide, x, y, w, h, text, size=12, color=INK, bold=False, font="Arial", italic=False, align=PP_ALIGN.LEFT):
        tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.alignment = align
        p.text = text
        p.font.name = font
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.italic = italic
        p.font.color.rgb = color
        return tb

    def light_chrome(slide, bg_rgb, kicker, title, page_str):
        rect(slide, 0, 0, 13.333, 7.5, bg_rgb)
        txt(slide, 0.65, 0.42, 8.5, 0.25, kicker.upper(), size=9.5, color=GOLD, bold=True)
        txt(slide, 0.65, 0.68, 9.5, 0.55, title, size=26, color=DARK, bold=True)
        if LOGO_FILE.exists():
            add_picture_fit(slide, LOGO_FILE, 10.6, 0.55, 0.4, 0.4)
        txt(slide, 11.05, 0.66, 1.65, 0.25, "JUN-HSIANG", size=9, color=MUTED, bold=True)
        rect(slide, 0.65, 1.28, 12.033, 0.015, LINE)
        rect(slide, 0.65, 6.92, 12.033, 0.015, LINE)
        txt(slide, 0.65, 7.02, 9.5, 0.28, "Jun-Hsiang Enterprise Co., Ltd.  |  Custom Silicone & Rubber OEM Manufacturer", size=9, color=MUTED)
        txt(slide, 11.4, 7.02, 1.28, 0.28, page_str, size=9.5, color=DARK, bold=True, align=PP_ALIGN.RIGHT)

    # SLIDE 1: ARCHITECTURAL SPLIT COVER
    s1 = prs.slides.add_slide(blank)
    rect(s1, 0, 0, 7.8, 7.5, DARK)
    rect(s1, 7.8, 0, 5.533, 7.5, WARM)
    if LOGO_FILE.exists():
        add_picture_fit(s1, LOGO_FILE, 0.65, 0.5, 0.5, 0.5)
    txt(s1, 1.25, 0.53, 5.5, 0.25, "JUN-HSIANG ENTERPRISE CO., LTD.", size=11, color=WHITE, bold=True)
    txt(s1, 1.25, 0.78, 5.5, 0.22, "PRECISION ELASTOMER MANUFACTURING  |  TAIWAN", size=8.5, color=LIGHT_MUTED)

    txt(s1, 0.65, 2.05, 6.5, 0.28, "CORPORATE CAPABILITY PROFILE", size=10, color=GOLD_LIGHT, bold=True)
    txt(s1, 0.65, 2.4, 6.6, 1.55, "Custom Silicone &\nRubber Engineering", size=42, color=WHITE, bold=True)
    txt(s1, 0.65, 4.15, 6.4, 1.2, "In-house Liquid Silicone Rubber (LSR) injection, high-vacuum compression molding, and silicone-to-metal/plastic overmolding. Built in Taiwan for OEM and ODM engineering teams across North America, Europe, and Japan.", size=13, color=RGBColor(203, 213, 225))

    rect(s1, 0.65, 5.85, 6.5, 0.015, LINE_DARK)
    metas = [("ESTABLISHED", "Sep 1991 (35+ Yrs)"), ("QUALITY SYSTEM", "ISO 9001:2015"), ("SUPPLY CHAIN", "100% Made in Taiwan")]
    for i, (k, v) in enumerate(metas):
        txt(s1, 0.65 + i * 2.2, 6.05, 2.1, 0.22, k, size=8, color=LIGHT_MUTED, bold=True)
        txt(s1, 0.65 + i * 2.2, 6.3, 2.1, 0.3, v, size=11, color=WHITE, bold=True)

    txt(s1, 8.25, 0.52, 3.8, 0.25, "SELECTED MANUFACTURING HIGHLIGHTS", size=8.5, color=MUTED, bold=True)
    txt(s1, 12.1, 0.52, 0.8, 0.25, "01 / 07", size=8.5, color=MUTED, bold=True, align=PP_ALIGN.RIGHT)
    rect(s1, 8.25, 0.82, 4.65, 0.015, LINE)

    rect(s1, 8.25, 1.05, 4.65, 3.05, WHITE, LINE)
    add_picture_fit(s1, IMAGES_DIR / "equip-lsr.jpg", 8.45, 1.18, 4.25, 2.45)
    txt(s1, 8.45, 3.74, 4.25, 0.25, "FIG. 01   |   Vertical LSR Injection — MIV 1500-LS", size=8.5, color=MUTED, bold=True)

    rect(s1, 8.25, 4.35, 4.65, 2.65, WHITE, LINE)
    add_picture_fit(s1, IMAGES_DIR / "prod-orings.jpg", 8.45, 4.48, 4.25, 2.05)
    txt(s1, 8.45, 6.64, 4.25, 0.25, "FIG. 02   |   Custom O-Rings & Precision Seals", size=8.5, color=MUTED, bold=True)

    # SLIDE 2: HERITAGE & F.H.P.Q.
    s2 = prs.slides.add_slide(blank)
    light_chrome(s2, WHITE, "01 — Company Overview & Heritage", "35 Years of Precision Elastomer Tooling in Taiwan", "02 / 07")

    rect(s2, 0.65, 1.6, 3.85, 5.05, WARM)
    txt(s2, 0.95, 1.85, 1.8, 0.75, "1991", size=44, color=DARK, font="Georgia")
    txt(s2, 2.65, 2.0, 1.65, 0.55, "Founded in\nNew Taipei City", size=11, color=INK, bold=True)
    rect(s2, 0.95, 2.75, 3.25, 0.015, LINE)

    facts = [
        ("COMPANY", "Jun-Hsiang Enterprise Co., Ltd."),
        ("CAPITAL", "NTD 12,000,000"),
        ("BASE", "Xinzhuang Dist., New Taipei"),
        ("STANDARD", "ISO 9001:2015 Registered"),
        ("MARKETS", "USA, Europe, Japan"),
        ("ORIGIN", "100% Non-China Taiwan"),
    ]
    for i, (k, v) in enumerate(facts):
        y = 2.95 + i * 0.58
        txt(s2, 0.95, y, 1.15, 0.25, k, size=8.5, color=MUTED, bold=True)
        txt(s2, 2.05, y, 2.15, 0.25, v, size=10, color=INK, bold=True, align=PP_ALIGN.RIGHT)
        if i < len(facts) - 1:
            rect(s2, 0.95, y + 0.38, 3.25, 0.01, LINE)

    txt(s2, 4.95, 1.65, 7.7, 0.78, "Guided by our F.H.P.Q. operational discipline, we support global hardware teams from initial DFM review and mold fabrication through validated mass production.", size=15, color=INK)
    rect(s2, 4.95, 2.58, 7.7, 0.015, LINE)

    fhpq = [
        ("01", "Friend — Engineering Partnership", "Collaborative DFM feedback on parting lines, draft angles, undercut demolding, and material selection before tooling begins."),
        ("02", "Honesty — Protected Tooling & Specs", "Strict customer tooling ownership protection, NDA confidentiality, and transparent raw material compliance documentation."),
        ("03", "Profession — Vertical Integration", "In-house compounding, LSR injection, vacuum compression, screen printing, and secondary post-cure baking (laser etching & spray coating via vetted partners)."),
        ("04", "Quality — Zero-Defect Standard", "Do not accept, do not produce, and do not release defective parts. Backed by 2.5D optical and load testing."),
    ]
    for idx, (num, title, desc) in enumerate(fhpq):
        col = idx % 2
        row = idx // 2
        x = 4.95 + col * 3.95
        y = 2.85 + row * 1.95
        txt(s2, x, y, 0.6, 0.35, num, size=18, color=GOLD, font="Georgia")
        txt(s2, x, y + 0.36, 3.65, 0.32, title, size=13.5, color=DARK, bold=True)
        txt(s2, x, y + 0.72, 3.65, 1.0, desc, size=10.5, color=MUTED)

    # SLIDE 3: PROCESSES & MATERIALS
    s3 = prs.slides.add_slide(blank)
    light_chrome(s3, WARM, "02 — Manufacturing Capabilities", "Three Core Molding Processes & Material Matrix", "03 / 07")

    procs = [
        ("01", "LSR Liquid Silicone\nInjection", "Closed-loop metered A/B liquid silicone injection for complex geometries and cleanroom-grade consistency.",
         ["Vertical LSR press architecture (MIV 1500-LS)", "Flash-minimized cold-runner tooling options", "Ideal for medical masks, valves & optical seals", "Consistent batch-to-batch curing repeatability"], True),
        ("02", "Vacuum Compression\nMolding", "High-tonnage hydraulic molding with integrated vacuum evacuation for HCR silicone and synthetic rubbers.",
         ["Vacuum chamber prevents trapped air & voids", "Cost-effective tooling for prototypes & mid-volumes", "Supports conductive keypads, O-rings & gaskets", "Flexible Shore A 10 to 90 custom compounding"], False),
        ("03", "Overmolding &\nInsert Bonding", "Chemical and mechanical bonding of silicone directly onto metal hardware and high-temp plastics.",
         ["Silicone-to-stainless steel, aluminum & brass", "Silicone-to-PC, PBT, PA & PEEK substrates", "Controlled surface pretreatment & priming", "Eliminates manual assembly and leak paths"], False),
    ]
    for i, (num, title, summ, pts, is_dark) in enumerate(procs):
        x = 0.65 + i * 4.1
        bg = DARK if is_dark else WHITE
        bd = DARK if is_dark else LINE
        rect(s3, x, 1.55, 3.85, 4.15, bg, bd)
        txt(s3, x + 0.28, 1.78, 0.8, 0.4, num, size=24, color=GOLD_LIGHT if is_dark else GOLD, font="Georgia")
        txt(s3, x + 0.28, 2.25, 3.3, 0.65, title, size=16.5, color=WHITE if is_dark else DARK, bold=True)
        txt(s3, x + 0.28, 2.98, 3.3, 0.82, summ, size=10.5, color=RGBColor(203, 213, 225) if is_dark else MUTED)
        rect(s3, x + 0.28, 3.88, 3.3, 0.012, LINE_DARK if is_dark else LINE)
        tb = s3.shapes.add_textbox(Inches(x + 0.28), Inches(4.02), Inches(3.3), Inches(1.5))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        for j, pt in enumerate(pts):
            p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
            p.text = f"—  {pt}"
            p.font.name = "Arial"
            p.font.size = Pt(9.8)
            p.font.color.rgb = RGBColor(226, 232, 240) if is_dark else INK
            p.space_after = Pt(5)

    rect(s3, 0.65, 5.95, 12.033, 0.78, WHITE, LINE)
    txt(s3, 0.9, 6.12, 1.45, 0.45, "ELASTOMER\nMATERIALS", size=9, color=DARK, bold=True)
    rect(s3, 2.4, 6.08, 0.015, 0.52, LINE)
    mats = [("LSR", "Medical & Optical"), ("VMQ", "FDA / LFGB"), ("FKM", "Viton Chemical"), ("FVMQ", "Fuel & Oil"), ("EPDM", "Weather & Steam"), ("NBR / CR", "Industrial Seals")]
    for i, (m, d) in enumerate(mats):
        mx = 2.65 + i * 1.65
        txt(s3, mx, 6.12, 1.55, 0.24, m, size=11.5, color=DARK, bold=True)
        txt(s3, mx, 6.38, 1.55, 0.22, d, size=9, color=MUTED)

    # SLIDE 4: PRODUCT PORTFOLIO
    s4 = prs.slides.add_slide(blank)
    light_chrome(s4, WHITE, "03 — Product Portfolio", "Custom Components Built to Print", "04 / 07")

    cards4 = [
        ("prod-keypads.jpg", "HMI & TACTILE INTERFACES", "Conductive Silicone Keypads",
         ["Conductive carbon pills & gold contacts", "In-house multi-color silk-screen printing", "Partner-coordinated laser etching & spray coating"],
         "Apps: Industrial controllers, POS, remotes"),
        ("prod-orings.jpg", "FLUID & PRESSURE SEALING", "Custom O-Rings & Oil Seals",
         ["AS568, JIS B2401 & custom sizes", "Thermal stability -50°C to +250°C (by material)", "Low compression set compounds"],
         "Apps: Automotive harnesses, valves, pumps"),
        ("prod-medical-kb.jpg", "HEALTHCARE & CLEANROOM", "Medical Washable Keyboards",
         ["Seamless watertight hygienic surface", "Resists hospital disinfectants", "Biocompatible & food-grade silicone"],
         "Apps: Clinical carts, dental, cleanrooms"),
        ("prod-gaskets.jpg", "ENCLOSURE PROTECTION", "Precision Frame Gaskets",
         ["Complex 3D perimeter rib profiles", "Waterproof & dust-resistant enclosure sealing", "Self-lubricating & EMI options"],
         "Apps: Outdoor telecom, UAVs, sensors"),
    ]
    for idx, (img_name, tag, title, pts, app) in enumerate(cards4):
        col = idx % 2
        row = idx // 2
        x = 0.65 + col * 6.15
        y = 1.55 + row * 2.65
        rect(s4, x, y, 5.88, 2.42, WARM, LINE)
        rect(s4, x, y, 2.35, 2.42, WHITE, LINE)
        add_picture_fit(s4, IMAGES_DIR / img_name, x + 0.14, y + 0.14, 2.07, 2.14)
        tx = x + 2.58
        txt(s4, tx, y + 0.2, 3.1, 0.22, tag, size=8.2, color=GOLD, bold=True)
        txt(s4, tx, y + 0.44, 3.1, 0.34, title, size=14.5, color=DARK, bold=True)
        tb = s4.shapes.add_textbox(Inches(tx), Inches(y + 0.85), Inches(3.1), Inches(1.0))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        for j, pt in enumerate(pts):
            p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
            p.text = f"—  {pt}"
            p.font.name = "Arial"
            p.font.size = Pt(9.5)
            p.font.color.rgb = MUTED
            p.space_after = Pt(3)
        rect(s4, tx, y + 1.95, 3.05, 0.012, LINE)
        txt(s4, tx, y + 2.04, 3.1, 0.26, app, size=8.5, color=INK, bold=True)

    # SLIDE 5: IN-HOUSE EQUIPMENT
    s5 = prs.slides.add_slide(blank)
    light_chrome(s5, WARM, "04 — Production Infrastructure", "In-House Molding Fleet & Secondary Processing", "05 / 07")

    equips = [
        ("equip-lsr.jpg", "LIQUID INJECTION SYSTEM", "Vertical LSR\nInjection Press",
         "Chuan-Lien MIV 1500-LS vertical clamping system for insert loading and precision liquid silicone molding.",
         ["Closed A/B metered dosing & mixing", "Vertical ergonomics for metal inserts", "Consistent cavity fill for micro-features"]),
        ("equip-vacuum-press.jpg", "SOLID ELASTOMER FLEET", "Vacuum Compression\nPresses",
         "Heavy-duty hydraulic compression fleet with vacuum chambers to eliminate air entrapment during vulcanization.",
         ["Full vacuum evacuation before closure", "Uniform platen thermal control", "Handles large gaskets, dampers & keypads"]),
    ]
    for i, (img_name, tag, title, desc, pts) in enumerate(equips):
        x = 0.65 + i * 6.18
        rect(s5, x, 1.55, 5.85, 4.2, WHITE, LINE)
        rect(s5, x, 1.55, 2.55, 4.2, WHITE, LINE)
        add_picture_fit(s5, IMAGES_DIR / img_name, x + 0.16, 1.72, 2.23, 3.86)
        tx = x + 2.8
        txt(s5, tx, 1.82, 2.85, 0.22, tag, size=8.5, color=GOLD, bold=True)
        txt(s5, tx, 2.1, 2.85, 0.65, title, size=17, color=DARK, bold=True)
        txt(s5, tx, 2.85, 2.85, 0.95, desc, size=10, color=MUTED)
        rect(s5, tx, 3.92, 2.8, 0.012, LINE)
        tb = s5.shapes.add_textbox(Inches(tx), Inches(4.08), Inches(2.85), Inches(1.45))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        for j, pt in enumerate(pts):
            p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
            p.text = f"—  {pt}"
            p.font.name = "Arial"
            p.font.size = Pt(9.8)
            p.font.color.rgb = INK
            p.space_after = Pt(5)

    rect(s5, 0.65, 6.02, 12.033, 0.68, DARK)
    txt(s5, 0.92, 6.25, 2.4, 0.25, "IN-HOUSE SECONDARY LINE", size=9, color=GOLD_LIGHT, bold=True)
    txt(s5, 3.45, 6.24, 9.0, 0.26, "2-Roll Mixing Mills   |   3-Roll Ink Mills   |   Flatbed Screen Printing   |   IR Conveyor Dryers   |   Post-Cure Ovens", size=10.5, color=WHITE)

    # SLIDE 6: METROLOGY & QA LAB
    s6 = prs.slides.add_slide(blank)
    light_chrome(s6, WHITE, "05 — Quality Assurance & Metrology", "Non-Contact Optical & Mechanical Verification", "06 / 07")

    qas = [
        ("qc-25d-optical.jpg", "DIMENSIONAL METROLOGY", "HO STAR 2.5D Optical System",
         "Non-contact optical edge inspection prevents mechanical deformation on soft elastomers, verifying critical IDs, ODs, and profiles."),
        ("qc-load-curve.jpg", "TACTILE & FORCE TESTING", "AIKOH Load Curve Tester",
         "Captures complete force-displacement curves (peak actuation force, return force, and tactile snap ratio) for keypad switch consistency."),
    ]
    for i, (img_name, tag, title, desc) in enumerate(qas):
        x = 0.65 + i * 3.55
        rect(s6, x, 1.55, 3.32, 5.1, WARM, LINE)
        rect(s6, x, 1.55, 3.32, 2.65, WHITE, LINE)
        add_picture_fit(s6, IMAGES_DIR / img_name, x + 0.14, 1.7, 3.04, 2.35)
        txt(s6, x + 0.22, 4.38, 2.88, 0.22, tag, size=8.2, color=GOLD, bold=True)
        txt(s6, x + 0.22, 4.65, 2.88, 0.35, title, size=13.5, color=DARK, bold=True)
        txt(s6, x + 0.22, 5.05, 2.88, 1.4, desc, size=10, color=MUTED)

    rect(s6, 7.85, 1.55, 4.83, 5.1, WARM)
    txt(s6, 8.18, 1.82, 4.2, 0.22, "ISO 9001 QUALITY WORKFLOW", size=8.5, color=GOLD, bold=True)
    txt(s6, 8.18, 2.08, 4.2, 0.36, "4-Stage Inspection Gate", size=16, color=DARK, bold=True)
    rect(s6, 8.18, 2.54, 4.18, 0.015, LINE)

    gates = [
        ("01", "Incoming Compound Check", "Shore A, batch traceability, RoHS/REACH/FDA lot docs."),
        ("02", "First Article Inspection (FAI)", "Full 2.5D optical dimensional report on T1 samples."),
        ("03", "In-Process Molding Checks", "Scheduled checks on cure state, flash & visual quality."),
        ("04", "Outgoing Visual & Dimensional QA", "Final lot sampling & visual screening prior to export."),
    ]
    for i, (num, title, desc) in enumerate(gates):
        y = 2.8 + i * 0.82
        txt(s6, 8.18, y, 0.4, 0.3, num, size=14, color=GOLD, font="Georgia")
        txt(s6, 8.62, y, 3.75, 0.24, title, size=10.8, color=DARK, bold=True)
        txt(s6, 8.62, y + 0.25, 3.75, 0.34, desc, size=9.2, color=MUTED)
    rect(s6, 8.18, 6.18, 4.18, 0.015, LINE)
    txt(s6, 8.18, 6.28, 4.2, 0.28, "ISO 9001 quality management system; material reports on request.", size=8.8, color=INK, bold=True)

    # SLIDE 7: DARK ARCHITECTURAL CLOSING
    s7 = prs.slides.add_slide(blank)
    rect(s7, 0, 0, 13.333, 7.5, DARK)
    txt(s7, 0.65, 0.45, 8.5, 0.25, "06 — ENGAGEMENT & DIRECT CONTACT", size=9.5, color=GOLD_LIGHT, bold=True)
    txt(s7, 0.65, 0.72, 9.5, 0.52, "From CAD Drawing to Global Delivery", size=28, color=WHITE, bold=True)
    if LOGO_FILE.exists():
        add_picture_fit(s7, LOGO_FILE, 12.2, 0.55, 0.48, 0.48)
    rect(s7, 0.65, 1.35, 12.033, 0.015, LINE_DARK)

    steps = [
        ("01", "CAD & DFM Review", "Draft angles, parting lines & undercut evaluation under NDA."),
        ("02", "Compound & Quote", "Polymer & Shore A selection, tooling NRE & volume pricing."),
        ("03", "Tooling & T1 Samples", "CNC/EDM mold fabrication, T1 trial & 2.5D optical FAI."),
        ("04", "Validation & Mass Prod", "Customer fit approval, vulcanization, post-cure & QA."),
        ("05", "Direct Global Export", "Air/Ocean shipping from Taiwan to USA, EU & Japan."),
    ]
    for i, (num, title, desc) in enumerate(steps):
        x = 0.65 + i * 2.43
        txt(s7, x, 1.65, 0.6, 0.38, num, size=20, color=GOLD_LIGHT, font="Georgia")
        txt(s7, x, 2.08, 2.22, 0.32, title, size=12, color=WHITE, bold=True)
        txt(s7, x, 2.45, 2.22, 0.85, desc, size=9.5, color=LIGHT_MUTED)
        if i < 4:
            rect(s7, x + 2.3, 1.72, 0.012, 1.45, LINE_DARK)

    rect(s7, 0.65, 3.45, 12.033, 0.015, LINE_DARK)

    rect(s7, 0.65, 3.8, 5.55, 2.75, RGBColor(21, 28, 40), LINE_DARK)
    txt(s7, 0.95, 4.05, 4.9, 0.22, "FAST-TRACK ENGINEERING QUOTATION", size=8.5, color=GOLD_LIGHT, bold=True)
    txt(s7, 0.95, 4.32, 4.9, 0.35, "RFQ Drawing Submission Checklist", size=15, color=WHITE, bold=True)
    chk = [
        "2D drawing with tolerances", "3D CAD (STEP / IGES)",
        "Material & Shore A hardness", "Operating temp & media",
        "Color spec (Pantone / RAL)", "Prototype & annual volume"
    ]
    for i, item in enumerate(chk):
        col = i % 2
        row = i // 2
        txt(s7, 0.95 + col * 2.5, 4.85 + row * 0.45, 2.4, 0.32, f"—  {item}", size=10, color=RGBColor(209, 213, 219))

    txt(s7, 6.65, 3.82, 6.0, 0.72, "Send your 2D/3D drawings for a direct engineering feasibility review.", size=19, color=WHITE, font="Georgia")
    contacts = [
        ("CONTACT", "Andy Hsu — Engineering & Global Sales", WHITE),
        ("EMAIL", "andy_hsu@jun-hsiang.com.tw", GOLD_LIGHT),
        ("TELEPHONE", "+886-2-2203-9918  (Fax: +886-2-2206-6968)", WHITE),
        ("FACTORY", "No. 1 & 3, Ln. 345, Xinshu Rd., Xinzhuang Dist., New Taipei City 242, Taiwan", WHITE),
        ("WEBSITE", "https://www.jun-hsiang.com.tw/en/", WHITE),
    ]
    for i, (k, v, col_rgb) in enumerate(contacts):
        y = 4.72 + i * 0.36
        txt(s7, 6.65, y, 1.15, 0.25, k, size=8.5, color=LIGHT_MUTED, bold=True)
        txt(s7, 7.85, y, 4.85, 0.32, v, size=10.5, color=col_rgb, bold=(col_rgb == GOLD_LIGHT))

    rect(s7, 0.65, 6.92, 12.033, 0.015, LINE_DARK)
    txt(s7, 0.65, 7.02, 9.5, 0.28, "Jun-Hsiang Enterprise Co., Ltd.  |  Mutual NDA available prior to file transfer", size=9, color=LIGHT_MUTED)
    txt(s7, 11.4, 7.02, 1.28, 0.28, "07 / 07", size=9.5, color=WHITE, bold=True, align=PP_ALIGN.RIGHT)

    prs.save(str(OUTPUT_PPTX))
    print(f"  - Native 16:9 PPTX saved: {OUTPUT_PPTX.name} ({OUTPUT_PPTX.stat().st_size / 1024:.1f} KB)")


def main():
    generate_pdf_and_previews()
    generate_native_pptx()
    print("ALL DONE!")


if __name__ == "__main__":
    main()
