# variables.tf
#
# Defines input variables for the Azure AI Compliance Checker Terraform deployment.
# These variables allow customization of resource names, locations, and access control.
#
# Variables:
#   - resource_group_name: Name for the Azure resource group.
#   - location: Azure region for resource deployment.
#   - storage_account_name: Name for the Azure Storage Account.
#   - blob_container_name: Name for the blob container to store compliance reports.
#   - user_object_id: Azure AD Object ID of the user or service principal to assign Blob Data Contributor role.

variable "resource_group_name" {
  type    = string
  default = "ai-compliance-demo-rg"
}

variable "location" {
  type    = string
  default = "australiaeast"
}

variable "storage_account_name" {
  type    = string
  default = "aicompliancedemost"
}

variable "blob_container_name" {
  type    = string
  default = "reports"
}

variable "user_object_id" {
  description = "Azure AD Object ID of the user or service principal to assign Blob Data Contributor role"
  type        = string
}
