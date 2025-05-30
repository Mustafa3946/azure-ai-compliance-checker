import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from datetime import datetime, timedelta
from src.compliance_checker.model_audit import (
    check_model_drift,
    check_model_bias,
    check_model_explainability,
    audit_model
)

class TestModelAudit(unittest.TestCase):

    def test_check_model_drift_recent_model(self):
        recent_date = (datetime.now() - timedelta(days=10)).isoformat()
        metadata = {"last_trained": recent_date}
        self.assertFalse(check_model_drift(metadata))

    def test_check_model_drift_old_model(self):
        old_date = (datetime.now() - timedelta(days=60)).isoformat()
        metadata = {"last_trained": old_date}
        self.assertTrue(check_model_drift(metadata))

    def test_check_model_drift_missing_date(self):
        metadata = {}
        self.assertTrue(check_model_drift(metadata))

    def test_check_model_bias_no_bias(self):
        metrics = {"precision_group_A": 0.91, "precision_group_B": 0.88}
        self.assertFalse(check_model_bias(metrics))

    def test_check_model_bias_detected(self):
        metrics = {"precision_group_A": 0.91, "precision_group_B": 0.75}
        self.assertTrue(check_model_bias(metrics))

    def test_check_model_explainability_present(self):
        metadata = {"explainability_tools": ["SHAP"]}
        self.assertFalse(check_model_explainability(metadata))

    def test_check_model_explainability_missing(self):
        metadata = {"explainability_tools": []}
        self.assertTrue(check_model_explainability(metadata))

    def test_audit_model_with_issues(self):
        metadata = {
            "last_trained": (datetime.now() - timedelta(days=90)).isoformat(),
            "metrics": {"precision_group_A": 0.9, "precision_group_B": 0.7},
            "explainability_tools": []
        }
        issues = audit_model(metadata)
        self.assertEqual(len(issues), 3)

    def test_audit_model_compliant(self):
        metadata = {
            "last_trained": (datetime.now() - timedelta(days=5)).isoformat(),
            "metrics": {"precision_group_A": 0.9, "precision_group_B": 0.89},
            "explainability_tools": ["SHAP", "LIME"]
        }
        issues = audit_model(metadata)
        self.assertEqual(issues, [])

if __name__ == "__main__":
    unittest.main()
