# source of descriptions: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group

variable "name" {
  type        = string
  description = "Name of the security group. If omitted, Terraform will assign a random, unique name"
}

variable "description" {
  type        = string
  description = "(Optional, Forces new resource) Security group description"
}

variable "vpc_id" {
  type        = string
  description = "(Optional, Forces new resource) VPC ID. Defaults to the region's default VPC"
}

variable "tags" {
  type        = map(string)
  description = "Map of tags to assign to the resource"
  default = {
    Name = "allow_tls"
  }
}
variable "ingress" {
  type        = list(any)
  description = "Configuration block for ingress rules. Can be specified multiple times for each ingress rule"
}
