import glob
import os
import re
import subprocess
import tempfile

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

PRINT_CSS = """
<style id="pdf-print-override">
  @page { size: A4; margin: 16mm 14mm; }
  html, body {
    background: #ffffff !important;
    color: #111827 !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
    font-size: 11pt !important;
    line-height: 1.55 !important;
  }
  nav, .navbar, .mobile-menu, .article-quick-bar, form, .g-recaptcha, .footer-nav, .breadcrumb {
    display: none !important;
  }
  .page-hero {
    background: #f8fafc !important;
    color: #0f172a !important;
    padding: 18px 20px !important;
    border-bottom: 2px solid #0d9488 !important;
    margin-bottom: 16px !important;
  }
  .page-hero-title, h1, h2, h3, h4, p, li, td, th, span, strong {
    color: #111827 !important;
  }
  .page-hero-subtitle {
    color: #475569 !important;
  }
  a { color: #0f766e !important; text-decoration: underline !important; }
  table { border-collapse: collapse !important; width: 100% !important; page-break-inside: avoid; }
  th, td { border: 1px solid #cbd5e1 !important; padding: 6px 8px !important; }
  .article-cta, .article-related, .footer {
    background: #f8fafc !important;
    border: 1px solid #cbd5e1 !important;
    color: #111827 !important;
    page-break-inside: avoid;
  }
  .pdf-brand-banner {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #cbd5e1;
    padding-bottom: 8px;
    margin-bottom: 12px;
    font-size: 9pt;
    color: #334155 !important;
  }
</style>
"""


def generate_pdfs():
    if not os.path.exists(CHROME_PATH):
        raise FileNotFoundError(f"Chrome not found at {CHROME_PATH}")

    repo_root = os.path.abspath(".")
    created = 0

    with tempfile.TemporaryDirectory() as tmp_dir:
        for lang in ["en", "ja"]:
            out_dir = os.path.join(repo_root, "pdf", lang)
            os.makedirs(out_dir, exist_ok=True)
            files = sorted(glob.glob(f"{lang}/knowledge-*.html"))

            for p in files:
                base = os.path.basename(p)
                with open(p, "r", encoding="utf-8") as f:
                    html = f.read()
                if 'http-equiv="refresh"' in html:
                    continue

                pdf_name = base.replace(".html", f"-{lang}.pdf")
                pdf_path = os.path.join(out_dir, pdf_name)

                # Rewrite relative ../ links for temp rendering in lang dir
                base_href = f'<base href="file:///{os.path.join(repo_root, lang).replace(os.sep, "/")}/"/>'
                banner = (
                    '<div class="pdf-brand-banner">'
                    '<span><strong>Jun-Hsiang Enterprise Co., Ltd.</strong> | 100% Made in Taiwan OEM • ISO 9001:2015</span>'
                    '<span>Written RFQ Email: <a href="mailto:andy_hsu@jun-hsiang.com.tw">andy_hsu@jun-hsiang.com.tw</a></span>'
                    '</div>'
                )

                mod_html = html.replace("<head>", "<head>\n" + base_href + PRINT_CSS, 1)
                mod_html = re.sub(r'(<article\b[^>]*>)', r'\1\n' + banner, mod_html, count=1)

                tmp_html = os.path.join(tmp_dir, f"{lang}_{base}")
                with open(tmp_html, "w", encoding="utf-8") as tf:
                    tf.write(mod_html)

                tmp_url = "file:///" + tmp_html.replace(os.sep, "/")
                cmd = [
                    CHROME_PATH,
                    "--headless=new",
                    "--disable-gpu",
                    "--no-sandbox",
                    f"--user-data-dir={os.path.join(tmp_dir, 'chrome_prof')}",
                    "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf_path}",
                    tmp_url,
                ]
                res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
                if res.returncode == 0 and os.path.exists(pdf_path):
                    created += 1
                else:
                    print(f"Failed PDF for {p}: {res.stderr.decode(errors='ignore')[:200]}")

    print(f"Generated {created} PDF technical guides.")


if __name__ == "__main__":
    generate_pdfs()
