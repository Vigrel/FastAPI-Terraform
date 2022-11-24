# source of descriptions: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance

variable "ami" {
  type        = string
  description = "AMI to use for the instance"
  default     = "ami-0149b2da6ceec4bb0"
}

variable "instance_type" {
  type        = string
  description = "Instance type to use for the instance. Updates to this field will trigger a stop/start of the EC2 instance"
  default     = "t2.micro"
}

variable "vpc_security_group_ids" {
  type        = set(string)
  description = "List of security group IDs to associate with"
}

variable "subnet_id" {
  type        = string
  description = "VPC Subnet ID to launch in"
}

variable "tags" {
  type        = map(string)
  description = "Map of tags to assign to the resource. Note that these tags apply to the instance and not block storage devices"
  default = {
    Name = "HelloWorld"
  }
}
