# providers.tf
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.80"
    }
  }
  required_version = ">= 1.3"
}

provider "azurerm" {
  features {}

  subscription_id = "6897121f-97fc-4479-8d33-a05307e01483"  # Your actual Subscription ID
  tenant_id       = "50147da2-cd70-4a09-ace7-0803d9ad7874"  # Your actual Tenant ID
}