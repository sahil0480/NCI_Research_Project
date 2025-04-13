resource "aws_vpc" "eks" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "eks-vpc"
  }
}

data "aws_availability_zones" "available" {}

resource "aws_subnet" "eks" {
  count                   = 2
  vpc_id                  = aws_vpc.eks.id
  cidr_block              = "10.0.${count.index}.0/24"
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true  # ✅ This enables auto-assign public IPs

  tags = {
    Name = "eks-subnet-${count.index}"
  }
}

output "vpc_id" {
  value = aws_vpc.eks.id
}

output "subnet_ids" {
  value = aws_subnet.eks[*].id
}
