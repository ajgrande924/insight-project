## Background

#### tech stack

  - docker (containers)
  - kubernetes (orchestration)
  - aws eks (cloud)
  - prometheus / grafana (monitoring)

#### project pitch

Containers, Orchestration, and Chaos

Having a resilient data pipeline for your business is becoming a necessity to stay competitive in times where vast amounts of data are generated and consumed. Containers allow you to focus on a single area of concern, whether it is application data capture, storage, analysis, or visualization. Container orchestrators like Kubernetes can help deploy, manage, and scale containerized components of modern cloud native data pipelines. So how do we test for resiliency? My project focuses on taking an existing data pipeline, Scale, containerizing each piece of the pipeline,utilizing container orchestration, and testing for resiliency by running a set of chaos experiments.

The existing batch data pipeline is called Scale. It is a music recommendation engine that finds similar songs based on shared instruments. The original application can be found [here](https://github.com/mothas/insight-music-project). The data pipeline is shown below:

<p align="center"> 
  <img src="./media/scale_data_pipeline.png" alt="scale_data_pipeline" width="800px"/>
</p>

  - S3: storage of midi files
  - Spark: extract data about instruments from midi files
  - Postgres: store results
  - Flask: view results
