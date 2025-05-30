# azure-ai-compliance-checker
An Azure-powered compliance checker leveraging AI-driven automation and Infrastructure as Code. Demonstrates integration of Azure AI services, Terraform, Ansible, and GitOps to support secure and scalable AI operations aligned with enterprise governance and regulatory requirements.

## Project Overview

This project demonstrates an Azure-powered automated compliance checker designed to support enterprise AI governance, infrastructure security, and regulatory adherence. It leverages Infrastructure as Code (Terraform, Ansible) and integrates Azure AI services including Azure OpenAI and Azure Machine Learning to provide scalable, secure, and cost-efficient AI-driven automation.

Built to showcase core skills for an Azure Engineer (AI) role, this solution automates the detection of infrastructure misconfigurations, audits AI model governance (drift, fairness, explainability), and performs regulatory compliance reporting aligned with industry standards such as APRA CPS 234 and Responsible AI frameworks.

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
├── README.md
├── requirements.txt
├── .gitignore
├── main.py
├── agent/
│   ├── __init__.py
│   ├── base_agent.py
│   └── compliance_agent.py
├── checks/
│   ├── __init__.py
│   ├── infra_scanner.py
│   ├── ai_model_checker.py
│   └── log_auditor.py
├── reports/
│   ├── __init__.py
│   └── report_generator.py
├── config/
│   ├── settings.yaml
│   └── rules/
│       ├── infra_rules.json
│       ├── ai_rules.json
│       └── log_rules.json
├── scripts/
│   ├── deploy_with_terraform.sh
│   └── run_ansible_playbook.sh
├── notebooks/
│   ├── model_bias_analysis.ipynb
│   └── drift_detection.ipynb
└── tests/
    ├── __init__.py
    ├── test_infra_scanner.py
    ├── test_ai_model_checker.py
    └── test_log_auditor.py
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
python src/agentic_ai.py
```
This will prompt you through scanning options and generate reports accordingly.

### Testing
Run unit tests with:
```bash
pytest tests/
```
## Documentation
Refer to detailed design and as-built documentation in the docs/ folder (to be added).

## Roadmap
Planned enhancements:
Integration with Azure DevOps pipelines for automated scanning
Enhanced AI governance checks with Azure Machine Learning SDK
Web-based dashboard for compliance visualization
Full Azure resource scanning using Azure SDKs with proper auth
