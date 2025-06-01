## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Architecture Overview](#architecture-overview)
- [Folder Structure](#folder-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Testing](#testing)
- [Documentation](#documentation)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

# azure-ai-compliance-checker

An Azure-powered, agentic compliance checker leveraging AI-driven automation and Infrastructure as Code. Demonstrates integration of Azure AI services, Terraform, Ansible, and GitOps to support secure and scalable AI operations aligned with enterprise governance and regulatory requirements.

---

## Project Overview

This project showcases an **agentic AI system** built to operate autonomously within Azure environments to ensure AI infrastructure compliance, security, and governance. It features an LLM-powered agent that orchestrates scans, audits, and policy evaluations across Infrastructure as Code, model governance metadata, and runtime environments.

Leveraging tools like **Azure OpenAI**, **Azure Machine Learning**, **Terraform**, and **Ansible**, the solution supports:

- Autonomous compliance gap detection
- Responsible AI governance checks (e.g., drift, fairness, explainability)
- Regulatory alignment (e.g., APRA CPS 234, Microsoft Responsible AI)
- Scalable and cost-efficient automation using GitOps best practices

---

## Features

- **Infrastructure Scan:** Detect misconfigurations such as public storage, untagged resources, and expired certificates.
- **AI Model Governance Check:** Evaluate AI models for drift, bias, explainability, and fairness using metadata.
- **Audit Log Analysis:** Identify potentially non-compliant data transfers and sensitive data exposures in logs.
- **Reporting:** Generate summary compliance reports aligned with APRA CPS 234 and Responsible AI guidelines.
- **Agentic AI Assistant:** An interactive assistant to guide users through compliance checks and recommendations.

---
### Model Fairness Audit

This tool uses `fairlearn` and `scikit-learn` to assess bias in ML models. It computes:
- Demographic Parity Difference
- Equalized Odds Difference
- Selection Rate by Group

Example usage:

```bash
python src/compliance_checker/model_audit.py

---

## Technology Stack

- **Azure Services:** Azure CLI, Azure Storage SDK (locally simulated or minimal usage), Azure OpenAI (optional for agentic AI features)
- **Infrastructure as Code:** Terraform and Ansible (demonstrated via templates and scripts)
- **DevOps Tools:** Git for version control, basic CI/CD scripts (optional)
- **Programming:** Python for compliance checks, report generation, and agentic AI orchestration
- **AI and Analytics:** Local model explainability/bias checks, minimal Azure AI service calls to reduce cost

---

## Architecture Overview

```
+---------------------+         +---------------------+         +---------------------+
|  User / Developer   | <-----> |  Agentic AI System  | <-----> |   Azure Services    |
+---------------------+         +---------------------+         +---------------------+
         |                               |                               |
         |                               |                               |
         v                               v                               v
+---------------------+   +---------------------------+   +---------------------------+
|  CLI / Assistant    |   | Compliance Check Modules  |   |   Infra as Code (IaC)     |
|  (agentic_ai.py)    |   | - infra_scan.py           |   |   - Terraform             |
+---------------------+   | - model_audit.py          |   |   - Ansible               |
                          | - pii_scan.py             |   +---------------------------+
                          | - tag_policy.py           |           |
                          +---------------------------+           v
                                   |                        +---------------------+
                                   v                        |   Azure Resources   |
                          +---------------------------+     +---------------------+
                          |    Report Generation      |
                          |    (report.py)            |
                          +---------------------------+
                                   |
                                   v
                          +---------------------------+
                          |   Compliance Reports      |
                          |   (data/results/)         |
                          +---------------------------+
```

---

## Folder Structure

```bash
azure-ai-compliance-checker/
├── data/
│   ├── config/
│   └── results/
├── src/
│   ├── compliance_checker/
│   │   ├── __init__.py
│   │   ├── infra_scan.py
│   │   ├── model_audit.py
│   │   ├── pii_scan.py
│   │   ├── report.py
│   │   ├── tag_policy.py
│   │   └── utils.py
├── tests/
│   ├── test_infra_scan.py
│   ├── test_model_audit.py
│   ├── test_pii_scan.py
│   ├── test_tag_policy.py
│   └── test_report.py
├── infra/
│   ├── terraform/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── ansible/
│       └── deploy.yml
├── notebooks/
│   └── model_fairness_analysis.ipynb
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- Terraform and Ansible installed (for IaC templates)
- Git
- (Optional) Azure CLI configured with minimal Azure subscription access
- (Optional) Azure OpenAI access for enhanced agentic AI capabilities

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Mustafa3946/azure-ai-compliance-checker.git
    cd azure-ai-compliance-checker
    ```

2. Create a virtual environment and install dependencies:

    ```bash
    python -m venv .venv
    # Activate virtual environment:
    # On Linux/macOS:
    source .venv/bin/activate
    # On Windows PowerShell:
    .\.venv\Scripts\Activate.ps1
    # On Windows cmd:
    .\.venv\Scripts\activate.bat

    pip install -r requirements.txt
    ```

---

## Usage

Run the compliance checks individually or via the interactive agentic AI assistant:

```bash
python src/compliance_checker/agentic_ai.py
```

You will be presented with a menu:

```
Please choose an option:
1. Run Infrastructure Scan
2. Run AI Model Governance Audit
3. Run PII Data Exposure Scan
4. Generate Compliance Report
5. Exit
Enter choice [1-5]:
```

Enter the number corresponding to your choice and follow the prompts.

The compliance report will be generated in `data/results/` and will look like this:

```markdown
# Compliance Report Summary

## Infrastructure Scan

- Total Resources Scanned: 4
- Non-Compliant Resources: 2

### Non-Compliant Resources
- **storage-logs** (Microsoft.Storage/storageAccounts):
  - Missing 'env' tag
- **vm-unlabeled** (Microsoft.Compute/virtualMachines):
  - Missing 'env' tag

## AI Model Governance Audit

- Model may be outdated (drift risk).
- Possible model bias detected in precision/recall across groups.
- Explainability tools not documented for this model.

## PII Data Exposure Scan

- **Email**:
  - john.doe@example.com
- **Phone**:
  - 4111 1111 1111
- **Credit_card**:
  - 4111 1111 1111 1111
- **Ssn**:
  - 123-45-6789
```

---

## Testing

Run unit tests with:

```bash
pytest tests/
```

---

## Documentation

Refer to detailed design and as-built documentation in the `docs/` folder (to be added).

---

## Roadmap

Planned enhancements:

- Integration with Azure DevOps pipelines for automated scanning
- Enhanced AI governance checks with Azure Machine Learning SDK
- Web-based dashboard for compliance visualization
- Full Azure resource scanning using Azure SDKs with proper authentication

---

## License

This project is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/).

You may:
- Share, remix, and adapt the work, as long as it's for **non-commercial purposes only**.

You may not:
- Use this work for **commercial purposes**, including resale or profit-driven uses, without explicit permission from the author.

**Note:**  
The `llama-2-7b.Q4_K_M.gguf` model file is **not included** in this repository.  
You can download it from [Hugging Face](https://huggingface.co/) or the official Llama 2 release, and place it in the `models/` directory.

![Python](https://img.shields.io/badge/python-3.8%2B-blue)