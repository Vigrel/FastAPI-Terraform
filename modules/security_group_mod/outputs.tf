# source of descriptions: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group

output "arn" {
  value       = aws_security_group.main.arn
  description = "ARN of the security group"
}

output "id" {
  value       = aws_security_group.main.id
  description = "ID of the security group"
}

output "owner_id" {
  value       = aws_security_group.main.owner_id
  description = "Owner ID"
}
