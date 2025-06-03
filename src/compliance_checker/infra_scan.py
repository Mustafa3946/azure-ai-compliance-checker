"""
infra_scan.py

Performs Azure infrastructure compliance scanning using Azure SDK and CLI credentials.
Fetches resources, checks for compliance issues (e.g., missing tags), and generates summary reports.
"""

from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
from typing import List, Dict, Any
import json
import os

def get_subscription_id() -> str:
    """
    Returns the current Azure subscription ID using the Azure CLI.
    """
    import subprocess
    result = subprocess.run(
        "az account show --query id -o tsv",
        capture_output=True,
        text=True,
        shell=True  # Required for Windows to find 'az'
    )
    return result.stdout.strip()

def fetch_azure_resources() -> List[Dict[str, Any]]:
    """
    Fetches all resources in the current Azure subscription using Azure SDK.
    Returns a list of resource dictionaries with name, type, and tags.
    """
    subscription_id = get_subscription_id()
    credential = AzureCliCredential()
    resource_client = ResourceManagementClient(credential, subscription_id)

    resources = []
    for item in resource_client.resources.list():
        resources.append({
            "name": item.name,
            "type": item.type,
            "tags": item.tags or {}
        })
    return resources

def scan_resources(resources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Scans a list of Azure resources for compliance issues.
    Returns a list of non-compliant resources with detected issues.
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

def generate_summary_report(issues: List[Dict[str, Any]], total: int) -> Dict[str, Any]:
    """
    Generates a summary report dictionary from the list of issues and total resources scanned.
    """
    return {
        "summary": {
            "total": total,
            "non_compliant": len(issues),
        },
        "non_compliant_resources": issues,
    }

def scan_for_compliance() -> Dict[str, Any]:
    """
    Runs the full compliance scan: fetches resources, scans for issues, and returns a summary report.
    """
    resources = fetch_azure_resources()
    issues = scan_resources(resources)
    return generate_summary_report(issues, total=len(resources))

def save_report(report: Dict[str, Any], filepath: str = "data/results/infra_scan_report.json") -> None:
    """
    Saves the compliance report to a JSON file at the specified filepath.
    """
    dir_path = os.path.dirname(filepath)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(report, f, indent=2)

def run_scan() -> None:
    """
    Runs the compliance scan and saves the report to the default location.
    """
    report = scan_for_compliance()
    save_report(report)

if __name__ == "__main__":
    run_scan()
