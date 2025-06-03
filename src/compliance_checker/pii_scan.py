"""
pii_scan.py

Scans text files for Personally Identifiable Information (PII) such as emails, phone numbers,
credit card numbers, and social security numbers using regular expressions.

Functions:
    - scan_text_for_pii: Scans a string for PII patterns.
    - scan_file: Scans a file for PII by reading its contents.
    - perform_pii_scan: Wrapper to scan a default file for PII.
"""

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
    """
    Scans the provided text for PII patterns.
    Returns a dictionary with PII types as keys and lists of matches as values.
    """
    findings = {}
    for label, pattern in PII_PATTERNS.items():
        matches = re.findall(pattern, text)
        findings[label] = matches  # Always include the label, even if no matches
    return findings

def scan_file(file_path: str) -> Dict[str, List[str]]:
    """
    Reads the contents of a file and scans it for PII.
    Raises FileNotFoundError if the file does not exist.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    return scan_text_for_pii(text)

def perform_pii_scan(file_path: str = "data/sample_log.txt") -> Dict[str, List[str]]:
    """
    Wrapper function to perform a PII scan on the specified file.
    Defaults to scanning 'data/sample_log.txt' if no file is provided.
    """
    return scan_file(file_path)

if __name__ == "__main__":
    # Example usage: Run a PII scan on the default file and print results.
    results = perform_pii_scan()
    print("PII Scan Results:")
    for k, v in results.items():
        print(f"{k}: {v}")
