## todo

#### containerize

**9-16-19**
  
  - [x] **CONT**: containerize simple flask app
  
  ```sh
  cd app/simple-flask
  docker build -t ajgrande924/simple-flask .
  docker login
  docker push ajgrande924/simple-flask
  ```

**9-17-19**

  - [x] **KUBE**: bring up kube cluster through aws eks
  - [x] **KUBE**: bring up monitoring tools (prometheus/grafana) on kuberneters cluster using helm

**9-18-19**

  - [x] **CONT**: containerize puzzle flask app

  ```sh
  # build
  cd app/puzzle-flask
  docker build -t ajgrande924/puzzle-flask .
  docker login
  docker push ajgrande924/puzzle-flask

  # run
  dex <container> sh
  python -c  'import database; database.init_db()'
  ```

  - [x] **KUBE**: nginx deployment available outside of kube cluster: `<hash>.us-west-2.elb.amazonaws.com`

  You can do this two ways:

  ```sh
  # 1. use yaml in repo
  
  # bringup
  kubectl apply -f kubernetes/nginx-app/nginx.yaml
  
  # teardown
  kubectl delete -f kubernetes/nginx-app/nginx.yaml

  # 2. specify through kubectl only
  
  # bringup
  kubectl create deployment --image nginx nginx-app
  kubectl scale deployment --replicas 2 nginx-app
  kubectl expose deployment nginx-app --port=80 --type=LoadBalancer
  
  # teardown
  kubectl delete svc nginx-app
  kubectl delete deployment nginx-app
  ```

**9-19-19**
  
  - [x] **KUBE**: bring up simple flask application (stateless) on kube cluster
  - [x] **KUBE**: bring up simple postgres db (stateful) on kube cluster
  - [x] **KUBE**: communication between flask and postgres db
  - [x] **KUBE**: flask application accessible outside of kube cluster

  ```sh
  # handles all  4 list items above
  kubectl apply --recursive -f kubernetes/puzzle-app # ka
  kubectl exec -i -t <flask_container_name> sh # kex
  python -c  'import database; database.init_db()'
  exit
  kubectl delete --recursive -f kubernetes/puzzle-app # krmf
  ```

**9-22-19**

  - [x] **CHAOS**: run simple kube-monkey example on minikube

  ```sh
  # minikube w/ kube monkey
  ./run_minikube init
  ./run_minikube start_chaos
  ./run_minikube cleanup_chaos
  ./run_minikube destroy
  ```

**9-23-19**

  - [x] **KUBE**: deploy prometheus-operator to monitor on eks cluster
  - [x] **KUBE**: ability to load custom dashboard through yaml/json
  - [ ] **MONIT**: ability to pull metrics from sample app to prometheus/grafana
  - [ ] **CONT**: finish containerizing scale app

**9-24-19**

**9-25-19**

**9-26-19**

**9-27-19**

**9-28-19**

  - [x] able to submit spark jobs to spark cluster on kubernetes and store in postgres
  - [ ] ...
  - [ ] ...
  - [ ] ...