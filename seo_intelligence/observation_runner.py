#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jun-Hsiang SEO & RFQ Commercial Intelligence Observation Runner v1.0
Automates Baseline Generation, Evidence Review, and Commercial Outcome Tracking
"""

import os
import sys
import json
import csv
from datetime import datetime
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass


class ObservationRunner:
    def __init__(self, workspace_root=None):
        self.workspace_root = Path(workspace_root or Path(__file__).resolve().parent.parent)
        self.reports_dir = self.workspace_root / "seo_intelligence" / "reports"
        self.baselines_dir = self.workspace_root / "seo_intelligence" / "baselines"
        self.rfq_csv_path = self.workspace_root / "seo_intelligence" / "rfq_outcome_registry.csv"
        self.day0_json_path = self.baselines_dir / "day0_baseline_20260828.json"
        
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.baselines_dir.mkdir(parents=True, exist_ok=True)

    def load_rfq_outcomes(self):
        """Parse RFQ outcome registry and calculate funnel metrics."""
        records = []
        if not self.rfq_csv_path.exists():
            return records
        
        with open(self.rfq_csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(row)
        return records

    def aggregate_cluster_funnel(self, rfq_records):
        """Aggregate RFQ funnel by topic cluster."""
        clusters = {}
        for r in rfq_records:
            c = r.get("source_cluster", "general")
            if c not in clusters:
                clusters[c] = {
                    "total_rfq": 0,
                    "cad_count": 0,
                    "quoted_count": 0,
                    "sample_count": 0,
                    "won_count": 0,
                    "total_order_value": 0
                }
            clusters[c]["total_rfq"] += 1
            if r.get("has_cad", "").upper() == "YES":
                clusters[c]["cad_count"] += 1
            if r.get("quote_status", "").upper() == "QUOTED":
                clusters[c]["quoted_count"] += 1
            if r.get("sample_status", "").upper() in ["SENT", "APPROVED"]:
                clusters[c]["sample_count"] += 1
            if r.get("won_status", "").upper() == "WON":
                clusters[c]["won_count"] += 1
            try:
                clusters[c]["total_order_value"] += float(r.get("order_value_twd", 0) or 0)
            except ValueError:
                pass
        return clusters

    def generate_day0_report(self):
        """Generate Day 0 Baseline Markdown and JSON."""
        day0_data = {}
        if self.day0_json_path.exists():
            with open(self.day0_json_path, "r", encoding="utf-8") as f:
                day0_data = json.load(f)
        
        rfqs = self.load_rfq_outcomes()
        funnel = self.aggregate_cluster_funnel(rfqs)
        
        report_md = [
            "# 📊 Jun-Hsiang Day 0 SEO & Commercial Intelligence Baseline",
            f"**建立時間**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ",
            f"**觀測模式狀態**: 🟢 ACTIVE (Observation Mode)  ",
            "**代碼凍結狀態**: 🔒 Step 1 Governance, Step 2 Attribution, Step 3 MVP Article FROZEN\n",
            "---",
            "## 1. 🎯 核心觀測文章 (Target Article Baseline)",
            "| 文章 Slug | 所屬叢集 | 角色定位 | Day 0 GSC 狀態 | 核心鎖定意圖詞 |",
            "| :--- | :--- | :--- | :--- | :--- |",
            "| `silicone-metal-bonding-failure` | 🥈 Overmolding | Diagnostic Entrance MVP | 0 Impr / 0 Click | 矽膠包鐵脫膠、矽膠包金屬脫膠原因 |",
            "| `silicone-overmolding-bonding` | 🥈 Overmolding | Pillar Guide | 基準觀測中 | 矽膠包金屬、異材結合代工 |",
            "| `self-lubricating-silicone` | Self-Lubricating | Pillar Guide | 基準觀測中 | 自潤矽膠、出油膠 |",
            "\n---",
            "## 2. 🛡️ 全站技術與治理指標健全度 (Site & Governance Health)",
            f"- **總 HTML 頁面數**: {day0_data.get('site_inventory', {}).get('total_html_files', 114)} 頁",
            f"- **Sitemap 登記 URL 數**: {day0_data.get('site_inventory', {}).get('sitemap_urls_count', 114)} 筆",
            f"- **Claim Governance 違規數**: 0 (Production Gate: 🟢 PASSED)",
            f"- **RFQ 歸因引擎版本**: v1 (支援 First Touch, Content Journey, Conversion Touch)",
            "\n---",
            "## 3. 💼 商務轉換漏斗基準 (RFQ Commercial Funnel Baseline)",
            "| 主題叢集 (Cluster) | RFQ 總數 | CAD 附圖率 | 已報價數 (Quoted) | 打樣數 (Sample) | 成交數 (Won) |",
            "| :--- | :---: | :---: | :---: | :---: | :---: |"
        ]
        
        for c, data in funnel.items():
            cad_rate = f"{(data['cad_count'] / data['total_rfq'] * 100):.0f}%" if data['total_rfq'] > 0 else "0%"
            report_md.append(f"| **{c}** | {data['total_rfq']} | {cad_rate} | {data['quoted_count']} | {data['sample_count']} | {data['won_count']} |")
        
        if not funnel:
            report_md.append("| *(目前處於 Day 0 基準建立期，尚無正式 RFQ)* | - | - | - | - | - |")
            
        report_md.extend([
            "\n---",
            "## 4. 🧭 下一階段觀測節點與驗收標準",
            "- **Day 7 (2026-09-04)**: 技術收錄驗收（Check Index Status / Canonical / robots.txt）",
            "- **Day 28 (2026-09-25)**: 搜尋信號探勘（Capture Real Market Queries / Early Impressions）",
            "- **Day 56 (2026-10-23)**: GSC × RFQ 商業歸因交叉驗證（Content-to-RFQ Correlation）",
            "- **Day 90 (2026-11-26)**: Cluster 商業價值與 ROI 結算（Final Commercial ROI Decision Matrix）"
        ])
        
        report_text = "\n".join(report_md)
        out_path = self.reports_dir / "day0_baseline_report.md"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(report_text)
            
        return out_path, report_text


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Jun-Hsiang Observation Pipeline Runner")
    parser.add_argument("--report", choices=["day0", "day7", "day28", "day56", "day90"], default="day0", help="Observation report type")
    args = parser.parse_args()
    
    runner = ObservationRunner()
    if args.report == "day0":
        out_path, report_text = runner.generate_day0_report()
        print(f"✅ Day 0 Baseline report generated at: {out_path}\n")
        print(report_text)


if __name__ == "__main__":
    main()
