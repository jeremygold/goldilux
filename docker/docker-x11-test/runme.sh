#!/bin/bash
CONTAINER=xtermtest
#create the container using the Docker File Dockerfile
#it’s based on the default ubuntu container
#
docker build -t $CONTAINER .
# create the var to pass to docker linking host file X0 to container file X0
XSOCK=/tmp/.X11-unix/X0
# run the xterm xapp container
docker run --rm -v $XSOCK:$XSOCK --device=/dev/video0 -v $(pwd):/work $CONTAINER
