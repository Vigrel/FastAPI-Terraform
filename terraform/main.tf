terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.40"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region  = "us-east-1"
  profile = "cloudProject"
}

module "vpc" {
  source     = "./modules/vpc_mod"
  cidr_block = "172.16.0.0/16"
}

module "security_group" {
  source      = "./modules/security_group_mod"
  name        = "instance-sg"
  description = "security group for production grade web servers"
  vpc_id      = module.vpc.id
}

module "subnet" {
  source            = "./modules/subnet_mod"
  vpc_id            = module.vpc.id
  cidr_block        = "172.16.10.0/24"
  availability_zone = "us-east-1a"
}

module "instance" {
  source                 = "./modules/instance_mod"
  subnet_id              = module.subnet.id
  vpc_security_group_ids = [module.security_group.id]
}


