## Setup

**requirements**

The application requires the following dependencies:

  - `jq`
  - `awscli`
  - `kubetcl`
  - `helm`
  - `aws-iam-authenticator`
  - `terraform @ >= 0.12`

**start application**

To start the application, you can run the following steps:

  - setup vpc + eks cluster: `./oneclick setup_eks`
  - instantiate helm + tiller: `./oneclick setup_helm`
  - setup prometheus: `./oneclick setup_prometheus`
  - setup grafana: `./onceclick setup_grafana`

```
# get grafana admin pw
kubectl get secret --namespace grafana grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

# In grafana dashboard
# - click '+' & select 'import' 
# - 3131 for 'Kubernetes All Nodes' Dashboard
# - 3146 for 'Kubernetes Pods' Dashboard
# - select 'Prometheus' under data sources
# - click 'import'
```

**teardown application**

To bring down the application you can run the following steps:

  - cleanup prometheus + grafana: `./oneclick cleanup_prom_graf`
  - cleanup tiller: `./oneclick cleanup_tiller`
  - destroy eks cluster + vpc: `./oneclick destroy`
