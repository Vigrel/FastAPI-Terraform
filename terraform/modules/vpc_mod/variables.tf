# source of descriptions: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/vpc

variable "cidr_block" {
  type        = string
  description = "The IPv4 CIDR block for the VPC. CIDR can be explicitly set or it can be derived from IPAM using ipv4_netmask_length"
}

variable "tags" {
  type        = map(string)
  description = "Map of tags to assign to the resource"
  default = {
    Name = "tf-example"
  }
}

