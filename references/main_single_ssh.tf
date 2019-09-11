# ability to ssh only from your current local ip address
data "http" "ip-address" {
  url = "http://ipv4.icanhazip.com"
}

locals  {
  ipAddress = "${chomp(data.http.ip-address.body)}/32"
}

module "single_ssh_sg" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "3.1.0"
  name        = "single-ssh-sg"
  description = "Security group that enables inbound SSH connection from my personal IP address"
  vpc_id              = module.sandbox_vpc.vpc_id
  ingress_cidr_blocks = ["10.0.0.0/26"]
  ingress_with_cidr_blocks = [
    {
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      cidr_blocks = "${local.ipAddress}"
    },
  ]
  egress_cidr_blocks = ["10.0.0.0/26"]
  egress_with_cidr_blocks = [
    {
      from_port   = 0
      to_port     = 0
      protocol    = "-1"
      cidr_blocks = "10.0.0.0/26"
    },
  ]
  tags = {
    Owner       = var.fellow_name
    Environment = "dev"
    Terraform   = "true"
  }
}