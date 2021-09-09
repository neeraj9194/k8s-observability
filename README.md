

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


## Kubernetes service discovery

Using kubernetes service discovery(kubernetes_sd_configs) you can scrape services, nodes, pods for data without configuring everytime there is new service/node etc.


### To configure for discovering services

The config is done only once to discover service [endpoints](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#endpoints) from where it can fetch data, provided we have configured services with prometheus annotation so that it know which port and endpoint to call.


The job prometheus config looks like this,

```
  - job_name: 'kubernetes-service-endpoints'
    kubernetes_sd_configs:
    - role: endpoints
    relabel_configs:
      # these are the annotation you will be configuring on your services
    - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scrape]
      action: keep
      regex: true
    - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scheme]
      action: replace
      target_label: __scheme__
      regex: (https?)
    - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_path]
      action: replace
      target_label: __metrics_path__
      regex: (.+)
    - source_labels: [__address__, __meta_kubernetes_service_annotation_prometheus_io_port]
      action: replace
      target_label: __address__
      regex: ([^:]+)(?::\d+)?;(\d+)
      replacement: $1:$2
    - action: labelmap
      regex: __meta_kubernetes_service_label_(.+)
    - source_labels: [__meta_kubernetes_namespace]
      action: replace
      target_label: kubernetes_namespace
    - source_labels: [__meta_kubernetes_service_name]
      action: replace
      target_label: kubernetes_name
```

And the service config we can do like this, that way we can add as many services as we like and it will be detected automatically. 

```
apiVersion: v1
kind: Service
metadata:
  name: django-app-svc
  annotations:
    prometheus.io/port: "8000"
    prometheus.io/scrape: "true"
```

There are other roles in kubernetes_sd_configs thta can be used for collecting from diffrent types of components.

Other types of metric collection techniques in kubernetes

- kubernetes-apiservers: It gets all the metrics from the API servers.
- nodes: It collects all the kubernetes node metrics.
- pods: All the pod metrics get discovered if the pod metadata is annotated with prometheus.io/scrape and prometheus.io/port annotations.
- kubernetes-cadvisor: Collects all cAdvisor metrics.
- endpoints: All the Service endpoints are scrapped if the service metadata is annotated with prometheus.io/scrape and prometheus.io/port annotations.
- service The service role discovers a target for each service port for each service. This is generally useful for blackbox monitoring of a service. The address will be set to the Kubernetes DNS name of the service and respective service port.