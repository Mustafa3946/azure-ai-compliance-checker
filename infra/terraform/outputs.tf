# outputs.tf
#
# Outputs for Azure AI Compliance Checker Terraform deployment.
# Provides key resource names and the static website endpoint for reference after deployment.
#
# Outputs:
#   - resource_group_name: Name of the created resource group.
#   - storage_account_name: Name of the created storage account.
#   - container_name: Name of the blob container for compliance reports.
#   - static_website_url: URL endpoint for the storage account's static website.

output "resource_group_name" {
  value = azurerm_resource_group.compliance_rg.name
}

output "storage_account_name" {
  value = azurerm_storage_account.compliance_storage.name
}

output "container_name" {
  value = azurerm_storage_container.reports.name
}

output "static_website_url" {
  description = "URL of the storage account's static website"
  value       = azurerm_storage_account.compliance_storage.primary_web_endpoint
}
