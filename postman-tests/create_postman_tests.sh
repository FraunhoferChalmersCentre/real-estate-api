#! /bin/sh

IMAGE_TAG=${IMAGE_TAG:=fcc-sys/oas-to-postman}

docker run --rm \
    --mount type=bind,source=$PWD,target=/mnt/host \
    $IMAGE_TAG $@
