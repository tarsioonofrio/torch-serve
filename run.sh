# TODO change to docker python api
docker kill $(docker ps -q)
docker rm $(docker ps -a -q)
docker run --rm \
        -it \
        -p 8080:8080 -p 8081:8081 \
        -p 7070:7070 -p 7071:7071 \
        --name mar \
#        -v $(pwd)/serve/examples:/home/model-server/examples \
        tarsioonofrio/torch-serve-test \
        torchserve --model-store=/home/model-server/model-store/ --models densenet161.mar #all