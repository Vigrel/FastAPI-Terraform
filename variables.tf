
variable "instances" {
  description = "AMI to use for the instance and instance type to use for the instance. Updates to this field will trigger a stop/start of the EC2 instance"
  type = map(object({
    ami           = string
    instance_type = string
  }))
}

variable "ingress" {
  type        = list(any)
  description = "Configuration block for ingress rules. Can be specified multiple times for each ingress rule"
}
