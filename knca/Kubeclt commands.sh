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
- Get logs from a previous instance of a container:
  ```sh
  kubectl logs -p pods/nginx -n testing
  ```
- Command to monitor the pod until it is running:
  ```sh
  until kubectl logs pod/countdown-pod -c init-countdown -n testing -f --pod-running-timeout=5m; do sleep 1; done;
  until kubectl logs pod/countdown-pod -c main-container -n testing -f --pod-running-timeout=5m; do sleep 1; done
  ```

## **4️⃣ Networking & Connectivity**
- Port-forward the pod to localhost:
  ```sh
  kubectl port-forward nginx 8081:80 -n testing
  ```
- Run a temporary pod to test connectivity:
  ```sh
  kubectl run -it --rm curl-tool --image=curlimages/curl --restart=Never -- http://10.42.0.5
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
