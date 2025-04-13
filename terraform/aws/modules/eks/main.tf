
resource "aws_eks_cluster" "eks" {
  name     = "nci-research-eks"
  role_arn = var.cluster_role

  vpc_config {
    subnet_ids = var.subnet_ids
  }
}

output "cluster_endpoint" {
  value = aws_eks_cluster.eks.endpoint
}

output "cluster_certificate_authority" {
  value = aws_eks_cluster.eks.certificate_authority[0].data
}
