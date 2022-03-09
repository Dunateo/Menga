
use cty::*;

// This is where you should define the types shared by the kernel and user
// space, eg:
//
// #[repr(C)]
// #[derive(Debug)]
// pub struct SomeEvent {
//     pub pid: u64,
//     ...
// }

pub const PATHLEN: usize = 256;

#[repr(C)]
#[derive(Debug, Clone)]
pub struct OpenPath {
    pub filename: [u8; PATHLEN],
}

impl Default for OpenPath {
    fn default() -> OpenPath {
        OpenPath {
            filename: [0; PATHLEN],
        }
    }
}