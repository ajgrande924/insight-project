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

| Step | Command | Description |
| :---: | :---- | :---- |
| 1 | `./run_kube setup_eks` | setup vpc + eks cluster |
| 2 | `./run_kube helm_init` | instantiate helm + tiller |
| 3 | `./run_kube setup_monitoring` | setup monitoring |

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

| Step | Command | Description |
| :---: | :---- | :---- |
| 1 | `./run_kube cleanup_monitoring` | cleanup monitoring |
| 2 | `./run_kube cleanup_tiller` | cleanup tiller |
| 3 | `./run_kube teardown` | destroy eks cluster + vpc |

