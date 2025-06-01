import datetime
from typing import Dict, List, Any


def check_model_drift(model_metadata: Dict[str, Any], threshold_days: int = 30) -> bool:
    """
    Checks whether the model may be outdated (i.e., drift risk) based on last training date.

    Args:
        model_metadata: Dictionary with 'last_trained' (ISO 8601 string)
        threshold_days: Number of days to consider before flagging drift risk

    Returns:
        True if drift risk is detected, False otherwise
    """
    last_trained = model_metadata.get("last_trained")
    if not last_trained:
        return True  # Assume risk if metadata is missing

    try:
        last_trained_date = datetime.datetime.fromisoformat(last_trained)
        days_since_train = (datetime.datetime.now() - last_trained_date).days
        return days_since_train > threshold_days
    except Exception:
        return True  # Assume risk if format is invalid


def check_model_bias(metrics: Dict[str, float], bias_threshold: float = 0.1) -> bool:
    """
    Checks for potential bias by comparing precision or recall across groups.

    Args:
        metrics: Dictionary like {'precision_group_A': 0.91, 'precision_group_B': 0.75}
        bias_threshold: Absolute difference threshold to flag bias

    Returns:
        True if possible bias detected, False otherwise
    """
    precision_values = [
        v for k, v in metrics.items() if "precision" in k.lower()
    ]
    if len(precision_values) < 2:
        return False  # Not enough data to determine bias

    max_diff = max(precision_values) - min(precision_values)
    return max_diff > bias_threshold


def check_model_explainability(metadata: Dict[str, Any]) -> bool:
    """
    Checks whether model explainability tools were used (e.g., SHAP, LIME)

    Args:
        metadata: Dictionary with keys like 'explainability_tools': ['SHAP', ...]

    Returns:
        True if explainability missing, False if explainability is present
    """
    tools = metadata.get("explainability_tools", [])
    return not tools  # True means explainability is missing


def audit_model(model_metadata: Dict[str, Any]) -> List[str]:
    """
    Runs all audit checks and returns list of compliance issues.

    Args:
        model_metadata: Metadata dict with model info

    Returns:
        List of string messages indicating audit failures
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
    # Demo model metadata (can be replaced by actual file/parsing later)
    example_model = {
        "last_trained": "2024-11-15T12:00:00",
        "metrics": {
            "precision_group_A": 0.90,
            "precision_group_B": 0.75
        },
        "explainability_tools": []  # e.g., ["SHAP"]
    }

    return audit_model(example_model)
