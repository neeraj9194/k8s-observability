

## Run the monitoring in kind
- Create kind cluster `kind create cluster --config=kind.yaml` 
- Load local image in kind nodes `kind load docker-image django-app:latest`
- Deploy `kubectl apply -f k8s --recursive`

