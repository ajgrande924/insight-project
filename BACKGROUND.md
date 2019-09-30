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

