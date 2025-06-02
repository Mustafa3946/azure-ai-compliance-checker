output "resource_group_name" {
  value = azurerm_resource_group.compliance_rg.name
}

output "storage_account_name" {
  value = azurerm_storage_account.compliance_storage.name
}
