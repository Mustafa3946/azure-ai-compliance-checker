import json
from typing import Dict, Any, List

# Mock definitions simulating Azure SDK results
MOCK_AZURE_RESOURCES = [
    {"name": "vm-prod-1", "type": "Microsoft.Compute/virtualMachines", "tags": {"env": "prod"}},
    {"name": "storage-logs", "type": "Microsoft.Storage/storageAccounts", "tags": {}},
    {"name": "db-backup", "type": "Microsoft.Sql/servers", "tags": {"env": "dev"}},
    {"name": "vm-unlabeled", "type": "Microsoft.Compute/virtualMachines", "tags": {}},
]

def scan_resources(resources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Scans a list of Azure resources for common misconfiguration patterns.
    Currently checks for:
      - Missing tags (e.g., 'env')
    Returns a list of issues found per resource.
    """
    issues = []
    for res in resources:
        res_issues = []
        if not res.get("tags") or not res["tags"].get("env"):
            res_issues.append("Missing 'env' tag")
        if res_issues:
            issues.append({
                "resource_name": res["name"],
                "resource_type": res["type"],
                "issues": res_issues
            })
    return issues

def generate_summary_report(issues: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Builds a summary report from a list of issues.
    """
    return {
        "summary": {
            "total": len(MOCK_AZURE_RESOURCES),
            "non_compliant": len(issues),
        },
        "non_compliant_resources": issues,
    }

def scan_for_compliance() -> Dict[str, Any]:
    """
    Public interface to perform a scan and return a full compliance report.
    This is the function expected by unit tests.
    """
    issues = scan_resources(MOCK_AZURE_RESOURCES)
    report = generate_summary_report(issues)
    return report

def save_report(report: Dict[str, Any], filepath: str = "data/results/infra_scan_report.json") -> None:
    """
    Saves the compliance report to a JSON file.
    """
    with open(filepath, "w") as f:
        json.dump(report, f, indent=2)

def run_scan() -> None:
    """
    Main CLI entrypoint for scanning and saving results.
    """
    report = scan_for_compliance()
    save_report(report)

if __name__ == "__main__":
    run_scan()
