
def wait_indirect_dma(semaphore: _ods_ir.Value[_ods_ir.MemRefType], src: _ods_ir.Value[_ods_ir.MemRefType], dst: _ods_ir.Value[_ods_ir.MemRefType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> WaitIndirectDMAOp:
  return WaitIndirectDMAOp(semaphore=semaphore, src=src, dst=dst, loc=loc, ip=ip)

