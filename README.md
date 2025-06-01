# azure-ai-compliance-checker

An Azure-powered, agentic compliance checker leveraging AI-driven automation and Infrastructure as Code. Demonstrates integration of Azure AI services, Terraform, Ansible, and GitOps to support secure and scalable AI operations aligned with enterprise governance and regulatory requirements.

## Project Overview

This project showcases an **agentic AI system** built to operate autonomously within Azure environments to ensure AI infrastructure compliance, security, and governance. It features an LLM-powered agent that orchestrates scans, audits, and policy evaluations across Infrastructure as Code, model governance metadata, and runtime environments.

Leveraging tools like **Azure OpenAI**, **Azure Machine Learning**, **Terraform**, and **Ansible**, the solution supports:

- Autonomous compliance gap detection
- Responsible AI governance checks (e.g., drift, fairness, explainability)
- Regulatory alignment (e.g., APRA CPS 234, Microsoft Responsible AI)
- Scalable and cost-efficient automation using GitOps best practices


## Features

- **Infrastructure Scan:** Detect misconfigurations such as public storage, untagged resources, and expired certificates.
- **AI Model Governance Check:** Evaluate AI models for drift, bias, explainability, and fairness using metadata.
- **Audit Log Analysis:** Identify potentially non-compliant data transfers and sensitive data exposures in logs.
- **Reporting:** Generate summary compliance reports aligned with APRA CPS 234 and Responsible AI guidelines.
- **Agentic AI Assistant:** A limited agentic AI assistant to guide users interactively through compliance checks and recommendations.

## Technology Stack

- **Azure Services:** Azure CLI, Azure Storage SDK (locally simulated or minimal usage), Azure OpenAI (optional for agentic AI features)
- **Infrastructure as Code:** Terraform and Ansible (demonstrated via templates and scripts)
- **DevOps Tools:** Git for version control, basic CI/CD scripts (optional)
- **Programming:** Python for compliance checks, report generation, and agentic AI orchestration
- **AI and Analytics:** Local model explainability/bias checks, minimal Azure AI service calls to reduce cost

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
git clone <repo-url>
cd regulatory-compliance-checker
```
2. Create a virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or
.\\.venv\\Scripts\\activate  # Windows
```
pip install -r requirements.txt

### Usage
Run the compliance checks individually or via the interactive agentic AI assistant:
```bash
python src/compliance_checker/agentic_ai.py
```
This will prompt you through scanning options and generate reports accordingly.

### Testing
Run unit tests with:
```bash
pytest tests/test_infra_scan.py
pytest tests/test_model_audit.py
pytest tests/test_pii_scan.py
pytest tests/test_report.py
pytest tests/test_tag_policy.py
```
## Documentation
Refer to detailed design and as-built documentation in the docs/ folder (to be added).

## Roadmap
Planned enhancements:
Integration with Azure DevOps pipelines for automated scanning
Enhanced AI governance checks with Azure Machine Learning SDK
Web-based dashboard for compliance visualization
Full Azure resource scanning using Azure SDKs with proper auth
