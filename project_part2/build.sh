cd info/
docker build -t andres112/watches-info:watches-info .
cd ../image/
docker build -t andres112/watches-image:watches-image .
docker push andres112/watches-info
docker push andres112/watches-image
