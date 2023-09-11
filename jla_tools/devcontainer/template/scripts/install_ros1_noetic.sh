#!/bin/bash 
set -euo pipefail

# Check if it's Ubuntu 20.04
ubuntu_version=$(lsb_release -r | awk '{print $2}')
if [ "$ubuntu_version" != "20.04" ]; then
    echo "This system is not running Ubuntu 20.04 - exiting"
    exit -1
fi


echo "Installing dependencies"
export DEBIAN_FRONTEND=noninteractive && apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gpg-agent \
    gnupg \
    && rm -rf /root/.cache/pip/*. \
    && rm -rf /var/lib/apt/lists/*

echo "Adding key"
sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -

apt update
apt install -y --no-install-recommends \
    ros-noetic-desktop-full

# Source for both bash and zsh
echo "source /opt/ros/noetic/setup.bash" >> /home/dev/.bashrc
echo "source /opt/ros/noetic/setup.zsh" >> /home/dev/.zshrc

# Project Armtrack dependencies
# ==============================

export DEBIAN_FRONTEND=noninteractive && apt-get update && apt-get install -y --no-install-recommends \
    can-utils \
    ros-noetic-joint-trajectory-controller \
    ros-noetic-socketcan-bridge \
    ros-noetic-twist-mux \
    && rm -rf /root/.cache/pip/*. \
    && rm -rf /var/lib/apt/lists/*