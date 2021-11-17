# Menga

When we download a docker image, and run it as a container, we have no guarantee on its malicious behavior or not. Indeed, docker images are regularly uploaded on public repositories open to everyone. So, an attacker can publish a malicious docker image on a public repository. This image could then be downloaded by a developer or an ops and executed on his infrastructure. 


Menga is an application that aims to analyze the behavior of docker containers running on a given infrastructure with the objective of detecting potentially malicious behavior of these containers: 

    - Illegal or unsolicited network traffic 

    - Suspicious CPU consumption (crypto-mining) 

    - Suspicious kernel calls 


The project is based on ebpf technology which allows for a wide variety of hook and probe functionality.


## Installation

# llvm-11

[https://apt.llvm.org/](https://apt.llvm.org/)

`bash -c "$(wget -O -(https://apt.llvm.org/llvm.sh))"`

llvm-config --version **should work**

# Install dependencies

Preparation for the cargo installation.

```bash
sudo apt-get -y install build-essential zlib1g-dev \
		llvm-11-dev libclang-11-dev linux-headers-$(uname -r)
```

# Install Rust

`curl --proto '=https' --tlsv1.2 -sSf [https://sh.rustup.rs](https://sh.rustup.rs/) | sh`

Don't forget to copy the environment PATH

# Examples

```bash
cargo install cargo-bpf
```

You might have some errors.

#Compilation:

`cargo build --examples and cargo make bpf`

##Running:

go in target/examples/ folder

and just run in sudo the executable

`sudo ./block_http`