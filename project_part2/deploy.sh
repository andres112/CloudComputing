# Push images to Docker Hub
docker login
docker push andres112/watch-info:latest
docker push andres112/watch-image:latest

# Manifest execution
kubectl apply -f all.yml

# Update images for both deployments
kubectl set image deployment/watch-image watch-image=docker.io/andres112/watch-image:latest --record
kubectl set image deployment/watch-info watch-info=docker.io/andres112/watch-info:latest --record

# Verify Rolling Update status
kubectl rollout status deployment.apps/watch-image
kubectl rollout status deployment.apps/watch-info

# History Rolling Update status
kubectl rollout history deployment.apps/watch-image
kubectl rollout history deployment.apps/watch-info


