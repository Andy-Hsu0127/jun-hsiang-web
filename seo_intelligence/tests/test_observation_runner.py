#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for ObservationRunner
"""

import unittest
import os
import json
from pathlib import Path
from seo_intelligence.observation_runner import ObservationRunner

class TestObservationRunner(unittest.TestCase):
    def setUp(self):
        self.runner = ObservationRunner()

    def test_01_load_rfq_outcomes(self):
        records = self.runner.load_rfq_outcomes()
        self.assertIsInstance(records, list)

    def test_02_aggregate_cluster_funnel(self):
        records = [
            {"source_cluster": "overmolding", "has_cad": "YES", "quote_status": "QUOTED", "sample_status": "SENT", "won_status": "OPEN", "order_value_twd": "50000"},
            {"source_cluster": "overmolding", "has_cad": "NO", "quote_status": "REVIEWING", "sample_status": "N/A", "won_status": "OPEN", "order_value_twd": "0"},
            {"source_cluster": "lsr_injection", "has_cad": "YES", "quote_status": "QUOTED", "sample_status": "APPROVED", "won_status": "WON", "order_value_twd": "120000"},
        ]
        funnel = self.runner.aggregate_cluster_funnel(records)
        self.assertIn("overmolding", funnel)
        self.assertEqual(funnel["overmolding"]["total_rfq"], 2)
        self.assertEqual(funnel["overmolding"]["cad_count"], 1)
        self.assertEqual(funnel["overmolding"]["quoted_count"], 1)
        self.assertEqual(funnel["lsr_injection"]["won_count"], 1)
        self.assertEqual(funnel["lsr_injection"]["total_order_value"], 120000.0)

    def test_03_generate_day0_report(self):
        out_path, report_text = self.runner.generate_day0_report()
        self.assertTrue(os.path.exists(out_path))
        self.assertIn("Day 0 SEO & Commercial Intelligence Baseline", report_text)
        self.assertIn("silicone-metal-bonding-failure", report_text)
        self.assertIn("Day 7", report_text)

if __name__ == "__main__":
    unittest.main()
