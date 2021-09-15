# Event Driven auto scaling using KEDA

![img1](https://dz2cdn1.dzone.com/storage/temp/13757677-keda-arch.png)

KEDA acts to monitor the event source and feed that data to Kubernetes and the HPA (Horizontal Pod Autoscaler) to drive rapid scale of a deployment. Each replica of a deployment is actively pulling items from the event source. With KEDA and scaling deployments you can scale based on events while also preserving rich connection and processing semantics with the event source (e.g. in-order processing, retries, deadletter, checkpointing).

## Prerequisites

- Install Helm

## Install Keda

```
$ helm repo add kedacore https://kedacore.github.io/charts

$ helm repo update

$ kubectl create namespace keda

$ helm install keda kedacore/keda --namespace keda
```


## ScaledObject spec

ScaledObject custom resource definition which is used to define how KEDA should scale your application and what the triggers are.

```
apiVersion: keda.k8s.io/v1alpha1
kind: ScaledObject
metadata:
  name: django-app-scaler
spec:
  scaleTargetRef:
    deploymentName: django-app # must be in the same namespace as the ScaledObject
    containerName: django-app  #Optional. Default: deployment.spec.template.spec.containers[0]
  pollingInterval: 30  # Optional. Default: 30 seconds
  cooldownPeriod:  300 # Optional. Default: 300 seconds
  minReplicaCount: 1   # Optional. Default: 0
  maxReplicaCount: 10 # Optional. Default: 100
  triggers:
  - type: prometheus
    metadata:
      serverAddress: http://prometheus:9090
      metricName: process_virtual_memory_bytes
      query: rate(process_virtual_memory_bytes{deployment="my-deployment"}[20m])
      threshold: '100'  
```



