#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jun-Hsiang Claim Governance & Production Gate Validator v1.0
Automates the verification of website technical claims against claim_registry.csv
"""

import os
import sys
import re
import csv
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Tuple
from bs4 import BeautifulSoup, NavigableString, Comment

# Ensure UTF-8 output on Windows consoles
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

FOUNDATION_YEAR = 1991

class ClaimRule:
    def __init__(self, row: Dict[str, str]):
        self.claim_id = row['claim_id'].strip()
        self.claim_pattern = row['claim_pattern'].strip()
        self.claim_type = row['claim_type'].strip()
        self.status = row['status'].strip()  # VERIFIED, CONDITIONAL, BLOCKED
        self.evidence_source = row['evidence_source'].strip()
        self.evidence_updated_at = row['evidence_updated_at'].strip()
        self.allowed_scope = row['allowed_scope'].strip()
        self.required_qualifier = row['required_qualifier'].strip()
        self.severity = row['severity'].strip()  # PASS, WARNING, ERROR
        self.owner = row['owner'].strip()
        
        self.regex = re.compile(self.claim_pattern, re.IGNORECASE | re.MULTILINE)
        self.qualifier_regex = re.compile(self.required_qualifier, re.IGNORECASE | re.MULTILINE) if self.required_qualifier else None

    def matches(self, text: str) -> List[re.Match]:
        return list(self.regex.finditer(text))

    def has_valid_qualifier(self, context_text: str) -> bool:
        if not self.qualifier_regex:
            return True
        return bool(self.qualifier_regex.search(context_text))


class ClaimValidator:
    def __init__(self, registry_path: str):
        self.registry_path = registry_path
        self.rules: List[ClaimRule] = []
        self.load_registry()

    def load_registry(self):
        if not os.path.exists(self.registry_path):
            raise FileNotFoundError(f"Claim registry not found: {self.registry_path}")
        
        with open(self.registry_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('claim_id') and not row['claim_id'].startswith('#'):
                    self.rules.append(ClaimRule(row))

    def is_valid_dynamic_years(self, matched_text: str) -> bool:
        """Check if dynamic years claim (e.g. 30+ 年) is mathematically <= (current_year - 1991)."""
        current_year = datetime.now().year
        max_allowed_years = current_year - FOUNDATION_YEAR  # e.g., 2026 - 1991 = 35
        
        digits = re.findall(r'\d+', matched_text)
        if digits:
            claimed_years = int(digits[0])
            # If claimed years is <= max allowed (e.g. 30 <= 35), it's valid
            return claimed_years <= max_allowed_years
        return True

    def extract_visible_blocks(self, html_content: str) -> Tuple[List[Dict[str, Any]], str]:
        """Parse HTML with BeautifulSoup, strip script/style/noscript, and extract hierarchical text blocks."""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Strip script, style, noscript, template
        for elem in soup(['script', 'style', 'noscript', 'template']):
            elem.decompose()
        
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()
            
        blocks = []
        
        # Extract meaningful tags
        target_tags = ['p', 'li', 'td', 'th', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'div', 'blockquote', 'a']
        
        # Iterate over leaf or small container elements with direct text
        for tag in soup.find_all(target_tags):
            # Only consider tags that have direct text or minimal nested inline tags
            text = tag.get_text(separator=' ', strip=True)
            if not text:
                continue
            
            # Find parent container (e.g. section, article, div)
            parent_container = tag.find_parent(['section', 'article', 'div', 'main'])
            container_text = parent_container.get_text(separator=' ', strip=True) if parent_container else text
            
            # Attempt to get line number if available (bs4 sourceline)
            sourceline = getattr(tag, 'sourceline', 1)
            
            blocks.append({
                'tag_name': tag.name,
                'text': text,
                'container_text': container_text,
                'sourceline': sourceline
            })
            
        return blocks, soup.get_text(separator=' ', strip=True)

    def audit_file(self, file_path: str) -> Dict[str, Any]:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            html_content = f.read()

        blocks, full_visible_text = self.extract_visible_blocks(html_content)
        
        file_findings = []
        claim_counts = {
            'VERIFIED': 0,
            'CONDITIONAL_PASS': 0,
            'WARNING': 0,
            'ERROR': 0
        }
        
        # 1. Check BLOCKED rules FIRST across all visible blocks & full visible text
        blocked_rules = [r for r in self.rules if r.status == 'BLOCKED']
        conditional_rules = [r for r in self.rules if r.status == 'CONDITIONAL']
        verified_rules = [r for r in self.rules if r.status == 'VERIFIED']
        
        checked_blocked_spans = set()
        
        for block in blocks:
            text = block['text']
            line = block['sourceline']
            
            # Step 1: Check BLOCKED Rules
            for rule in blocked_rules:
                matches = rule.matches(text)
                for m in matches:
                    span_key = (line, m.group(0).strip())
                    if span_key not in checked_blocked_spans:
                        checked_blocked_spans.add(span_key)
                        claim_counts['ERROR'] += 1
                        file_findings.append({
                            'level': 'ERROR',
                            'claim_id': rule.claim_id,
                            'claim_type': rule.claim_type,
                            'matched_text': m.group(0),
                            'line': line,
                            'context': text[:180],
                            'reason': f"Blocked claim pattern matched: '{rule.claim_pattern}' ({rule.evidence_source})"
                        })

        # Step 2: Check CONDITIONAL and VERIFIED Rules
        checked_conditional_spans = set()
        checked_verified_spans = set()
        
        for block in blocks:
            text = block['text']
            container_text = block['container_text']
            line = block['sourceline']
            
            # Split text into sentences
            sentences = re.split(r'[。！？\.\!\?]', text)
            
            # A. Check CONDITIONAL Rules
            for rule in conditional_rules:
                matches = rule.matches(text)
                for m in matches:
                    matched_str = m.group(0).strip()
                    span_key = (line, matched_str)
                    if span_key in checked_conditional_spans or span_key in checked_blocked_spans:
                        continue
                    checked_conditional_spans.add(span_key)
                    
                    # Hierarchical Context Check
                    # Level 1: Same sentence
                    matched_sentence = next((s for s in sentences if matched_str in s), text)
                    has_qualifier = rule.has_valid_qualifier(matched_sentence)
                    
                    # Level 2: Same tag block
                    if not has_qualifier:
                        has_qualifier = rule.has_valid_qualifier(text)
                    
                    # Level 3: Same parent container
                    if not has_qualifier:
                        has_qualifier = rule.has_valid_qualifier(container_text)
                    
                    if has_qualifier:
                        claim_counts['CONDITIONAL_PASS'] += 1
                        file_findings.append({
                            'level': 'INFO',
                            'claim_id': rule.claim_id,
                            'claim_type': rule.claim_type,
                            'matched_text': matched_str,
                            'line': line,
                            'context': matched_sentence[:150],
                            'reason': f"Valid qualifier present for conditional claim '{rule.claim_id}'"
                        })
                    else:
                        claim_counts['WARNING'] += 1
                        file_findings.append({
                            'level': 'WARNING',
                            'claim_id': rule.claim_id,
                            'claim_type': rule.claim_type,
                            'matched_text': matched_str,
                            'line': line,
                            'context': text[:150],
                            'reason': f"Missing required qualifier '{rule.required_qualifier}' for conditional claim '{rule.claim_id}'"
                        })
                        
            # B. Check VERIFIED Rules
            for rule in verified_rules:
                matches = rule.matches(text)
                for m in matches:
                    matched_str = m.group(0).strip()
                    span_key = (line, matched_str)
                    if span_key in checked_verified_spans or span_key in checked_blocked_spans:
                        continue
                    checked_verified_spans.add(span_key)
                    
                    # Dynamic year calculation validation
                    if '年' in matched_str or 'Year' in matched_str:
                        if not self.is_valid_dynamic_years(matched_str):
                            claim_counts['WARNING'] += 1
                            file_findings.append({
                                'level': 'WARNING',
                                'claim_id': rule.claim_id,
                                'claim_type': rule.claim_type,
                                'matched_text': matched_str,
                                'line': line,
                                'context': text[:150],
                                'reason': f"Claimed years exceed foundation year math (1991 -> {datetime.now().year})"
                            })
                            continue
                            
                    claim_counts['VERIFIED'] += 1
                    file_findings.append({
                        'level': 'INFO',
                        'claim_id': rule.claim_id,
                        'claim_type': rule.claim_type,
                        'matched_text': matched_str,
                        'line': line,
                        'context': text[:150],
                        'reason': f"Verified fact/capability supported by '{rule.evidence_source}'"
                    })
                    
        return {
            'file': file_path,
            'counts': claim_counts,
            'findings': file_findings
        }

    def audit_directory(self, root_dir: str) -> Dict[str, Any]:
        results = []
        total_counts = {
            'VERIFIED': 0,
            'CONDITIONAL_PASS': 0,
            'WARNING': 0,
            'ERROR': 0
        }
        
        html_files = []
        for root, dirs, files in os.walk(root_dir):
            # Skip node_modules, .git, scratch, .system_generated
            if any(p in root for p in ['.git', 'node_modules', 'scratch', '.system_generated', '.gemini']):
                continue
            for file in files:
                if file.endswith('.html'):
                    html_files.append(os.path.join(root, file))
                    
        for file_path in sorted(html_files):
            res = self.audit_file(file_path)
            results.append(res)
            for k in total_counts:
                total_counts[k] += res['counts'][k]
                
        all_errors = [f for r in results for f in r['findings'] if f['level'] == 'ERROR']
        all_warnings = [f for r in results for f in r['findings'] if f['level'] == 'WARNING']
        all_infos = [f for r in results for f in r['findings'] if f['level'] == 'INFO']
        
        status = 'PASSED' if len(all_errors) == 0 else 'BLOCKED'
        
        return {
            'timestamp': datetime.now().isoformat() + 'Z',
            'files_scanned': len(html_files),
            'status': status,
            'summary': {
                'error_count': len(all_errors),
                'warning_count': len(all_warnings),
                'info_count': len(all_infos),
                'verified_count': total_counts['VERIFIED'],
                'conditional_pass_count': total_counts['CONDITIONAL_PASS']
            },
            'errors': all_errors,
            'warnings': all_warnings,
            'files': results
        }


def print_audit_summary(report: Dict[str, Any]):
    print("\n" + "═" * 70)
    print("        JUN-HSIANG CLAIM AUDIT & PRODUCTION GATE v1.0")
    print("═" * 70)
    print(f" Files Scanned        : {report['files_scanned']} HTML Pages")
    print(f" 🟢 VERIFIED (INFO)   : {report['summary']['verified_count']}")
    print(f" 🟢 QUALIFIED (INFO)  : {report['summary']['conditional_pass_count']}")
    print(f" 🟡 WARNING           : {report['summary']['warning_count']} (Human Review Required)")
    print(f" 🔴 BLOCKED (ERROR)   : {report['summary']['error_count']} (Violation Detected)")
    print("─" * 70)
    
    if report['summary']['error_count'] > 0:
        print(" ❌ Production Gate Status : 🔴 DEPLOY BLOCKED")
        print("\n [ERRORS REQUIRING IMMEDIATE FIX]:")
        for err in report['errors'][:10]:
            print(f"  • Line {err['line']}: [{err['claim_id']}] {err['matched_text']} -> {err['reason']}")
    else:
        print(" ✅ Production Gate Status : 🟢 PASSED")
        print(" 🚀 Deploy Status          : ALLOWED")
        
    if report['summary']['warning_count'] > 0:
        print("\n [WARNINGS FOR AUDIT REVIEW]:")
        for warn in report['warnings'][:10]:
            print(f"  • Line {warn['line']}: [{warn['claim_id']}] {warn['matched_text']} -> {warn['reason']}")
            
    print("═" * 70 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Jun-Hsiang Claim Governance Validator")
    parser.add_argument('--scan-dir', default='.', help="Directory to scan HTML files")
    parser.add_argument('--registry', default='seo_intelligence/claim_registry.csv', help="Path to claim_registry.csv")
    parser.add_argument('--output', default='seo_intelligence/reports/claim_audit_report.json', help="Output report path")
    parser.add_argument('--strict', action='store_true', help="Treat WARNING as failure")
    
    args = parser.parse_args()
    
    base_dir = os.path.abspath(args.scan_dir)
    reg_path = os.path.join(base_dir, args.registry) if not os.path.isabs(args.registry) else args.registry
    out_path = os.path.join(base_dir, args.output) if not os.path.isabs(args.output) else args.output
    
    validator = ClaimValidator(reg_path)
    report = validator.audit_directory(base_dir)
    
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        
    print_audit_summary(report)
    
    if report['summary']['error_count'] > 0:
        sys.exit(1)
    if args.strict and report['summary']['warning_count'] > 0:
        sys.exit(1)
        
    sys.exit(0)


if __name__ == '__main__':
    main()
