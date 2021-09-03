#! /bin/bash

IMAGE_TAG=${IMAGE_TAG:=fcc-sys/oas-to-postman}
DOCKERFILE=$PWD/Dockerfile.oas-to-postman

pushd ../
# the UID is required on Unix to make sure that the generated output file does not have its permissions set to root
    docker build \
        -f $DOCKERFILE \
        --build-arg uid=$(id -u) \
        -t $IMAGE_TAG .
popd
