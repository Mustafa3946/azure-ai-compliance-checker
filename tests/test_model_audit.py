"""
test_model_audit.py

Unit tests for the model_audit module.
Tests model drift detection, bias detection, explainability checks, and overall audit logic.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from datetime import datetime, timedelta
from src.compliance_checker.model_audit import (
    check_model_drift,
    check_model_bias,
    check_model_explainability,
    audit_model,
    run_model_audit
)

class TestModelAudit(unittest.TestCase):
    """
    Test suite for model_audit module.
    """

    def test_check_model_drift_recent_model(self):
        """
        Test that a recently trained model is not flagged as drifted.
        """
        recent_date = (datetime.now() - timedelta(days=10)).isoformat()
        metadata = {"last_trained": recent_date}
        self.assertFalse(check_model_drift(metadata))

    def test_check_model_drift_old_model(self):
        """
        Test that an old model is flagged as drifted.
        """
        old_date = (datetime.now() - timedelta(days=60)).isoformat()
        metadata = {"last_trained": old_date}
        self.assertTrue(check_model_drift(metadata))

    def test_check_model_drift_missing_date(self):
        """
        Test that missing last_trained date is treated as drifted.
        """
        metadata = {}
        self.assertTrue(check_model_drift(metadata))

    def test_check_model_bias_no_bias(self):
        """
        Test that similar precision metrics do not trigger bias detection.
        """
        metrics = {"precision_group_A": 0.91, "precision_group_B": 0.88}
        self.assertFalse(check_model_bias(metrics))

    def test_check_model_bias_detected(self):
        """
        Test that a large difference in precision metrics triggers bias detection.
        """
        metrics = {"precision_group_A": 0.91, "precision_group_B": 0.75}
        self.assertTrue(check_model_bias(metrics))

    def test_check_model_explainability_present(self):
        """
        Test that presence of explainability tools is not flagged as missing.
        """
        metadata = {"explainability_tools": ["SHAP"]}
        self.assertFalse(check_model_explainability(metadata))

    def test_check_model_explainability_missing(self):
        """
        Test that missing explainability tools is flagged.
        """
        metadata = {"explainability_tools": []}
        self.assertTrue(check_model_explainability(metadata))

    def test_audit_model_with_issues(self):
        """
        Test that audit_model returns all expected issues for a non-compliant model.
        """
        metadata = {
            "last_trained": (datetime.now() - timedelta(days=90)).isoformat(),
            "metrics": {"precision_group_A": 0.9, "precision_group_B": 0.7},
            "explainability_tools": []
        }
        issues = audit_model(metadata)
        self.assertEqual(len(issues), 3)

    def test_audit_model_compliant(self):
        """
        Test that audit_model returns no issues for a compliant model.
        """
        metadata = {
            "last_trained": (datetime.now() - timedelta(days=5)).isoformat(),
            "metrics": {"precision_group_A": 0.9, "precision_group_B": 0.89},
            "explainability_tools": ["SHAP", "LIME"]
        }
        issues = audit_model(metadata)
        self.assertEqual(issues, [])

    def test_run_model_audit(self):
        """
        Test that run_model_audit returns at least one issue for the demo model.
        """
        issues = run_model_audit()
        self.assertTrue(len(issues) >= 1)
        self.assertIn("Model may be outdated (drift risk).", issues)

if __name__ == "__main__":
    unittest.main()
