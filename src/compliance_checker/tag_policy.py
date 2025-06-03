"""
tag_policy.py

Checks Azure resources for compliance with required tagging policies.
Identifies resources missing required tags such as 'env', 'owner', or 'cost_center'.

Functions:
    - check_required_tags: Checks a list of resources for missing required tags.
    - run_tag_policy_check: Example/demo function to run the tag policy check on sample data.
"""

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

def run_tag_policy_check() -> List[Dict[str, Any]]:
    """
    Runs the tag policy check on example resource data.
    Replace sample_resources with real resource fetching for production use.

    Returns:
        List of resources missing required tags.
    """
    print("DEBUG: run_tag_policy_check called")
    sample_resources = [
        {"name": "storage-logs", "type": "Microsoft.Storage/storageAccounts", "tags": {"owner": "teamA"}},
        {"name": "vm-unlabeled", "type": "Microsoft.Compute/virtualMachines", "tags": {}},
        {"name": "db-prod", "type": "Microsoft.SQL/servers/databases", "tags": {"env": "prod", "owner": "teamB", "cost_center": "1234"}},
    ]
    violations = check_required_tags(sample_resources)
    return violations

