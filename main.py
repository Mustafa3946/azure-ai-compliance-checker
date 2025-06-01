from src.compliance_checker import infra_scan, model_audit, tag_policy, pii_scan, report

def run_all_checks():
    results = {}

    try:
        print("Running infrastructure scan...")
        infra_results = infra_scan.scan_for_compliance()
        print(f"Infrastructure findings: {infra_results}\n")
        results["infrastructure"] = infra_results
    except Exception as e:
        print(f"Infrastructure scan failed: {e}")

    try:
        print("Running model governance audit...")
        model_results = model_audit.run_model_audit()
        print(f"Model audit findings: {model_results}\n")
        results["model_audit"] = model_results
    except Exception as e:
        print(f"Model audit failed: {e}")

    try:
        print("Running tag policy check...")
        tag_results = tag_policy.run_tag_policy_check()
        print(f"Tag policy findings: {tag_results}\n")
        results["tag_policy"] = tag_results
    except Exception as e:
        print(f"Tag policy check failed: {e}")

    try:
        print("Running PII log scan...")
        pii_results = pii_scan.scan_file("data/sample_log.txt")
        print(f"PII scan findings: {pii_results}\n")
        results["pii_scan"] = pii_results
    except Exception as e:
        print(f"PII scan failed: {e}")

    return results

if __name__ == "__main__":
    all_results = run_all_checks()
    print("Summary of all compliance checks:")
    print(all_results)

    # Generate report file
    report.generate_markdown_report(all_results)
