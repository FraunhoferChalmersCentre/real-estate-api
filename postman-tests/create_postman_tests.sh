#! /bin/bash

IMAGE_TAG=${IMAGE_TAG:=fcc-sys/oas-to-postman}

pushd ../
    docker run --rm \
        -e PORTMAN_TEST_HEATING_SYSTEM_ID=aHeatingSystemId \
        -e PORTMAN_TEST_RADIATOR_LOOP_ID=aRadiatorLoopId \
        -e PORTMAN_TEST_BUILDING_ID=aBuildingId \
        -e PORTMAN_TEST_SENSOR_ID=aSensorId \
        --mount type=bind,source=$PWD,target=/mnt/host \
        $IMAGE_TAG $@
popd
