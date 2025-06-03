import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import json
from datetime import datetime

from compliance_checker.infra_scan import scan_for_compliance
from compliance_checker.model_audit import run_model_audit as audit_model_check
from compliance_checker.pii_scan import perform_pii_scan
from compliance_checker.report import generate_html_report  # <-- new import

def run_infra_scan():
    print("Running Infrastructure Scan...")
    time.sleep(1)
    results = scan_for_compliance()
    print("Infrastructure Scan completed.")
    return {"infra_scan": results}

def run_model_audit_wrapper():
    print("Running AI Model Governance Audit...")
    time.sleep(1)
    results = audit_model_check()
    print("Model Audit completed.")
    return {"model_audit": results}

def run_pii_scan():
    print("Running PII Data Exposure Scan...")
    time.sleep(1)
    results = perform_pii_scan()
    print("PII Scan completed.")
    return {"pii_scan": results}

def generate_report(results):
    print("\nGenerating compliance report...")
    time.sleep(1)
    print("=== Compliance Report Summary ===")
    for check, status in results.items():
        print(f"{check}: {status}")
    print("==============================\n")

def export_report_to_file(results):
    if not results:
        print("No scan results available to export.")
        return

    filename = f"compliance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    folder_path = os.path.join("data", "results")
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, filename)

    with open(file_path, "w") as f:
        json.dump(results, f, indent=4)

    print(f"Compliance JSON report saved to {file_path}")

def export_report_to_markdown(results):
    if not results:
        print("No scan results available to export.")
        return

    filename = f"compliance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    folder_path = os.path.join("data", "results")
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, filename)

    with open(file_path, "w") as f:
        f.write("# Compliance Report Summary\n\n")

        infra = results.get('infra_scan', {})
        f.write("## Infrastructure Scan\n\n")
        summary = infra.get('summary', {})
        f.write(f"- Total Resources Scanned: {summary.get('total', 0)}\n")
        f.write(f"- Non-Compliant Resources: {summary.get('non_compliant', 0)}\n\n")

        if infra.get('non_compliant_resources'):
            f.write("### Non-Compliant Resources\n")
            for resource in infra['non_compliant_resources']:
                f.write(f"- **{resource['resource_name']}** ({resource['resource_type']}):\n")
                for issue in resource['issues']:
                    f.write(f"  - {issue}\n")
            f.write("\n")

        model_audit = results.get('model_audit', [])
        f.write("## AI Model Governance Audit\n\n")
        if model_audit:
            for issue in model_audit:
                f.write(f"- {issue}\n")
        else:
            f.write("No issues detected.\n")
        f.write("\n")

        pii_scan = results.get('pii_scan', {})
        f.write("## PII Data Exposure Scan\n\n")
        if any(pii_scan.values()):
            for pii_type, items in pii_scan.items():
                if items:
                    f.write(f"- **{pii_type.capitalize()}**:\n")
                    for item in items:
                        f.write(f"  - {item}\n")
        else:
            f.write("No PII detected.\n")

    print(f"Compliance Markdown report saved to {file_path}")

def main():
    print("Welcome to the Azure AI Compliance Checker Assistant (Local Demo)")
    results = {}

    while True:
        print("\nPlease choose an option:")
        print("1. Run Infrastructure Scan")
        print("2. Run AI Model Governance Audit")
        print("3. Run PII Data Exposure Scan")
        print("4. Generate Compliance Report")
        print("5. Exit")

        choice = input("Enter choice [1-5]: ").strip()

        if choice == "1":
            results.update(run_infra_scan())
        elif choice == "2":
            results.update(run_model_audit_wrapper())
        elif choice == "3":
            results.update(run_pii_scan())
        elif choice == "4":
            if results:
                generate_report(results)
                while True:
                    save_choice = input("Save report to file? (y/n): ").strip().lower()
                    if save_choice == 'y':
                        export_report_to_file(results)
                        export_report_to_markdown(results)
                        generate_html_report(results)  # <-- generate HTML here
                        break
                    elif save_choice == 'n':
                        break
                    else:
                        print("Please enter 'y' or 'n'.")
            else:
                print("No scan results available. Please run scans first.")
        elif choice == "5":
            print("Exiting assistant. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
