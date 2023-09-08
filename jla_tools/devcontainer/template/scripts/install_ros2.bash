#!/bin/bash
set -euo pipefail

# Install ROS2
export DEBIAN_FRONTEND=noninteractive && apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    curl
add-apt-repository universe

curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

echo 'Etc/UTC' > /etc/timezone && \
ln -s /usr/share/zoneinfo/Etc/UTC /etc/localtime

apt update && sudo apt install -y --no-install-recommends \
    ros-dev-tools
apt update && sudo apt install -y --no-install-recommends \
    ros-iron-desktop

echo "source /opt/ros/iron/setup.bash" >> ~/.bashrc
echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" >> ~/.bashrc
