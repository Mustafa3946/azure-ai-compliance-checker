import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.compliance_checker import report

TEST_REPORT_PATH = "data/results/test_compliance_report.md"

@pytest.fixture
def sample_findings():
    return {
        "infrastructure": {
            "summary": {"total": 2, "non_compliant": 1},
            "non_compliant_resources": [
                {"resource_name": "test-storage", "resource_type": "Microsoft.Storage/storageAccounts", "issues": ["Missing tag"]}
            ],
        },
        "model_audit": [
            "Possible model bias detected.",
            "Explainability tools not documented."
        ],
        "tag_policy": [
            {"resource_name": "test-storage", "missing_tags": ["env", "owner"]}
        ],
        "pii_scan": {
            "email": ["test@example.com"],
            "phone": [],
            "credit_card": [],
            "ssn": []
        }
    }

def test_generate_markdown_report_creates_file(sample_findings):
    report.generate_markdown_report(sample_findings, output_path=TEST_REPORT_PATH)
    assert os.path.exists(TEST_REPORT_PATH)
    with open(TEST_REPORT_PATH, "r") as f:
        content = f.read().lower()
    assert "# compliance report" in content
    assert "infrastructure" in content
    assert "model_audit" in content  # underscore, not space
    assert "tag_policy" in content
    assert "pii_scan" in content
    assert "test-storage" in content
    assert "test@example.com" in content
    os.remove(TEST_REPORT_PATH)

def test_generate_markdown_report_handles_empty_findings():
    empty_findings = {}
    # Provide an output path so file is written
    test_path = "data/results/test_empty_report.md"
    report.generate_markdown_report(empty_findings, output_path=test_path)
    assert os.path.exists(test_path)
    with open(test_path, "r") as f:
        content = f.read().lower()
    assert "# compliance report" in content
    os.remove(test_path)
