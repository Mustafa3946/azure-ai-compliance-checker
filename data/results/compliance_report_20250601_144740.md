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
