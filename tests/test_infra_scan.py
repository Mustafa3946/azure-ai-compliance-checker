"""
test_infra_scan.py

Unit tests for the infra_scan module.
Tests infrastructure compliance scanning and report saving functionality.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import unittest
from unittest.mock import patch, mock_open
from src.compliance_checker import infra_scan


class TestInfraScan(unittest.TestCase):
    """
    Test suite for infra_scan module.
    """

    def setUp(self):
        # Set up a test output file for report saving tests.
        self.test_output_file = "test_infra_report.json"

    def tearDown(self):
        # Clean up the test output file after each test.
        if os.path.exists(self.test_output_file):
            os.remove(self.test_output_file)

    @patch("src.compliance_checker.infra_scan.fetch_azure_resources")
    def test_scan_for_compliance_output_structure(self, mock_fetch):
        """
        Test that scan_for_compliance returns the expected report structure and values.
        """
        # Mock Azure resources
        mock_fetch.return_value = [
            {"name": "vm-test", "type": "Microsoft.Compute/virtualMachines", "tags": {}},
            {"name": "vm-prod", "type": "Microsoft.Compute/virtualMachines", "tags": {"env": "prod"}},
        ]
        report = infra_scan.scan_for_compliance()
        self.assertIsInstance(report, dict)
        self.assertIn("summary", report)
        self.assertIn("non_compliant_resources", report)
        self.assertEqual(report["summary"]["total"], 2)
        self.assertEqual(report["summary"]["non_compliant"], 1)

    def test_save_report_creates_file(self):
        """
        Test that save_report creates a file and writes the report correctly.
        """
        mock_report = {
            "summary": {"total": 1, "non_compliant": 1},
            "non_compliant_resources": [
                {"resource_name": "test", "resource_type": "vm", "issues": ["No env tag"]}
            ]
        }
        infra_scan.save_report(mock_report, self.test_output_file)
        self.assertTrue(os.path.exists(self.test_output_file))
        with open(self.test_output_file, 'r') as file:
            content = json.load(file)
        self.assertEqual(content, mock_report)

    @patch("src.compliance_checker.infra_scan.open", new_callable=mock_open)
    def test_save_report_calls_open(self, mock_file):
        """
        Test that save_report calls open with the correct arguments.
        """
        mock_report = {"summary": {}, "non_compliant_resources": []}
        infra_scan.save_report(mock_report, self.test_output_file)
        mock_file.assert_called_with(self.test_output_file, 'w')

if __name__ == '__main__':
    unittest.main()
