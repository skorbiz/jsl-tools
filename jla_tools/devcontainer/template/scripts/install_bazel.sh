#!/bin/bash 
set -euo pipefail

# Obs: bazel auto-completions and bazalisk to bazel mapping is done in main docker file 

export DEBIAN_FRONTEND=noninteractive 
apt-get update 
apt-get install -y --no-install-recommends \
    wget \

rm -rf /root/.cache/pip/*.
rm -rf /var/lib/apt/lists/*


wget https://golang.org/dl/go1.17.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.17.linux-amd64.tar.gz 

# Install bazel using bazelisk
echo 'export PATH=/home/dev/go/bin:$PATH:/usr/local/go/bin' >> /home/dev/.bashrc
GOPATH=/home/dev/go /usr/local/go/bin/go get github.com/bazelbuild/bazelisk@v1.12.2
GOPATH=/home/dev/go /usr/local/go/bin/go get github.com/bazelbuild/buildtools/buildifier
bazel

