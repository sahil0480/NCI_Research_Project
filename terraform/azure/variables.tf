# ------------------------------
# variables.tf
# ------------------------------

# Azure authentication variables
variable "subscription_id" {
  description = "Azure Subscription ID"
  type        = string
}

variable "client_id" {
  description = "Azure Client ID"
  type        = string
}

variable "client_secret" {
  description = "Azure Client Secret"
  type        = string
  sensitive   = true
}

variable "tenant_id" {
  description = "Azure Tenant ID"
  type        = string
}

# AKS and ACR configuration
variable "resource_group_name" {
  description = "Resource group name"
  type        = string
  default     = "nci-azure-rg"
}

variable "location" {
  description = "Azure region for deployment"
  type        = string
  default     = "northeurope"
}

variable "aks_cluster_name" {
  description = "AKS cluster name"
  type        = string
  default     = "nci-aks-cluster"
}

variable "dns_prefix" {
  description = "DNS prefix for AKS"
  type        = string
  default     = "nci"
}

variable "node_count" {
  description = "Number of nodes in AKS cluster"
  type        = number
  default     = 2
}

variable "vm_size" {
  description = "VM size for AKS nodes"
  type        = string
  default     = "Standard_B2s"
}

variable "kubernetes_version" {
  description = "Kubernetes version for AKS"
  type        = string
  default     = "1.30.11"
}

variable "ssh_public_key" {
  description = "Path to SSH public key"
  type        = string
  default     = "~/.ssh/id_rsa.pub"
}

variable "acr_name" {
  description = "Azure Container Registry name"
  type        = string
  default     = "nciregistryacr"
}

variable "prefix" {
  description = "Prefix used for resource naming"
  type        = string
  default     = "nciaks"
}
