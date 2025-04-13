resource "aws_ecr_repository" "django_repo" {
  name                 = "django-app"
  image_tag_mutability = "MUTABLE"

  tags = {
    Name        = "django-app"
    Environment = "prod"
  }
}
