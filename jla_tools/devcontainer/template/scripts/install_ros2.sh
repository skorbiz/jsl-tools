#!/bin/bash
set -euo pipefail

# Check if it's Ubuntu 22.04
ubuntu_version=$(lsb_release -r | awk '{print $2}')
if [ "$ubuntu_version" != "22.04" ]; then
    echo "This system is not running Ubuntu 22.04 - exiting"
    exit -1
fi


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

echo "source /opt/ros/iron/setup.bash" >> /home/dev/.bashrc
echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" >> /home/dev/.bashrc
