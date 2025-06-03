# main.tf
#
# Terraform configuration for deploying Azure resources required by the Azure AI Compliance Checker solution.
# This file provisions a resource group, storage account (with static website hosting), blob container for reports,
# and assigns the necessary role for blob data access.
#
# Resources:
#   - azurerm_resource_group: Resource group for all compliance checker resources.
#   - azurerm_storage_account: Storage account for storing reports and hosting the static website.
#   - azurerm_storage_account_static_website: Enables static website hosting on the storage account.
#   - azurerm_storage_container: Blob container for storing compliance reports.
#   - azurerm_role_assignment: Assigns 'Storage Blob Data Contributor' role to a specified user or service principal.
#
# Variables required:
#   - resource_group_name: Name for the resource group.
#   - location: Azure region for deployment.
#   - storage_account_name: Name for the storage account.
#   - blob_container_name: Name for the blob container.
#   - user_object_id: Object ID of the user or service principal to assign blob data contributor role.

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "compliance_rg" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_storage_account" "compliance_storage" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.compliance_rg.name
  location                 = azurerm_resource_group.compliance_rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  tags = {
    env = "demo"
  }
}

resource "azurerm_storage_account_static_website" "compliance_static_website" {
  storage_account_id = azurerm_storage_account.compliance_storage.id
  index_document     = "index.html"
  error_404_document = "404.html"
}

resource "azurerm_storage_container" "reports" {
  name                  = var.blob_container_name
  storage_account_name  = azurerm_storage_account.compliance_storage.name
  container_access_type = "blob"
}

resource "azurerm_role_assignment" "blob_data_contributor" {
  scope                = azurerm_storage_account.compliance_storage.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = var.user_object_id
}
