"""
test_tag_policy.py

Unit tests for the tag_policy module.
Tests detection of missing required tags on Azure resources.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from src.compliance_checker.tag_policy import check_required_tags

class TestTagPolicy(unittest.TestCase):
    """
    Test suite for tag_policy module.
    """

    def setUp(self):
        # Sample Azure resources with various tag configurations for testing.
        self.resources = [
            {"name": "vm-prod-1", "type": "Microsoft.Compute/virtualMachines", "tags": {"env": "prod", "owner": "teamA"}},
            {"name": "storage-logs", "type": "Microsoft.Storage/storageAccounts", "tags": {"owner": "teamB"}},
            {"name": "db-backup", "type": "Microsoft.Sql/servers", "tags": {"env": "dev", "cost_center": "1234"}},
            {"name": "vm-unlabeled", "type": "Microsoft.Compute/virtualMachines", "tags": {}},
        ]

    def test_check_required_tags_defaults(self):
        """
        Test that check_required_tags detects missing default tags.
        """
        violations = check_required_tags(self.resources)
        expected = [
            {
                "resource_name": "vm-prod-1",
                "resource_type": "Microsoft.Compute/virtualMachines",
                "missing_tags": ["cost_center"]
            },
            {
                "resource_name": "storage-logs",
                "resource_type": "Microsoft.Storage/storageAccounts",
                "missing_tags": ["env", "cost_center"]
            },
            {
                "resource_name": "db-backup",
                "resource_type": "Microsoft.Sql/servers",
                "missing_tags": ["owner"]
            },
            {
                "resource_name": "vm-unlabeled",
                "resource_type": "Microsoft.Compute/virtualMachines",
                "missing_tags": ["env", "owner", "cost_center"]
            }
        ]
        self.assertEqual(violations, expected)

    def test_check_required_tags_custom(self):
        """
        Test that check_required_tags works with custom required tags.
        """
        custom_required = ["project", "department"]
        violations = check_required_tags(self.resources, custom_required)
        # All resources missing both custom tags
        self.assertEqual(len(violations), 4)
        for v in violations:
            self.assertListEqual(v["missing_tags"], custom_required)

if __name__ == "__main__":
    unittest.main()
