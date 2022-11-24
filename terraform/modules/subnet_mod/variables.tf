# source of descriptions: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/subnet

variable "vpc_id" {
  type        = string
  description = "ID of the VPC that the desired subnet belongs to"
}

variable "cidr_block" {
  type        = string
  description = "CIDR block of the desired subnet"
}

variable "availability_zone" {
  type        = string
  description = "Availability zone where the subnet must reside"
}

variable "tags" {
  type        = map(string)
  description = "Map of tags, each pair of which must exactly match a pair on the desired subnet"
  default = {
    Name = "tf-example"
  }
}
