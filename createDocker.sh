
docker network create pencarian_network

docker build --tag pencarian-py:1.0.0 . -f Dockerfile

docker container create --name pencarian --network pencarian_network -p  80:8080 pencarian-py:1.0.0 

docker container start pencarian
