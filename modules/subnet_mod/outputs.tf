# source of descriptions: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/subnet
output "arn" {
  value       = aws_subnet.main.arn
  description = "ARN of the subnet"
}

output "id" {
  value       = aws_subnet.main.id
  description = "The ID of the subnet"
}
