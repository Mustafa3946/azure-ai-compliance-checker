from src.compliance_checker import infra_scan, model_audit, tag_policy

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
        print(f"Imported tag_policy module functions: {dir(tag_policy)}")
        tag_results = tag_policy.run_tag_policy_check()
        print(f"Tag policy findings: {tag_results}\n")
        results["tag_policy"] = tag_results
    except Exception as e:
        print(f"Tag policy check failed: {e}")

    return results

if __name__ == "__main__":
    all_results = run_all_checks()
    print("Summary of all compliance checks:")
    print(all_results)
