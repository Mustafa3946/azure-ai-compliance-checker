from typing import List, Dict, Any

def check_required_tags(
    resources: List[Dict[str, Any]],
    required_tags: List[str] = ["env", "owner", "cost_center"]
) -> List[Dict[str, Any]]:
    """
    Checks Azure resources for missing required tags.

    Args:
        resources: List of Azure resource dicts with `tags` key.
        required_tags: List of tags that each resource must have.

    Returns:
        List of dicts for resources missing one or more required tags:
        [
            {
                "resource_name": str,
                "resource_type": str,
                "missing_tags": List[str]
            },
            ...
        ]
    """
    violations = []

    for res in resources:
        tags = res.get("tags", {})
        missing = [tag for tag in required_tags if tag not in tags or not tags[tag]]
        if missing:
            violations.append({
                "resource_name": res.get("name", "unknown"),
                "resource_type": res.get("type", "unknown"),
                "missing_tags": missing
            })
    return violations
