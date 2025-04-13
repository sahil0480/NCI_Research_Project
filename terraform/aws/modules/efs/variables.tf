variable "subnet_ids" {
  type = list(string)
}

variable "security_group_id" {
  type = string
}

variable "irsa_role_arn" {
  description = "IAM Role ARN for EFS CSI driver IRSA"
  type        = string
}
