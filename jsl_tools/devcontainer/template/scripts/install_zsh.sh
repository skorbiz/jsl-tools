#!/bin/bash
set -euo pipefail
set -x

echo "Installing zsh"
export DEBIAN_FRONTEND=noninteractive && apt-get update && apt-get install -y --no-install-recommends \
    zsh \
    && rm -rf /root/.cache/pip/*. \
    && rm -rf /var/lib/apt/lists/*

echo "Set zsh default terminal"
chsh -s /usr/bin/zsh


echo "Installing oh-my-zsh"
wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh; \
    sh ./install.sh; \
    rm ./install.sh
# ENV ZSH_THEME agnoster
# OBS this is not complete

#   fonts-powerline \
#   && locale-gen en_US.UTF-8 \
#   # terminal colors with xterm
#   ENV TERM xterm
#   # set the zsh theme
#   ENV ZSH_THEME agnoster
