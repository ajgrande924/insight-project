## Background

#### tech stack

  - docker (containers)
  - kubernetes (orchestration)
  - aws eks (cloud)
  - prometheus / grafana (monitoring)

#### project pitch

Containers, Orchestration, and Chaos

Resilience means to be designed to withstand the unexpected. A resilient application can function despite having expected or unexpected failures to a system. If a single instance fails or and entire zone fails a resilient application remains fault tolerant by continuing to function or repairing itself automatically if necessary.

Having a resilient data pipeline for your business is becoming a necessity to stay competitive in times where vast amounts of data are generated and consumed. Containers allow you to focus on a single area of concern, whether it is application data capture, storage, analysis, or visualization. Container orchestrators like Kubernetes can help deploy, manage, and scale containerized components of modern cloud native data pipelines. So how do we test for resiliency? My project focuses on taking an existing data pipeline, Scale, containerizing each piece of the pipeline,utilizing container orchestration, and testing for resiliency by running a set of chaos experiments.

The existing batch data pipeline is called Scale. It is a music recommendation engine that finds similar songs based on shared instruments. The original application can be found [here](https://github.com/mothas/insight-music-project). The data pipeline is shown below:

<p align="center"> 
  <img src="./media/scale_data_pipeline.png" alt="scale_data_pipeline" width="800px"/>
</p>

  - S3: storage of midi files
  - Spark: extract data about instruments from midi files
  - Postgres: store results
  - Flask: view results

**chaos experiments**

Experiment 1: Resource exhaustion of containers

hypothesis:

  - increased latency in incoming requests
  - load balancer routes traffic away from availability zone 2
  - receive alert message

Experiment 2: Kill Stateful Replica Pod

scenario: Master postres replica pod is killed

hypothesis:

  - brief unavailability of data for a x duration of time
  - replica should get promoted (slave to master)
  - new clone should kick off and system recovers

**engineering challenges**

  **1. deployment of kubernetes cluster**
  
  I went through a few iterations when deploying my kubernetes cluster to the cloud. I tried using both KOPS and AWS. I decided to choose aws eks for a few reasons. The current data pipeline was also deployed on AWS with EC2 instances and the storage in which we will pull the data is also in AWS S3 which provides a much easier migration. AWS EKS is extremely simple to set up especially in conjunction with terraform. There is actually a great module on the terraform registry which allows you to use the base setup and spin up a cluster in 10 minutes. For time's sake, when you compare with KOPS, you do not have to provision anything in your control plane, you are only specifying your worker nodes. Also, one current downside to KOPS is that the terraform files generated for your cluster do not support `terraform>=0.12`. Since my terraform files are using the most up to date version of terraform, I did not want switch between versions to manage my infrastucture.
  
  **2. deployment of spark on kubernetes cluster**

  Spark is an open source, scalable, massively parallel, in-memory execution engine for analytics applications. It includes prebuilt machine learning algorithms which the scale application utilizes. Why should we use the Kubernetes cluster manager as opposed to the Standalone Scheduler? 
    
  - Are you using data analytical pipeline which is containerized? Are different pieces of your application containerized utilizing modern application patterns? It may make sense to use Kubernetes to manage your entire pipeline.
  - Resource sharing is better optimized b/c instead of running your pipeline on a dedicated hardware for each component, it is more efficient and optimal to run on a Kubernetes cluster so you can share resources between components.
  - utilizing the kubernetes ecosystem (multitenancy)
  - Limitations to the standalone scheduler still allow you to utilized Kubernetes features such as resource management, a variety of persistent storage options, and logging integrations.

  Currently as of `spark=2.4.4`, Kubernetes integration with Spark is still experimental. There are patches to the current version of Spark that can be added to make communication with the spark client and the kubernetes api server to work properly. Kubernetes scheduler will dynamically create pods for the spark cluster once the client submits the job. Communication with the spark cluster directly from the spark client is similar to the standalone scheduler but with utilization of some Kubernetes features such as resource management. It requires that the spark cluster is already up and running before you send the job.

