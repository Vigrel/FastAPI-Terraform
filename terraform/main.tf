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

# TODO: https://stackoverflow.com/questions/65628538/terraform-shows-invalidgroup-notfound-while-creating-an-ec2-instance

module "vpc" {
  source     = "./modules/vpc_mod"
  cidr_block = "172.31.0.0/16"
}

module "subnet" {
  source            = "./modules/subnet_mod"
  vpc_id            = module.vpc.id
  cidr_block        = "172.31.0.0/16"
  availability_zone = "us-east-1a"
}

module "instance" {
  source                 = "./modules/instance_mod"
  subnet_id              = module.subnet.id
  vpc_security_group_ids = [module.vpc.id]
}


