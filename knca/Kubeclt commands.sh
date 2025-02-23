# Create a namespace called testing
kubectl create ns testing

# Run a pod in the testing namespace
kubectl run nginx --image=nginx -n testing 

# Get all from all namespaces
kubectl get all -A

# Get the pod in the testing namespace
kubectl get pods -n testing

# Get pods with wide output
kubectl get pods -n testing -o wide

# Get pod logs
kubectl logs pods/nginx -n testing

# Follow the logs of a pod starting from last 500 lines
kubectl logs -f --tail=500 pods/nginx -n testing

# Get logs from a previous instance of a container
kubectl logs -p pods/nginx -n testing

# Port forward the pod to localhost
kubectl port-forward nginx 8081:80 -n testing 

# Runs a temporary pod named "curl-tool" using the "curlimages/curl" image, 
# executes an HTTP request to 10.42.0.5, and removes the pod after execution.
kubectl run -it --rm curl-tool --image=curlimages/curl --restart=Never -- http://10.42.0.5

# Delete the pod immediately
kubectl delete pod nginx -n testing --now

# Create a yaml file for a pod
kubectl run nginx --image=nginx -n testing --dry-run=client -o yaml | tee pod.yaml

# DOC: explain something
kubectl explain pod.spec.restartPolicy

# Command to monitor the pod until it is running
until kubectl logs pod/countdown-pod -c init-countdown -n testing -f --pod-running-timeout=5m; do sleep 1; done; until kubectl logs pod/countdown-pod -c main-container -n testing -f --pod-running-timeout=5m; do sleep 1; done

# Command to generate the yaml file for a deployment
kubectl create deploy nginx --image=nginx -n testing --dry-run=client -o yaml | tee deployment.yaml | kubectl apply -f -

# Get deployment
kubectl get deploy -n testing

# Get ReplicaSet
kubectl get rs -n testing

# Get the rollout history of a deployment
kubectl rollout history deploy/nginx -n testing

# Get the rollout status of a deployment
kubectl rollout status deploy/nginx -n testing

# Modify replicas in running deployment
kubectl scale deploy/nginx --replicas=3 -n testing; watch kubectl get pods -n testing
