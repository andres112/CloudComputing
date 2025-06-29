# **Kubernetes Command Reference**

## **1️⃣ Namespace Management**
- Create a namespace called `testing`:
  ```sh
  kubectl create ns testing
  ```

## **2️⃣ Pod Management**
- Run a pod in the `testing` namespace:
  ```sh
  kubectl run nginx --image=nginx -n testing
  ```
- Get all pods from all namespaces:
  ```sh
  kubectl get all -A
  ```
- Get the pod in the `testing` namespace:
  ```sh
  kubectl get pods -n testing
  ```
- Get pods with wide output:
  ```sh
  kubectl get pods -n testing -o wide
  ```
- Delete the pod immediately:
  ```sh
  kubectl delete pod nginx -n testing --now
  ```
- Generate YAML file for a pod:
  ```sh
  kubectl run nginx --image=nginx -n testing --dry-run=client -o yaml | tee pod.yaml
  ```

## **3️⃣ Logs & Monitoring**
- Get logs of a pod:
  ```sh
  kubectl logs pods/nginx -n testing
  ```
- Follow the logs of a pod starting from the last 500 lines:
  ```sh
  kubectl logs -f --tail=500 pods/nginx -n testing
  ```
- Follow the logs od a pod since a specific time:
  ```sh
  kubectl logs -f --since=1h pods/nginx -n testing
  ```
- Get logs from a previous instance of a container:
  ```sh
  kubectl logs -p pods/nginx -n testing
  ```
- Command to monitor the pod until it is running:
  ```sh
  until kubectl logs pod/countdown-pod -c init-countdown -n testing -f --pod-running-timeout=5m; do sleep 1; done;
  until kubectl logs pod/countdown-pod -c main-container -n testing -f --pod-running-timeout=5m; do sleep 1; done
  ```
- Get resources by label:
  ```sh
  kubectl get pods -l app=nginx -n testing
  ```
- Get resources with level of verbosity:
  ```sh
  kubectl get pods -n testing -v=7
  ```

## **4️⃣ Networking & Connectivity**
- Port-forward the pod to localhost:
  ```sh
  kubectl port-forward nginx 8081:80 -n testing
  ```
- Run a temporary pod to test connectivity:
  ```sh
  kubectl run -it --rm curl-tool --image=curlimages/curl --restart=Never -- sh
  then curl http://nginx:80
  ```

## **5️⃣ Deployments & Replica Management**
- Generate YAML for a Deployment and apply it:
  ```sh
  kubectl create deploy nginx --image=nginx -n testing --dry-run=client -o yaml | tee deployment.yaml | kubectl apply -f -
  ```
- Get a Deployment:
  ```sh
  kubectl get deploy -n testing
  ```
- Get a ReplicaSet:
  ```sh
  kubectl get rs -n testing
  ```
- Modify replicas in a running deployment:
  ```sh
  kubectl scale deploy/nginx --replicas=3 -n testing; watch kubectl get pods -n testing
  ```
- Set the image of a Deployment to a new version:
  ```sh
  kubectl set image deploy/nginx nginx=nginx:1.19.1 -n testing
  ```

## **6️⃣ Rollouts & Rollbacks**
- Get the rollout history of a Deployment:
  ```sh
  kubectl rollout history deploy/nginx -n testing
  ```
- Get the rollout status of a Deployment:
  ```sh
  kubectl rollout status deploy/nginx -n testing
  ```
- Rollback a Deployment to a previous revision:
  ```sh
  kubectl rollout undo deploy/nginx -n testing --to-revision=1
  ```

## **7️⃣ Documentation & Help**
- Explain a field in Kubernetes resources:
  ```sh
  kubectl explain pod.spec.restartPolicy
  ```

## **8️⃣ Service Management**
- Expose a Deployment as a Service:
  ```sh
  kubectl expose deploy/nginx --port=8081 --target-port=80 -n testing
  ```
- Expose as a NodePort Service:
  ```sh
  kubectl expose deploy/nginx --port=8081 --target-port=80 --type=NodePort -n testing
  ```
- Expose as a LoadBalancer Service:
  ```sh
  kubectl expose deploy/nginx --port=8081 --target-port=80 --type=LoadBalancer -n testing
  ```
- Get a Service:
  ```sh
  kubectl get svc/nginx -n testing
  ```
- Get the endpoints of a Service:
  ```sh
  kubectl get ep/nginx -n testing
  ```
- Create headless service:
  ```sh
  kubectl create svc clusterip nginx --cluster-ip=None -n testing
  ```

## **9️⃣ Jobs & CronJobs**
- Create a Job:
  ```sh
  kubectl create job python-log-job --image=python:3.9 -n testing -- /bin/sh -c 'python -c "import time; [print(f\"Processing task {i+1}\") or time.sleep(2) for i in range(10)]"'
  ```
- Get a Job:
  ```sh
  kubectl get job/python-log-job -n testing
  ```
- Get the logs of a Job:
  ```sh
  kubectl logs job/python-log-job -n testing
  ```
- Create a CronJob:
  ```sh
  kubectl create cj python-log-cronjob --image=python:3.9 -n testing --schedule="* * * * *" -- /bin/sh -c 'python -c "import time; [print(f\"Processing task {i+1}\") or time.sleep(2) for i in range(10)]"'
  ```
- Get a CronJob:
  ```sh
  kubectl get cj python-log-cronjob -n testing
  ```

## **🔟 Configmaps**
- Create a ConfigMap from literal:
  ```sh
  kubectl create configmap colour-configmap --from-literal=colour=blue --from-literal=KEY=value -n testing
  ```
- Create a ConfigMap from env file:
  ```sh
  kubectl create configmap app-config --from-env-file=app.env -n testing
  ```
- Create a ConfigMap from file:
  ```sh
  kubectl create configmap app-config --from-file=app.properties -n testing
  ```

## **1️⃣1️⃣ Secrets**
- Create a Secret from literal:
  ```sh
  kubectl create secret generic db-secret --from-literal=username=admin --from-literal=password=passw0rd -n testing
  ```
- Create a Secret from file:
  ```sh
  kubectl create secret generic db-secret --from-file=credentials.txt -n testing
  ```

## **1️⃣2️⃣ RBAC **
# ClusterRole and ClusterRoleBinding
- Create a ClusterRole:
  ```sh
  kubectl create clusterrole cluster-superhero --verb=get,list,watch --resource=pods
  ```
- Create a ClusterRoleBinding with group:
  ```sh
  kubectl create clusterrolebinding cluster-superhero --clusterrole=cluster-superhero --group=cluster-superheroes
  ```
- Create a ClusterRoleBinding with user:
  ```sh
  kubectl create clusterrolebinding cluster-superhero --clusterrole=cluster-superhero --user=batman
  ```
- Create a ClusterRoleBinding with service account:
  ```sh
  kubectl create clusterrolebinding cluster-superhero --clusterrole=cluster-superhero --serviceaccount=default:pod-sa
  ```
- Auth can In:
  ```sh
  kubectl auth can-i get pods --as=cluster-superhero  OR 
  kubectl auth can-i "*" "*" --as-group=cluster-superheroes --as="batman" OR
  kubectl auth can-i get pods --as=harry -n hogwarts # Just for specific namespace
  ```
# Role and RoleBinding
- Create a Role:
  ```sh
  kubectl create role pod-reader --verb=get,list,watch --resource=pods -n hogwarts
  ```
- Create a RoleBinding:
  ```sh
  kubectl create rolebinding pod-reader-binding --role=pod-reader --user=harry -n hogwarts
  ```
- Create a RoleBinding with group:
  ```sh
  kubectl create rolebinding pod-reader-binding --role=pod-reader --group=gryffindor -n hogwarts
  ```
- Create a RoleBinding with service account:
  ```sh
  kubectl create rolebinding pod-reader-binding --role=pod-reader --serviceaccount=default:pod-sa -n hogwarts
  ```
# ServiceAccount
- Create a ServiceAccount:
  ```sh
  kubectl create sa pod-sa -n hogwarts 
  ```

## **1️⃣3️⃣ Storage Management**
- Get StorageClass: StorageClass are cluster-wide resources
  ```sh
  kubectl get sc
  ```
- Get PersistentVolume: PV are cluster-wide resources
  ```sh
  kubectl get pv
  ```
- Get PersistentVolumeClaim: PVC are namespace-scoped resources
  ```sh
  kubectl get pvc -n testing
  ```

## **1️⃣4️⃣ Pod Disruption Budgets**
- Create a PodDisruptionBudget for a Deployment with label `app=nginx`:
  ```sh
  kubectl create pdb nginx-pdb --selector=app=nginx --min-available=1 -n testing
  ```
- Cordon a node:
  ```sh
  kubectl cordon <node-name>
  ```
- Drain a node:
  ```sh
  kubectl drain <node-name> --ignore-daemonsets --delete-local-data
  ```
- Uncordon a node:
  ```sh
  kubectl uncordon <node-name>
  ```

## **1️⃣5️⃣ HELM**

helm repo add bitnami https://charts.bitnami.com/bitnami    # Add a chart repository
helm search repo nginx                                       # Search for charts
helm install my-release bitnami/nginx -n testing             # Install a chart
helm upgrade my-release bitnami/nginx -n testing             # Upgrade the release
helm uninstall my-release -n testing                         # Uninstall the release
helm list -A                                               # List all releases