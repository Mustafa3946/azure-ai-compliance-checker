"""
model_audit.py

Performs AI model governance audits and fairness analysis.
Includes checks for model drift, bias, and explainability using metadata,
and demonstrates fairness metrics computation using Fairlearn and scikit-learn.

Functions:
    - check_model_drift: Checks if a model is outdated based on last training date.
    - check_model_bias: Checks for bias in model precision metrics across groups.
    - check_model_explainability: Checks if explainability tools are documented.
    - audit_model: Aggregates audit issues for a given model's metadata.
    - run_model_audit: Runs a demo audit on example model metadata.
    - run_fairness_analysis: Runs a fairness audit using Fairlearn on a sample dataset.
"""

import datetime
from typing import Dict, List, Any, Optional

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from fairlearn.metrics import MetricFrame, selection_rate, demographic_parity_difference, equalized_odds_difference
from fairlearn.datasets import fetch_adult


def check_model_drift(model_metadata: Dict[str, Any], threshold_days: int = 30) -> bool:
    """
    Determines if the model is outdated based on the last training date.
    Returns True if the model is considered to have drifted.
    """
    last_trained = model_metadata.get("last_trained")
    if not last_trained:
        return True

    try:
        last_trained_date = datetime.datetime.fromisoformat(last_trained)
        days_since_train = (datetime.datetime.now() - last_trained_date).days
        return days_since_train > threshold_days
    except Exception:
        return True


def check_model_bias(metrics: Dict[str, float], bias_threshold: float = 0.1) -> bool:
    """
    Checks for bias in model precision metrics across groups.
    Returns True if the difference exceeds the bias threshold.
    """
    precision_values = [
        v for k, v in metrics.items() if "precision" in k.lower()
    ]
    if len(precision_values) < 2:
        return False

    max_diff = max(precision_values) - min(precision_values)
    return max_diff > bias_threshold


def check_model_explainability(metadata: Dict[str, Any]) -> bool:
    """
    Checks if explainability tools are documented in the model metadata.
    Returns True if no tools are listed.
    """
    tools = metadata.get("explainability_tools", [])
    return not tools


def audit_model(model_metadata: Dict[str, Any]) -> List[str]:
    """
    Aggregates audit issues for a given model's metadata.
    Returns a list of issue descriptions.
    """
    issues = []

    if check_model_drift(model_metadata):
        issues.append("Model may be outdated (drift risk).")

    if check_model_bias(model_metadata.get("metrics", {})):
        issues.append("Possible model bias detected in precision/recall across groups.")

    if check_model_explainability(model_metadata):
        issues.append("Explainability tools not documented for this model.")

    return issues


def run_model_audit() -> List[str]:
    """
    Runs a demo model audit using placeholder metadata.
    Returns:
        List of audit issue strings
    """
    example_model = {
        "last_trained": "2024-11-15T12:00:00",
        "metrics": {
            "precision_group_A": 0.90,
            "precision_group_B": 0.75
        },
        "explainability_tools": []  # e.g., ["SHAP"]
    }

    return audit_model(example_model)


def run_fairness_analysis(use_fairlearn_demo: bool = True) -> Optional[Dict[str, Any]]:
    """
    Runs a fairness audit using Fairlearn on a sample dataset.
    Returns a dictionary of fairness metrics or None if skipped or failed.
    """
    try:
        if not use_fairlearn_demo:
            return None

        data = fetch_adult(as_frame=True)
        X = data.data.drop(columns=["education-num"])
        y = (data.target == ">50K").astype(int)

        sensitive_feature = X["sex"]
        X = pd.get_dummies(X.drop(columns=["sex", "native-country", "race", "workclass", "marital-status", "occupation"]), drop_first=True)

        X_train, X_test, y_train, y_test, sf_train, sf_test = train_test_split(
            X, y, sensitive_feature, test_size=0.3, random_state=42
        )

        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        frame = MetricFrame(metrics={"selection_rate": selection_rate},
                            y_true=y_test, y_pred=y_pred, sensitive_features=sf_test)

        dp_diff = demographic_parity_difference(y_test, y_pred, sensitive_features=sf_test)
        eo_diff = equalized_odds_difference(y_test, y_pred, sensitive_features=sf_test)

        return {
            "selection_rate_by_group": frame.by_group.to_dict(),
            "demographic_parity_difference": dp_diff,
            "equalized_odds_difference": eo_diff
        }

    except Exception as e:
        print(f"Fairness analysis failed: {e}")
        return None


if __name__ == "__main__":
    # Demo: Run metadata-based model audit
    print("=== Metadata-Based Model Audit ===")
    issues = run_model_audit()
    for issue in issues:
        print(f"- {issue}")

    # Demo: Run Fairlearn-based fairness analysis
    print("\n=== Fairlearn-Based Fairness Analysis ===")
    fairness_metrics = run_fairness_analysis()
    if fairness_metrics:
        print(f"Selection Rate by Group: {fairness_metrics['selection_rate_by_group']}")
        print(f"Demographic Parity Difference: {fairness_metrics['demographic_parity_difference']:.3f}")
        print(f"Equalized Odds Difference: {fairness_metrics['equalized_odds_difference']:.3f}")
    else:
        print("Fairness audit not performed.")
