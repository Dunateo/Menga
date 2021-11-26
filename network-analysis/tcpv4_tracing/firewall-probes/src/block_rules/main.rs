#![no_std]
#![no_main]

use redbpf_probes::xdp::prelude::*;

program!(0xFFFFFFFE, "GPL");


#[xdp]
pub fn block_port_80(ctx: XdpContext) -> XdpResult {
    if let Ok(transport) = ctx.transport() {
        if transport.dest() == 80 {
            return Ok(XdpAction::Drop);
            
        }else if transport.source() == 80  {
            return Ok(XdpAction::Drop);
        }
    }

    Ok(XdpAction::Pass)
}