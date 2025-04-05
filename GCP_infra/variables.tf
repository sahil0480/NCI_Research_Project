variable "project_id" {
  description = "The ID of the GCP project"
  type        = string
}

variable "cluster_name" {
  description = "The name of the GKE cluster"
  default     = "nci-research-cluster"
}

variable "region" {
  description = "The region where GKE cluster will be deployed"
  default     = "europe-west1"
}
