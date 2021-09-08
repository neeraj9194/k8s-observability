

## Run the monitoring in kind
- `kind create cluster --config=kind.yaml` 
- load local image in kind nodes `kind load docker-image django-app:latest`
- `kubectl apply -f k8s`

