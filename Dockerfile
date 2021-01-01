FROM pytorch/torchserve:latest-gpu

USER root

RUN apt-get update

RUN apt-get -y install curl

COPY serve/examples/ /home/model-server/examples/

RUN curl -o /home/model-server/examples/image_classifier/densenet161-8d451a50.pth https://download.pytorch.org/models/densenet161-8d451a50.pth

USER model-server

RUN torch-model-archiver --model-name densenet161 --version 1.0 --model-file /home/model-server/examples/image_classifier/densenet_161/model.py --serialized-file /home/model-server/examples/image_classifier/densenet161-8d451a50.pth --export-path /home/model-server/model-store --extra-files /home/model-server/examples/image_classifier/index_to_name.json --handler image_classifier
