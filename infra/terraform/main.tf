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
