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
