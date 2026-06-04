#!/bin/bash

# 1. Allow the container to connect to the local X server (for QEMU graphics)
if command -v xhost >/dev/null 2>&1; then
    xhost +local:root > /dev/null
fi

# 2. Run the container with all hardware and GUI permissions mapped
docker run -it \
  --privileged \
  -v /dev:/dev \
  -e DISPLAY="$DISPLAY" \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  --net=host \
  prg32-env