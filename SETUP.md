## Setup

#### setup eks cluster

The application requires the following dependencies:

  - jq
  - awscli
  - kubetcl
  - aws-iam-authenticator
  - terraform @ >= 0.12

To start the application, you can run `./oneclick deploy`, which essentially runs these commands, but with auto approve:
```sh
# provision with terraform
cd terraform
terraform init
terraform plan
terraform apply

# add new context to ~/.kube/config
aws eks update-kubeconfig --name <cluster_name> # test-eks-ajdev

# checks
kubectl version
kubetctl get nodes
kubectl config current-context
kubectl config view
```

To bring down the application you can run `./oneclick destroy`, which essentially runs these commands, but with auto approve:
```sh
# destroy infrastructure
cd terraform
terraform destroy -auto-approve
rm -rf .terraform terraform.tfstate*
```

#### helm

```sh
# install helm / tiller
brew install kubernetes-helm

# delete cluster tiller
kubectl get all --all-namespaces | grep tiller
kubectl delete deployment tiller-deploy -n kube-system
kubectl delete service tiller-deploy -n kube-system
kubectl get all --all-namespaces | grep tiller

# a - initialize helm & add the service account
helm init 
kubectl create serviceaccount --namespace kube-system tiller
kubectl create clusterrolebinding tiller-cluster-rule --clusterrole=cluster-admin --serviceaccount=kube-system:tiller
kubectl patch deploy --namespace kube-system tiller-deploy -p '{"spec":{"template":{"spec":{"serviceAccount":"tiller"}}}}'

# or b - initialize helm & add the service account
helm init --service-account tiller
```

#### prometheus & grafana

```sh
# install prometheus
kubectl create namespace prometheus
helm install stable/prometheus \
    --name prometheus \
    --namespace prometheus \
    --set alertmanager.persistentVolume.storageClass="gp2" \
    --set server.persistentVolume.storageClass="gp2"

# check prometheus namespace
kubectl get all -n prometheus

# debug
kubectl port-forward -n prometheus deploy/prometheus-server 8080:9090

# install grafana
kubectl create namespace grafana
helm install stable/grafana \
    --name grafana \
    --namespace grafana \
    --set persistence.storageClassName="gp2" \
    --set adminPassword="notadmin" \
    --set datasources."datasources\.yaml".apiVersion=1 \
    --set datasources."datasources\.yaml".datasources[0].name=Prometheus \
    --set datasources."datasources\.yaml".datasources[0].type=prometheus \
    --set datasources."datasources\.yaml".datasources[0].url=http://prometheus-server.prometheus.svc.cluster.local \
    --set datasources."datasources\.yaml".datasources[0].access=proxy \
    --set datasources."datasources\.yaml".datasources[0].isDefault=true \
    --set service.type=LoadBalancer

# check grafana namespace
kubectl get all -n grafana

# get grafana elb url
export ELB=$(kubectl get svc -n grafana grafana -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
echo "http://$ELB"

# get grafana admin pw
kubectl get secret --namespace grafana grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

# In grafana dashboard
# - click '+' & select 'import' 
# - 3131 for 'Kubernetes All Nodes' Dashboard
# - 3146 for 'Kubernetes Pods' Dashboard
# - select 'Prometheus' under data sources
# - click 'import'
```