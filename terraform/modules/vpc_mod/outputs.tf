# source of descriptions: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/vpc

output "arn" {
  value       = aws_vpc.main.arn
  description = "Amazon Resource Name (ARN) of VPC"
}

output "id" {
  value       = aws_vpc.main.id
  description = "The ID of the VPC"
}

output "default_security_group_id" {
  value       = aws_vpc.main.default_security_group_id
  description = "The ID of the security group created by default on VPC creation"
}
