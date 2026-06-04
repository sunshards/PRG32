FROM ubuntu:24.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    git wget flex bison gperf python3 python3-venv python3-pip \
    cmake ninja-build ccache libffi-dev libssl-dev dfu-util \
    libusb-1.0-0 udev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory to /root (equivalent to $HOME)
WORKDIR /root

RUN git clone -b v5.3 --recursive https://github.com/espressif/esp-idf.git \
    && cd esp-idf \
    && ./install.sh esp32c3,esp32c6

RUN git clone https://github.com/raffmont/PRG32.git

RUN python3 -m venv .venv-platformio \
    && .venv-platformio/bin/activate \
    && pip install platformio

# Automatically source export.sh when starting the container
RUN echo ". /root/esp-idf/export.sh" >> /root/.bashrc

WORKDIR /root/PRG32

CMD ["/bin/bash"]