

## Run the monitoring app in kind
- Create kind cluster `kind create cluster --config=kind.yaml` 
- Load local image in kind nodes `kind load docker-image django-app:latest`
- Deploy `kubectl apply -f k8s --recursive`


## Custom metric pod autoscaling

The metrics registry is a central place in the cluster where metrics (of any kind) are exposed to clients (of any kind).

The Horizontal Pod Autoscaler is one of these clients.

![img1](https://learnk8s.io/a/dc4023a7cd4f93d5626ca09968d4c29a.svg)

The interface of the metrics registry consists of three separate APIs:

- Resource Metrics API: predefined resource usage metrics (CPU and memory) of Pods and Nodes
- Custom Metrics API: custom metrics associated with a Kubernetes object
- External Metrics API: custom metrics not associated with a Kubernetes object

Any metric that you want to use as a scaling metric must be exposed through one of these three metric APIs.
You also have to expose your desired scaling metric through the metric registry.

![img2](https://learnk8s.io/a/a0f449da74937da4ec61f53bdb81164b.svg)


So, to expose a metric through one of the metric APIs, you have to go through these steps:

1. Install a metrics collector (e.g. Prometheus) and configure it to collect the desired metric (e.g. from the Pods of your app)

2. Install a metric API server (e.g. the Prometheus Adapter) and configure it to expose from the metrics collector through the corresponding metrics API. This is a hard part https://github.com/kubernetes-sigs/prometheus-adapter.

3. Now Create a HorizontalPodAutoscaler similar to below code
```
apiVersion: autoscaling/v2beta2
kind: HorizontalPodAutoscaler
metadata:
  name: myhpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 1
  maxReplicas: 10
  metrics:
    - type: Pods
      pods:
        metric:
          name: myapp_requests_per_second
        target:
          type: AverageValue
          averageValue: 2
```




