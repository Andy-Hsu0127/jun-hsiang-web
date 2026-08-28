#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit Tests for Jun-Hsiang Claim Governance Validator (12 Test Cases)
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from claim_validator import ClaimValidator


class TestClaimValidator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'claim_registry.csv'))
        cls.validator = ClaimValidator(cls.registry_path)

    def _audit_snippet(self, html_snippet: str):
        with tempfile.NamedTemporaryFile('w', suffix='.html', encoding='utf-8', delete=False) as f:
            f.write(f"<!DOCTYPE html><html><body>{html_snippet}</body></html>")
            temp_path = f.name
        try:
            return self.validator.audit_file(temp_path)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_01_blocked_terms_raise_error(self):
        """Test 1: BLOCKED terms (零缺陷, 雙色LSR, 冷流道) must raise ERROR."""
        html = """
        <div>
            <p>我們的模具具備冷流道系統。</p>
            <p>全廠追求出廠零缺陷。</p>
            <p>引進雙色射出成型機。</p>
        </div>
        """
        res = self._audit_snippet(html)
        self.assertGreaterEqual(res['counts']['ERROR'], 3)
        error_claims = [f['claim_id'] for f in res['findings'] if f['level'] == 'ERROR']
        self.assertIn('CLM-010', error_claims)
        self.assertIn('CLM-012', error_claims)
        self.assertIn('CLM-013', error_claims)

    def test_02_blocked_priority_override(self):
        """Test 2 (Test 11): BLOCKED priority overrides qualifiers."""
        html = "<p>我們可依客戶需求提供 FDA 認證工廠生產服務。</p>"
        res = self._audit_snippet(html)
        self.assertGreaterEqual(res['counts']['ERROR'], 1)
        error_claims = [f['claim_id'] for f in res['findings'] if f['level'] == 'ERROR']
        self.assertIn('CLM-009', error_claims)

    def test_03_same_sentence_qualifier_pass(self):
        """Test 3: CONDITIONAL claim with qualifier in the same sentence should PASS (INFO)."""
        html = "<p>本廠可依客戶需求選用符合 FDA 認可之指定材料。</p>"
        res = self._audit_snippet(html)
        self.assertEqual(res['counts']['ERROR'], 0)
        self.assertEqual(res['counts']['WARNING'], 0)
        self.assertGreaterEqual(res['counts']['CONDITIONAL_PASS'], 1)

    def test_04_same_paragraph_qualifier_pass(self):
        """Test 4: CONDITIONAL claim with qualifier in the same <p> tag should PASS (INFO)."""
        html = "<p>我們專營客製化模具製造。產品可配合食品與醫療級規範，部分材料具備 FDA 與 LFGB 相關文件，依指定材料規格確認。</p>"
        res = self._audit_snippet(html)
        self.assertEqual(res['counts']['ERROR'], 0)
        self.assertEqual(res['counts']['WARNING'], 0)
        self.assertGreaterEqual(res['counts']['CONDITIONAL_PASS'], 1)

    def test_05_missing_qualifier_raises_warning(self):
        """Test 5: CONDITIONAL claim without any qualifier raises WARNING."""
        html = "<p>本廠全面具備 FDA 食品級保證。</p>"
        res = self._audit_snippet(html)
        self.assertEqual(res['counts']['ERROR'], 0)
        self.assertGreaterEqual(res['counts']['WARNING'], 1)

    def test_06_verified_terms_pass(self):
        """Test 6: VERIFIED claims (ISO 9001, 創立於 1991, 單色 LSR) PASS automatically."""
        html = """
        <div>
            <p>鈞翔實業通過 ISO 9001 品質體系認證。</p>
            <p>公司創立於 1991 年，專注於單色 LSR 射出加工。</p>
        </div>
        """
        res = self._audit_snippet(html)
        self.assertEqual(res['counts']['ERROR'], 0)
        self.assertEqual(res['counts']['WARNING'], 0)
        self.assertGreaterEqual(res['counts']['VERIFIED'], 3)

    def test_07_dynamic_years_calculation(self):
        """Test 7: Dynamic years (30+ 年) calculated against foundation year (1991)."""
        html_valid = "<p>鈞翔實業擁有 30+ 年業界經驗。</p>"
        res_valid = self._audit_snippet(html_valid)
        self.assertEqual(res_valid['counts']['ERROR'], 0)
        self.assertEqual(res_valid['counts']['WARNING'], 0)
        self.assertGreaterEqual(res_valid['counts']['VERIFIED'], 1)

        # 90+ years would exceed 2026 - 1991 = 35
        html_invalid = "<p>鈞翔實業擁有 90+ 年業界經驗。</p>"
        res_invalid = self._audit_snippet(html_invalid)
        self.assertGreaterEqual(res_invalid['counts']['WARNING'], 1)

    def test_08_script_style_exclusion(self):
        """Test 8 (Test 12): <script> and <style> contents are excluded from visible scan."""
        html = """
        <style>
            /* 零缺陷 should be ignored in CSS */
            .cold-runner { display: none; }
        </style>
        <script>
            // 冷流道 variable in JS should be ignored
            var forbidden = "雙色射出";
        </script>
        <p>鈞翔實業通過 ISO 9001 驗證。</p>
        """
        res = self._audit_snippet(html)
        self.assertEqual(res['counts']['ERROR'], 0)
        self.assertEqual(res['counts']['WARNING'], 0)
        self.assertEqual(res['counts']['VERIFIED'], 1)

    def test_09_multilingual_zhtw_support(self):
        """Test 9: Traditional Chinese claim compliance check."""
        html = "<p>原料符合 RoHS 與 REACH 環保規範，相關材質證明文件可依專案需求配合提供。</p>"
        res = self._audit_snippet(html)
        self.assertEqual(res['counts']['ERROR'], 0)
        self.assertEqual(res['counts']['WARNING'], 0)
        self.assertGreaterEqual(res['counts']['CONDITIONAL_PASS'], 2)

    def test_10_multilingual_en_support(self):
        """Test 10: English claim compliance check with case insensitivity."""
        html = "<p>Raw materials comply with RoHS and REACH standards. Material certificates are available upon request.</p>"
        res = self._audit_snippet(html)
        self.assertEqual(res['counts']['ERROR'], 0)
        self.assertEqual(res['counts']['WARNING'], 0)
        self.assertGreaterEqual(res['counts']['CONDITIONAL_PASS'], 2)

    def test_11_multilingual_ja_support(self):
        """Test 11: Japanese blocked term detection (剥離ゼロ, コールドランナー)."""
        html_blocked = "<p>コールドランナー金型により剥離ゼロを実現。</p>"
        res_blocked = self._audit_snippet(html_blocked)
        self.assertGreaterEqual(res_blocked['counts']['ERROR'], 2)

        html_pass = "<p>RoHS・REACH規制に適合した原料を使用し、お客様のご要望に応じて材質証明書の発行に対応いたします。</p>"
        res_pass = self._audit_snippet(html_pass)
        self.assertEqual(res_pass['counts']['ERROR'], 0)
        self.assertEqual(res_pass['counts']['WARNING'], 0)

    def test_12_exit_code_and_report_schema(self):
        """Test 12: Directory audit structure and schema validation."""
        report = self.validator.audit_directory(os.path.dirname(__file__))
        self.assertIn('timestamp', report)
        self.assertIn('files_scanned', report)
        self.assertIn('summary', report)
        self.assertIn('status', report)
        self.assertIn(report['status'], ['PASSED', 'BLOCKED'])


if __name__ == '__main__':
    unittest.main()
