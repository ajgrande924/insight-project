# insight_project
> chaos @ scale

## Table of Contents

  - [Introduction](README.md#Introduction)
  - [Tech Stack](README.md#Tech-Stack)
  - [Setup](README.md#Setup)
  - [Notes](README.md#Notes)

## Introduction

### containerize, iac, orchestration

In this project, we will be performing the experiments on a music recommendation data pipeline. The original source code for this application can be found at this [link](https://github.com/ajgrande924/insight-music-project).

Scale is a music recommendation engine that finds similar songs based on shared instruments. The data pipeline is shown below:

S3 -> Spark -> Postgres -> Flask (replace w/ diagram)

  - S3: storage of midi files
  - Spark: extract data about instruments from midi files
  - Postgres: store results
  - Flask: view results

In this part of the project, I will be containerizing the data pipeline and automating the deployment utilizing IaC & container orchestration.

Services within the kubernetes cluster:

  - spark (stateless, kube / ec2?)
  - postgres (stateful, kube / rds?)
  - flask (stateless)

### chaos testing

As an industry, we are quick to adopt practices that increase the flexibility of developement and velocity of deployment. But how much confidence do we have on the complex systems we put out in production. Chaos engineering is the discipline of experimenting on a distributed system in order to gain confidence in a system's capability to withstand turbulent conditions in production. To address this uncertainty, we will be running a set of experiments to uncover systemic weaknesses.

In this experiment, we will be deploying two instances of the data pipeline, a control group and an experimental group. We also will define a 'steady state' which will indicate some sort of normal behavior for the pipeline. We will be running a set of tests on the experimental group which will try to disrupt the steady state, giving us more confidence in our system.

Tests:

  - Will the system will be able to handle CPU / shutdown attacks at the container level?
  - Will the system be able to handle attacks at the pod level?
  - Will the system be able to handle an attack on availability zone?

Results:

  - need to figure out how we test steady state, what metrics from the distributed system are we going to track?
  - for mvp, simplest monitoring/observability mechanism would be CloudWatch? for stretch, incorporate what?

Experiments:

  - application receives increased 

## Tech Stack

  - `terraform @ >=0.12`
  - `packer @ >= 1.4.3`

## Setup

## Notes

Questions I need to answer:

  - why are you containerizing this application?
  - why did you decide to containerize spark?
  - why did you decide to containerize postgress instead of using aws rds?
  - why are you using kubernetes for container orchestration?
  - how do you plan to set up application infrastructure within kubernetes cluster?
  - what type of chaos experiments will I run and how will I monitor this?

What baseline metrics to collect for CE, or use for comparison between experimental / control group:

  - Infrastructure Monitoring Metrics

    - Resource: CPU, IO, Disk & Memory
    - State: Shutdown, Processes, Clock Time
    - Network: DNS, Latency, Packet Loss

  - Alerting and On-Call Metrics

    - Total alert counts by service per week
    - Time to resolution for alerts per service
    - Noisy alerts by service per week (self-resolving)
    - Top 20 most frequent alerts per week for each service.

  - High Severity Incident (SEV) Metrics

    - Total count of incidents per week by SEV level
    - Total count of SEVs per week by service
    - MTTD, MTTR and MTBF for SEVs by service

  - Application Metrics

    - Events
    - Stack traces
    - Context
    - Breadcrumbs

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
  - [ ] test application locally
  - [ ] containerize data pipeline 
  - [ ] deploy a simple example on aws eks and enable Cloudwatch 
  - [ ] deploy real project on aws eks w/ a control group and experimental group; enable cloud watch
  - [ ] perform attacks on experimental group at container, pod, zone level
  - [ ] iterate over infrastructure / architechture based on results

### references

  - terraform module, ssh only from your current local ip (from John)
  - [Principles of Chaos Engineering](http://principlesofchaos.org/?lang=ENcontent)
  - [awesome-chaos-engineering](https://github.com/dastergon/awesome-chaos-engineering)
  - [chaos engineering monitoring metrics guide](https://www.gremlin.com/community/tutorials/chaos-engineering-monitoring-metrics-guide/)
  - [Why run Spark on Kubernetes?](https://medium.com/@rachit1arora/why-run-spark-on-kubernetes-51c0ccb39c9b)