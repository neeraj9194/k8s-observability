# Pod affinity

https://www.verygoodsecurity.com/blog/posts/kubernetes-multi-az-deployments-using-pod-anti-affinity

https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#an-example-of-a-pod-that-uses-pod-affinity

topology-spread: https://kubernetes.io/docs/concepts/workloads/pods/pod-topology-spread-constraints/

The Pod affinity/anti-affinity may be formalized as follows. “this Pod should or should not run in an X node if that X node is already running one or more pods that meet rule Y”.
Y is a LabelSelector of Pods running on that node.
X may be a node, rack, CSP region, CSP zone, etc. Users can express it using a `topologyKey`.

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-cache
spec:
  selector:
    matchLabels:
      app: store
  replicas: 3
  template:
    metadata:
      labels:
        app: store
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - store
            topologyKey: "kubernetes.io/hostname"
      containers:
      - name: redis-server
        image: redis:3.2-alpine

---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-server
spec:
  selector:
    matchLabels:
      app: web-store
  replicas: 3
  template:
    metadata:
      labels:
        app: web-store
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - web-store
            topologyKey: "kubernetes.io/hostname"
        podAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - store
            topologyKey: "kubernetes.io/hostname"
      containers:
      - name: web-app
        image: nginx:1.16-alpine
```


# Pod Topology Spread

You can use topology spread constraints to control how Pods are spread across your cluster among failure-domains such as regions, zones, nodes, and other user-defined topology domains. This can help to achieve high availability as well as efficient resource utilization.

```
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
  labels:
    foo: bar
spec:
  topologySpreadConstraints:
  - maxSkew: 1 
    topologyKey: topology.kubernetes.io/zone 
    whenUnsatisfiable: DoNotSchedule 
    labelSelector: 
      matchLabels:
        foo: bar 
  containers:
  - image: "docker.io/ocpqe/hello-pod"
    name: hello-pod
```


- The maximum difference in number of pods between any two topology domains. The default is 1, and you cannot specify a value of 0.

- The key of a node label. Nodes with this key and identical value are considered to be in the same topology.

- How to handle a pod if it does not satisfy the spread constraint. The default is DoNotSchedule, which tells the scheduler not to schedule the pod. Set to ScheduleAnyway to still schedule the pod, but the scheduler prioritizes honoring the skew to not make the cluster more imbalanced.

- Pods that match this label selector are counted and recognized as a group when spreading to satisfy the constraint. Be sure to specify a label selector, otherwise no pods can be matched.

- Be sure that this Pod spec also sets its labels to match this label selector if you want it to be counted properly in the future.