#!/bin/bash
docker build -t zmk-config/glove-config .
docker run --name glove-config -v $(pwd)/config:/app/config zmk-config/glove-config:latest
# copy the symlinked data out of the container
# docker cp glove-config:/app/config/combined $(pwd)/config/
docker container rm glove-config
