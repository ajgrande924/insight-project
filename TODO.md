## todo

#### containerize

  9-16-19
  
  - [x] containerize simple flask app
  
  ```sh
  cd app/simple-flask
  docker build -t ajgrande924/simple-flask .
  docker login
  docker push ajgrande924/simple-flask
  ```

  9-18-19

  - [x] containerize puzzle flask app

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
  
  9-20-19

  - [ ] containerize flask application

#### orchestration

9-17-19

  - [x] bring up kube cluster through aws eks
  - [x] bring up monitoring tools (prometheus/grafana) on kuberneters cluster using helm

9-18-19

  - [x] nginx deployment available outside of kube cluster: `<hash>.us-west-2.elb.amazonaws.com`

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

  - [x] bring up simple flask application (stateless) on kube cluster
  - [x] bring up simple postgres db (stateful) on kube cluster
  - [x] communication between flask and postgres db
  - [x] flask application accessible outside of kube cluster

  ```sh
  # handles all  4 list items above
  kubectl apply --recursive -f kubernetes/puzzle-app # ka
  kubectl exec -i -t <flask_container_name> sh # kex
  python -c  'import database; database.init_db()'
  exit
  kubectl delete --recursive -f kubernetes/puzzle-app # krmf
  ```

#### chaos

  - [ ] setup monitoring on kube cluster, with prometheus/grafana, using helm charts
