#!bin/bash

#Only working on ubuntu right now cargo 1.55 and llvm 12

#headers
sudo apt-get -y install build-essential zlib1g-dev \
		llvm-12-dev libclang-12-dev linux-headers-$(uname -r) \
		libelf-dev;

#rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh;
source $HOME/.cargo/env;
rustup default 1.55;

#llvm
wget https://apt.llvm.org/llvm.sh;
chmod +x llvm.sh;
sudo ./llvm.sh 12;

# RedBPF crate installation
cargo install cargo-bpf;