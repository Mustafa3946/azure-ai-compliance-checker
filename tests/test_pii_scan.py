import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tempfile
from src.compliance_checker.pii_scan import scan_file

def test_pii_scan_detects_nothing_in_clean_file():
    content = "This is a clean log with no PII."
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
        temp_file.write(content)
        temp_file_path = temp_file.name

    result = scan_file(temp_file_path)

    os.remove(temp_file_path)

    expected_result = {
        'email': [],
        'ssn': [],
        'phone': [],
        'credit_card': []
    }
    assert result == expected_result

def test_pii_scan_detects_email_and_ssn():
    content = "Email: jane.doe@company.com\nSSN: 111-22-3333\nNothing sensitive here."
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
        temp_file.write(content)
        temp_file_path = temp_file.name

    result = scan_file(temp_file_path)

    os.remove(temp_file_path)

    assert 'email' in result
    assert 'ssn' in result
    assert 'jane.doe@company.com' in result['email']
    assert '111-22-3333' in result['ssn']
