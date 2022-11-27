# source of descriptions: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance

output "arn" {
  value       = aws_instance.main.arn
  description = "ARN of the instance"
}

output "instance_state" {
  value       = aws_instance.main.instance_state
  description = "State of the instance. One of: pending, running, shutting-down, terminated, stopping, stopped"
}
