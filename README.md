# insight_project
> todo insight project

### terraform setup

Add aws credentials to `.profile` or `.zprofile`:
```sh
export AWS_ACCESS_KEY_ID=XXXXXXXXXXXXXXXXXXX 
export AWS_SECRET_ACCESS_KEY=XXXXXXXXXXXXXXXXXXXX
```

Using `terraform@>=0.12`, to provision the infrastructure:
```sh
# provision infra
cd terraform
terraform init
terraform apply

# destroy infra
cd terraform 
terraform destroy
```

Update security group from open_all_sg to open_ssh_only:
```terraform
# open all security group
module "open_all_sg" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "3.1.0"

  name        = "open-to-all-sg"
  description = "Security group to make all ports publicly open...not secure at all"

  vpc_id              = module.sandbox_vpc.vpc_id
  ingress_cidr_blocks = ["10.0.0.0/26"]
  ingress_with_cidr_blocks = [
    {
      rule        = "all-all"
      cidr_blocks = "0.0.0.0/0"
    },
  ]

  egress_cidr_blocks = ["10.0.0.0/26"]
  egress_with_cidr_blocks = [
    {
      rule        = "all-all"
      cidr_blocks = "0.0.0.0/0"
    },
  ]

  tags = {
    Owner       = var.fellow_name
    Environment = "dev"
    Terraform   = "true"
  }
}

# open ssh only security group
module "open_ssh_sg" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "3.1.0"

  name        = "open-ssh-sg"
  description = "security group that allows ssh and all egress traffic"

  vpc_id              = module.sandbox_vpc.vpc_id
  ingress_cidr_blocks = ["10.0.0.0/26"]
  ingress_with_cidr_blocks = [
    {
      from_port = 22
      to_port = 22
      protocol = "tcp"
      cidr_blocks = "0.0.0.0/0"
    },
  ]

  egress_cidr_blocks = ["10.0.0.0/26"]
  egress_with_cidr_blocks = [
    {
      from_port = 0
      to_port = 0
      protocol = "-1"
      cidr_blocks = "0.0.0.0/0"
    },
  ]

  tags = {
    Owner       = var.fellow_name
    Environment = "dev"
    Terraform   = "true"
  }
}
```

Test ssh:
```sh
ssh -i <path_to_pem> ubuntu@<public_ip>
```

### packer setup

 - creates ami w/ all of the necessary software
 - speeds up boot times of instances
 - common approach when you run a horizontally scaled app layer

```sh
# build custom ami: test_ami
cd packer/test_ami
packer build -machine-readable packer.json
```
Add aws default region to `.profile` or `.zprofile`:
```sh
export AWS_DEFAULT_REGION=us-west-2
```

Created script to list and delete user amis (requires `awscli`):

```sh
Usage: ./aws_ami_cleaner.sh [options]

Options:

  -a, --aws_account_id <id>  aws account id
  -l, --list                 list user amis
  -d, --delete_all           delete all user amis
  -h, --help                 output usage information
```

```sh
# list user amis
./aws_ami_cleaner.sh -a <aws_account_id> -l

# delete all user amis
./aws_ami_cleaner.sh -a <aws_account_id> -d
```

### todo

  - [x] change security group from open_all_sg to open_ssh_sg
  - [x] utilize packer to build custom ami w/ desired software
  - [ ] ability to remote exec into instance to install software such as nginx or docker 
  - [ ] ability to pull docker image from global registry to aws instance