# Remove previous images
docker rmi andres112/watch-info:latest 
docker rmi andres112/watch-image:latest 
# Create new images
cd info/
docker build -t andres112/watch-info:latest .
cd ../image/
docker build -t andres112/watch-image:latest .
# Push images to Docker Hub
docker push andres112/watch-info:latest
docker push andres112/watch-image:latest
