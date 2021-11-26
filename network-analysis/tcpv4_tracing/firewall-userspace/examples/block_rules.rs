use futures::stream::StreamExt;
use redbpf::load::{Loaded, Loader};
use std::collections::HashMap;
use std::env;
use std::process;
use std::ptr;
use std::sync::{Arc, Mutex};
use tokio;
use tokio::runtime::Runtime;
use tokio::signal;
use tokio::time::delay_for;
use redbpf::Module;
use redbpf::xdp;



fn main() {
    if unsafe { libc::getuid() } != 0 {
        eprintln!("You must be root to use eBPF!");
        process::exit(1);
    }
    
    let _ = Runtime::new().unwrap().block_on(async {

        //let mut module = Module::parse(&std::fs::read("vfsreadlat.elf").unwrap()).unwrap();
        let mut module = Loader::load(probe_code()).expect("error loading BPF program");
        //let mut module = Loader::load_file("vfsreadlat.elf").expect("error loading probe");
            for uprobe in module.xdps_mut() {
                uprobe.attach_xdp("wlp2s0", xdp::Flags::default()).unwrap();
            }


        signal::ctrl_c().await
    });
}

fn probe_code() -> &'static [u8] {
    include_bytes!(concat!(
        env!("OUT_DIR"),
        "/target/bpf/programs/block_rules/block_rules.elf"
    ))
}
