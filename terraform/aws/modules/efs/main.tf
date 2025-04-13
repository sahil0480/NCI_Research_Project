resource "aws_efs_file_system" "efs" {
  creation_token = "nci-research-efs"
  encrypted      = true

  tags = {
    Name = "nci-research-efs"
  }
}

resource "aws_efs_mount_target" "efs_mount" {
  count          = length(var.subnet_ids)
  file_system_id = aws_efs_file_system.efs.id
  subnet_id      = var.subnet_ids[count.index]
  security_groups = [var.security_group_id]
}
