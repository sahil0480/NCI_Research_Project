module "vpc" {
  source = "./modules/vpc"
}

module "iam" {
  source = "./modules/iam"
}

module "eks" {
  source       = "./modules/eks"
  vpc_id       = module.vpc.vpc_id
  subnet_ids   = module.vpc.subnet_ids
  cluster_role = module.iam.eks_cluster_role_arn
}

module "nodegroup" {
  source       = "./modules/nodegroup"
  cluster_name = module.eks.cluster_name
  subnet_ids   = module.vpc.subnet_ids
  key_name     = "my-ireland-key" # 🔑 Replace this with your actual EC2 key pair name in AWS
}

module "efs_irsa" {
  source        = "./modules/efs-irsa"
  cluster_name  = module.eks.cluster_name
}


module "efs" {
  source            = "./modules/efs"
  subnet_ids        = module.vpc.subnet_ids
  security_group_id = module.eks.cluster_security_group_id
  irsa_role_arn     = module.efs_irsa.irsa_role_arn
}



module "s3" {
  source      = "./modules/s3"
  bucket_name = "nci-multicloud-logs-bucket"
  environment = "prod"
}

module "ecr" {
  source = "./modules/ecr"
}
