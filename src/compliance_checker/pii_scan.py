import re
import os
from typing import List, Dict

PII_PATTERNS = {
    'email': r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
    'phone': r'\b(?:\+?\d{1,3})?[-.\s]?(?:\(?\d{2,4}\)?)[-.\s]?\d{3,4}[-.\s]?\d{4}\b',
    'credit_card': r'\b(?:\d[ -]*?){13,16}\b',
    'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
}

def scan_text_for_pii(text: str) -> Dict[str, List[str]]:
    findings = {}
    for label, pattern in PII_PATTERNS.items():
        matches = re.findall(pattern, text)
        findings[label] = matches  # Always include the label, even if no matches
    return findings

def scan_file(file_path: str) -> Dict[str, List[str]]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    return scan_text_for_pii(text)
