#!/bin/bash

# Update & Upgrade Ubuntu
apt-get update -y
apt-get upgrade -y
apt-get full-upgrade -y

# Install all BPF tools needed
apt install bpfcc-tools bpftrace bpfcc-lua python3-bpfcc libbpfcc

# Install Figlet
apt install figlet

# Install Python3
apt install python3

# Install Pip
apt install pip

# PIP install bcc
pip install bcc

# Change directory
cd

# Get the v0.14.0 bcc version from bcc repository
wget https://github.com/iovisor/bcc/releases/download/v0.14.0/bcc-src-with-submodule.tar.gz

# Rename the bcc release .tar.gz
mv bcc-src-with-submodule.tar.gz bcc.tar.gz

# Uncompress it
tar -xf bcc.tar.gz

# Remove the .tar.gz file
rm bcc.tar.gz

# Git clone flamegraph repository
git clone https://github.com/brendangregg/FlameGraph